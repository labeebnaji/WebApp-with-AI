import sqlite3
import json
from flask import Flask, render_template, request, g, url_for, redirect
from datetime import datetime, timezone, timedelta
import pandas as pd
import pickle
import numpy as np




# --- Application Initialization ---
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this for production
DATABASE = 'frauddetect.db'

def get_db():
    """Create database connection if it doesn't exist"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        # Enable foreign key constraints
        db.execute("PRAGMA foreign_keys = ON")
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection at the end of the request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database using schema.sql"""
    with app.app_context():
        db = get_db()
        try:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            db.rollback()

@app.cli.command('init-db')
def init_db_command():
    """Create database tables"""
    init_db()
    print("Database tables created.")

# --- Language Support (i18n) ---
LANGUAGES = {
    'en': {
        'name': 'English',
        'dir': 'ltr'
    },
    'ar': {
        'name': 'العربية',
        'dir': 'rtl'
    }
}
DEFAULT_LANGUAGE = 'ar'
TRANSLATIONS = {}

try:
    for lang in LANGUAGES:
        with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
            TRANSLATIONS[lang] = json.load(f)
except FileNotFoundError as e:
    print(f"Translation files not found: {str(e)}")
    TRANSLATIONS = {lang: {} for lang in LANGUAGES}

def get_locale():
    """Determine the best language match"""
    # Check URL parameter first
    lang = request.args.get('lang')
    if lang in LANGUAGES:
        return lang
    
    # Fallback to default language
    return DEFAULT_LANGUAGE

@app.before_request
def before_request():
    """Set up global template variables"""
    g.lang = get_locale()
    g.translations = TRANSLATIONS.get(g.lang, {})
    g.current_lang = g.lang
    g.target_lang = 'en' if g.lang == 'ar' else 'ar'
    g.lang_config = LANGUAGES.get(g.lang, LANGUAGES[DEFAULT_LANGUAGE])
    g.now = datetime.now()    

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# --- Page Routes ---

@app.route('/')
def index():
    """Home page"""
    try:
        db = get_db()
        
        # إحصائيات التهديدات
        threats_stats = {
            'current_month': db.execute('''
                SELECT COUNT(*) FROM transactions 
                WHERE prediction = 0 
                
            ''').fetchone()[0],
            'last_month': db.execute('''
                SELECT COUNT(*) FROM transactions 
                WHERE prediction = 0 
                AND strftime('%m', transaction_date) = strftime('%m', 'now', '-1 month')
            ''').fetchone()[0]
        }
        
        # إحصائيات المعاملات
        transactions_stats = {
            'total': db.execute('SELECT COUNT(*) FROM transactions').fetchone()[0],
            'fraud': db.execute('SELECT COUNT(*) FROM transactions WHERE prediction = 0').fetchone()[0]
        }
        
        # حساب النسب المئوية للتغير
        threats_change = calculate_percentage_change(threats_stats['current_month'], threats_stats['last_month'])
        fraud_percentage = (transactions_stats['fraud'] / transactions_stats['total']) * 100 if transactions_stats['total'] > 0 else 0
        
        # بيانات الرسوم البيانية
        threats_by_time = db.execute('''
            SELECT strftime('%d', transaction_date) as day, COUNT(*) as count
            FROM transactions 
            WHERE prediction = 0
            GROUP BY day
            ORDER BY day
        ''').fetchall()
        
        attack_types = db.execute('''
            SELECT category, COUNT(*) as count
            FROM transactions
            WHERE prediction = 0
            GROUP BY category
            ORDER BY count DESC
            LIMIT 5
        ''').fetchall()
        
        return render_template('index.html',
                            threats_count=threats_stats['current_month'],
                            threats_change=threats_change,
                            fraud_count=transactions_stats['fraud'],
                            fraud_percentage=fraud_percentage,
                            security_score=100 - min(fraud_percentage * 2, 100),  # حساب افتراضي لمؤشر الأمان
                            threats_by_time=threats_by_time,
                            attack_types=attack_types)
        
    except Exception as e:
        app.logger.error(f"Dashboard error: {str(e)}")
        return render_template('errors/500.html'), 500

