# FraudDetect AI 🛡️

An intelligent fraud detection system for financial transactions using Artificial Intelligence and Machine Learning.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 📋 Description

FraudDetect AI is an advanced system that uses Machine Learning algorithms (Random Forest) to analyze financial transactions and detect fraudulent activities with high accuracy. The system provides a comprehensive dashboard with real-time analytics and supports multiple languages.

## ✨ Features

- 🤖 **Intelligent Fraud Detection** using Random Forest ML Model
- 📊 **Interactive Dashboard** with live charts and analytics
- 📁 **CSV File Upload & Analysis** with automatic processing
- 🌍 **Bilingual Support** (Arabic & English) with RTL/LTR
- 🌓 **Dual Theme Mode** (Light & Dark)
- 🏆 **Achievements & Points System** for user engagement
- 📱 **Responsive Design** works on all devices
- 📈 **Real-time Statistics** and threat visualization
- 🔍 **Transaction History** with detailed analysis

## 🛠️ Technologies Used

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

### Libraries & Tools
- **Flask 3.0.3** - Web framework
- **Werkzeug 3.0.1** - WSGI utility library
- **Pandas 2.2.2** - Data manipulation and analysis
- **NumPy 1.26.4** - Numerical computing
- **Scikit-learn 1.5.0** - Machine Learning algorithms
- **Chart.js** - Interactive charts
- **Font Awesome** - Icon library

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Installation Steps as a local
1. **Clone the repository:**
```bash
git clone https://github.com/labeebnaji/WebApp-with-AI.git
cd frauddetect-ai/Frauddetect-ai-WebApp
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install required packages:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your settings
```

5. **Initialize the database:**
```bash
python -c "from app import app, init_db; init_db()"
```

6. **Run the application:**
```bash
python app.py
```

7. **Open your browser:**
```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
frauddetect-ai/
├── app.py                      # Main application file
├── schema.sql                  # Database schema
├── requirements.txt            # Python dependencies
├── random_forest_model.pkl     # ML model (trained)
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── README.md                  # Project documentation
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       └── main.js           # JavaScript functionality
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Dashboard page
│   ├── upload.html           # File upload page
│   ├── alerts.html           # Alerts & analytics page
│   ├── profile.html          # User profile page
│   ├── achievements.html     # Achievements page
│   └── errors/               # Error pages
│       ├── 404.html
│       └── 500.html
└── translations/              # Language files
    ├── ar.json               # Arabic translations
    └── en.json               # English translations
```

## 📊 Usage

### 1. Upload CSV File
- Navigate to "Upload Data" page
- Upload a CSV file containing transactions
- Click "Run Model" to analyze

### 2. View Results
- Transactions are automatically analyzed
- Fraudulent transactions appear in red
- Safe transactions appear in green
- View detailed statistics on the dashboard

### 3. Monitor Statistics
- Dashboard displays comprehensive statistics
- Interactive charts for threat visualization
- Overall security score indicator

## 📝 CSV File Format

The CSV file must contain the following columns:

```csv
cc_num,category,amt,zip,lat,long,city_pop,merch_lat,merch_long,trans_day,trans_month,trans_year,trans_hour,trans_minute
```

### Example:
```csv
cc_num,category,amt,zip,lat,long,city_pop,merch_lat,merch_long,trans_day,trans_month,trans_year,trans_hour,trans_minute
4532123456789012,grocery,45.50,12345,40.7128,-74.0060,8000000,40.7580,-73.9855,15,1,2025,14,30
6011987654321098,gas_transport,75.20,54321,34.0522,-118.2437,4000000,34.0689,-118.4452,16,1,2025,9,15
```

### Column Descriptions:
- `cc_num`: Credit card number
- `category`: Transaction category (grocery, gas_transport, etc.)
- `amt`: Transaction amount
- `zip`: ZIP code
- `lat`, `long`: Customer location coordinates
- `city_pop`: City population
- `merch_lat`, `merch_long`: Merchant location coordinates
- `trans_day`, `trans_month`, `trans_year`: Transaction date
- `trans_hour`, `trans_minute`: Transaction time

## 🎯 Features Overview

### Dashboard
- Real-time threat detection statistics
- Monthly comparison charts
- Security score indicator
- Interactive data visualization

### Upload & Analysis
- Drag & drop file upload
- Automatic CSV validation
- Batch transaction processing
- Instant fraud detection results

### Alerts & Analytics
- Comprehensive transaction history
- Fraud/Safe transaction filtering
- Detailed transaction information
- Export capabilities (coming soon)

### User Profile
- Personal information management
- Social media links
- Activity tracking
- Achievement progress

### Achievements System
- **Threat Finder**: Discover your first security threat
- **Security Expert**: Discover 50+ security threats
- **Cybersecurity Master**: Master all security modules

## ⚙️ Configuration

### Environment Variables (.env)
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=frauddetect.db
DEBUG=True
HOST=0.0.0.0
PORT=5000
MAX_CONTENT_LENGTH=16777216
```

## 🔒 Security Notes

⚠️ **Important:** This system is for educational and development purposes. Before using in production:

1. ✅ Enable SECRET_KEY in app.py
2. ✅ Implement user authentication system
3. ✅ Encrypt credit card numbers
4. ✅ Add CSRF Protection
5. ✅ Use HTTPS
6. ✅ Add Rate Limiting
7. ✅ Implement proper logging
8. ✅ Use production-grade database (PostgreSQL/MySQL)
9. ✅ Add input validation and sanitization
10. ✅ Implement backup mechanisms

## 🚀 Deployment

### For Production:

1. **Use a production WSGI server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Set environment to production:**
```env
FLASK_ENV=production
DEBUG=False
```

3. **Use a reverse proxy (Nginx/Apache)**

4. **Enable HTTPS with SSL certificate**

5. **Use a production database**

## 🧪 Testing

```bash
# Run tests (when implemented)
python -m pytest tests/

# Check code coverage
python -m pytest --cov=app tests/
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Labeeb Al Baqeri** - *Initial work*

## 🙏 Acknowledgments

- Flask documentation and community
- Scikit-learn for ML algorithms
- Chart.js for beautiful visualizations
- Font Awesome for icons
- All contributors and supporters

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Upload Page
![Upload](screenshots/upload.png)

### Results
![Results](screenshots/results.png)

---

**Made with ❤️ using Flask & Python**

⭐ **Star this repo if you find it useful!**