def calculate_percentage_change(current, previous):
    """حساب نسبة التغير بين القيم الحالية والسابقة"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """File upload and model prediction page"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error="No file uploaded")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error="No file selected")
        
        if file and file.filename.endswith('.csv'):
            try:
                # تحميل البيانات من CSV
                df = pd.read_csv(file)
                required_columns = [
                    'cc_num', 'category', 'amt', 'zip', 'lat', 'long', 
                    'city_pop', 'merch_lat', 'merch_long', 'trans_day', 
                    'trans_month', 'trans_year', 'trans_hour', 'trans_minute'
                ]
                
                if not all(col in df.columns for col in required_columns):
                    missing = [col for col in required_columns if col not in df.columns]
                    return render_template('upload.html', error=f"Missing columns: {', '.join(missing)}")
                
                # تحميل النموذج
                with open('random_forest_model.pkl', 'rb') as f:
                    model = pickle.load(f)
                
                # التنبؤ
                features = df[required_columns]
                predictions = model.predict(features)
                
                # إضافة النتائج إلى البيانات
                df['prediction'] = predictions
                df['result_color'] = df['prediction'].apply(lambda x: 'green' if x == 1 else 'red')
                df['result_text'] = df['prediction'].apply(lambda x: 'سليمة' if x == 1 else 'احتيالية')
                
                # حفظ المعاملات في قاعدة البيانات
                db = get_db()
                user = db.execute('SELECT id FROM user WHERE username = ?', ('Ahmed',)).fetchone()
                
                for _, row in df.iterrows():
                    db.execute('''
                        INSERT INTO transactions (
                            user_id, cc_num, category, amt, zip, lat, long, city_pop,
                            merch_lat, merch_long, trans_day, trans_month, trans_year,
                            trans_hour, trans_minute, prediction, transaction_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user['id'], str(row['cc_num']), row['category'], row['amt'], 
                        str(row['zip']), row['lat'], row['long'], row['city_pop'],
                        row['merch_lat'], row['merch_long'], row['trans_day'],
                        row['trans_month'], row['trans_year'], row['trans_hour'],
                        row['trans_minute'], row['prediction'],
                        f"{row['trans_year']}-{row['trans_month']}-{row['trans_day']}"
                    ))
                
                # تحديث نقاط المستخدم إذا كانت هناك معاملات احتيالية
                fraud_count = sum(1 for p in predictions if p == 0)
                if fraud_count > 0:
                    db.execute('''
                        UPDATE user_points 
                        SET points = points + ?, 
                            last_updated = datetime('now')
                        WHERE user_id = ?
                    ''', (fraud_count, user['id']))
                    
                    # منح إنجازات بناءً على النقاط
                    points = db.execute('SELECT points FROM user_points WHERE user_id = ?', (user['id'],)).fetchone()[0]
                    
                    if points >= 10:
                        db.execute('''
                            UPDATE achievements 
                            SET unlocked = TRUE, 
                                unlocked_at = datetime('now')
                            WHERE user_id = ? AND achievement_type = 'expert'
                        ''', (user['id'],))
                    
                    if points >= 20:
                        db.execute('''
                            UPDATE achievements 
                            SET unlocked = TRUE, 
                                unlocked_at = datetime('now')
                            WHERE user_id = ? AND achievement_type = 'cyber_master'
                        ''', (user['id'],))
                
                db.commit()
                
                # تحويل النتائج إلى قوائم لعرضها في القالب
                results = df.to_dict('records')
                return render_template('upload.html', results=results)
            
            except Exception as e:
                return render_template('upload.html', error=f"Error processing file: {str(e)}")
    
    return render_template('upload.html')

@app.route('/alerts')
def alerts():
    """Alerts page with real data"""
    try:
        db = get_db()
        
        # جلب إحصائيات المعاملات
        stats = {
            'total_transactions': db.execute('SELECT COUNT(*) FROM transactions').fetchone()[0],
            'fraud_count': db.execute('SELECT COUNT(*) FROM transactions WHERE prediction = 0').fetchone()[0],
            'safe_count': db.execute('SELECT COUNT(*) FROM transactions WHERE prediction = 1').fetchone()[0]
        }
        
        # جلب آخر 50 معاملة
        transactions = db.execute('''
            SELECT * FROM transactions 
            ORDER BY trans_year DESC, trans_month DESC, trans_day DESC 
            LIMIT 50
        ''').fetchall()
        
        return render_template('alerts.html', 
                            stats=stats,
                            transactions=transactions)
        
    except sqlite3.Error as e:
        app.logger.error(f"Alerts error: {str(e)}")
        return render_template('errors/500.html'), 500
    except Exception as e:
        app.logger.error(f"Unexpected error in alerts: {str(e)}")
        return render_template('errors/500.html'), 500
# ... (الكود الحالي يبقى كما هو)

# تحديث دالة upload لحفظ المعاملات في قاعدة البيانات

@app.route('/achievements')
def achievements():
    try:
        db = get_db()
        
        # جلب بيانات المستخدم (افتراضي: student)
        user = db.execute('SELECT id FROM user WHERE username = ?', ('Ahmed',)).fetchone()
        if not user:
            return redirect(url_for('profile'))
        
        # جلب الإنجازات
        achievements_data = db.execute('''
            SELECT achievement_type, unlocked 
            FROM achievements 
            WHERE user_id = ?
        ''', (user['id'],)).fetchall()
        
        # تحضير البيانات للقالب
        achievements = {
            'finder': False,
            'expert': False,
            'cyber_master': False,
            'unlocked_count': 0,
            'total_count': 3,
            'completion_percentage': 0
        }
        
        for ach in achievements_data:
            achievements[ach['achievement_type']] = bool(ach['unlocked'])
            if ach['unlocked']:
                achievements['unlocked_count'] += 1
        
        # حساب نسبة الإكمال
        achievements['completion_percentage'] = int((achievements['unlocked_count'] / achievements['total_count']) * 100)
        
        return render_template('achievements.html', achievements=achievements)
        
    except sqlite3.Error as e:
        app.logger.error(f"Achievements error: {str(e)}")
        return render_template('errors/500.html'), 500

@app.route('/profile')
def profile():
    """User profile page"""
    try:
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username = ?', ('Ahmed',)).fetchone()
        
        if not user:
            return render_template('errors/404.html', 
                                message="User not found",
                                home_url=url_for('index')), 404
        
        # تحويل كائن sqlite3.Row إلى قاموس
        user_dict = dict(user)
        
        # إضافة الحقول الناقصة إن لم تكن موجودة
        user_dict.setdefault('last_login', 'غير محدد')
        user_dict.setdefault('twitter_link', None)
        
        app.logger.debug(f"User data: {user_dict}")
        return render_template('profile.html', user=user_dict)
        
    except sqlite3.Error as e:
        app.logger.error(f"Database error: {str(e)}", exc_info=True)
        return render_template('errors/500.html',
                            error_message=str(e),
                            home_url=url_for('index')), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return render_template('errors/500.html',
                            error_message="Internal Server Error",
                            home_url=url_for('index')), 500

@app.route('/debug/user')
def debug_user():
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE username = ?', ('Ahmed',)).fetchone()
    return dict(user) if user else "No user found"
# --- API Routes ---
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'timestamp': datetime.now(timezone.utc).isoformat()}

# --- Application Entry Point ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Debug should be False in production