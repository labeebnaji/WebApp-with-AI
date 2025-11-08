// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
 // --- 1. إدارة الوضع (Theme) ---
    const themeToggleButton = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            const theme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            themeToggleButton.style.transform = 'scale(1.2)';
            setTimeout(() => {
                themeToggleButton.style.transform = 'scale(1)';
            }, 200);
        });
    }
      document.body.classList.add('loaded');

 const mobileMenuButton = document.getElementById('mobileMenuButton');
  const navLinks = document.getElementById('navLinks');
  const overlay = document.getElementById('overlay');
  
  if (mobileMenuButton && navLinks && overlay) {
    mobileMenuButton.addEventListener('click', function() {
      navLinks.classList.toggle('active');
      overlay.classList.toggle('active');
      document.body.classList.toggle('menu-open');
    });
    
    overlay.addEventListener('click', function() {
      navLinks.classList.remove('active');
      overlay.classList.remove('active');
      document.body.classList.remove('menu-open');
    });
    
    const navItems = navLinks.querySelectorAll('a');
    navItems.forEach(item => {
      item.addEventListener('click', function() {
        navLinks.classList.remove('active');
        overlay.classList.remove('active');
        document.body.classList.remove('menu-open');
      });
    });
  }
  

    // --- 3. تأثيرات التنقل (للشاشات الكبيرة فقط) ---
    if (window.innerWidth > 768) {
        const navLinks = document.querySelectorAll('.nav-links a');
        if (navLinks) {
            navLinks.forEach(link => {
                link.addEventListener('mouseenter', () => {
                    link.style.transform = 'translateY(-2px)';
                });
                
                link.addEventListener('mouseleave', () => {
                    link.style.transform = 'translateY(0)';
                });
            });
        }
    }
    
    // --- 4. تأثيرات الأزرار ---
    const buttons = document.querySelectorAll('button, .action-btn, .browse-btn');
    if (buttons) {
        buttons.forEach(button => {
            button.addEventListener('mousedown', () => {
                button.style.transform = 'translateY(2px)';
            });
            
            button.addEventListener('mouseup', () => {
                button.style.transform = 'translateY(-3px)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translateY(0)';
            });
        });
    }
    
  // تأثير التمرير
  window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
    
    // --- تأثيرات الصفحة عند التحميل ---
    window.addEventListener('load', function() {
        document.body.style.opacity = '1';
    });

    // --- 5. تأثيرات الصفحة الرئيسية ---
    if (document.querySelector('.dashboard-header')) {
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = `all 0.5s ease ${index * 0.1}s`;
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 500 + (index * 100));
        });
    }
    
    // --- 6. تأثيرات صفحة الفريق ---
    if (document.querySelector('.team-grid')) {
        const teamMembers = document.querySelectorAll('.team-member');
        teamMembers.forEach((member, index) => {
            member.style.opacity = '0';
            member.style.transform = 'scale(0.9)';
            member.style.transition = `all 0.5s ease ${index * 0.1}s`;
            
            setTimeout(() => {
                member.style.opacity = '1';
                member.style.transform = 'scale(1)';
            }, 500 + (index * 100));
        });
    }
    
    // --- 7. تأثيرات صفحة الرفع ---
    if (document.querySelector('.upload-area')) {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('fileInput');
    const runModelBtn = document.querySelector('.run-model-btn');
    const lang = document.documentElement.lang || 'ar'; // تحديد اللغة من الـ HTML

    // رسائل متعددة اللغات
    const messages = {
        'ar': {
            success: 'تم رفع الملف بنجاح!',
            error: 'حدث خطأ أثناء رفع الملف',
            fileTypeError: 'يجب رفع ملف CSV فقط',
            fileSizeError: 'حجم الملف كبير جداً'
        },
        'en': {
            success: 'File uploaded successfully!',
            error: 'Error uploading file',
            fileTypeError: 'Only CSV files are allowed',
            fileSizeError: 'File size is too large'
        }
    };

    // عرض رسالة للمستخدم
    function showMessage(type, messageKey) {
        const messageType = type === 'success' ? 'success' : 'error';
        const color = type === 'success' ? 'var(--success-color)' : 'var(--danger-color)';
        const bgColor = type === 'success' ? 'rgba(0, 184, 148, 0.2)' : 'rgba(255, 71, 87, 0.2)';

        const existingMsg = uploadArea.querySelector('.upload-message');
        if (existingMsg) existingMsg.remove();

        const messageDiv = document.createElement('div');
        messageDiv.className = `upload-message ${messageType}`;
        messageDiv.innerHTML = `
            <div style="background: ${bgColor}; padding: 1rem; border-radius: 8px; 
                        margin-top: 1rem; border-left: 4px solid ${color};">
                <p style="color: ${color}; font-weight: 600; margin: 0;">
                    ${messages[lang][messageKey]}
                </p>
            </div>
        `;
        
        uploadArea.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    // أحداث السحب والإفلات
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--accent-color)';
        uploadArea.style.backgroundColor = 'rgba(253, 121, 168, 0.05)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.backgroundColor = 'var(--card-bg)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.backgroundColor = 'var(--card-bg)';
        
        if (e.dataTransfer.files.length) {
            const file = e.dataTransfer.files[0];
            
            // التحقق من نوع الملف
            if (!file.name.endsWith('.csv')) {
                showMessage('error', 'fileTypeError');
                return;
            }
            
            // التحقق من حجم الملف (5MB كحد أقصى كمثال)
            if (file.size > 5 * 1024 * 1024) {
                showMessage('error', 'fileSizeError');
                return;
            }
            
            fileInput.files = e.dataTransfer.files;
            showMessage('success', 'success');
            runModelBtn.disabled = false;
        }
    });

    // حدث تغيير الملف عبر الزر
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            const file = fileInput.files[0];
            
            if (!file.name.endsWith('.csv')) {
                showMessage('error', 'fileTypeError');
                fileInput.value = '';
                return;
            }
            
            if (file.size > 5 * 1024 * 1024) {
                showMessage('error', 'fileSizeError');
                fileInput.value = '';
                return;
            }
            
            showMessage('success', 'success');
            runModelBtn.disabled = false;
        }
    });

    // إعادة تعيين الأنماط عند إرسال النموذج
    document.querySelector('.upload-form').addEventListener('submit', () => {
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.backgroundColor = 'var(--card-bg)';
    });
}
    
    // --- 8. تهيئة الرسوم البيانية ---
    if (document.getElementById('threatsChart')) {
        // إعداد الألوان بناءً على الوضع الحالي
        const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDarkMode ? '#f5f6fa' : '#2d3436';
        const gridColor = isDarkMode ? '#3d4a54' : '#dfe6e9';
        
        // رسم بياني للتهديدات حسب الوقت (خط)
        const threatsCtx = document.getElementById('threatsChart').getContext('2d');
        new Chart(threatsCtx, {
            type: 'line',
            data: {
                labels: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
                datasets: [{
                    label: 'التهديدات المكتشفة',
                    data: [3, 7, 5, 12, 8, 15],
                    borderColor: '#6c5ce7',
                    backgroundColor: 'rgba(108, 92, 231, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: '#6c5ce7',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: textColor,
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: isDarkMode ? '#2d3436' : '#ffffff',
                        titleColor: isDarkMode ? '#a29bfe' : '#6c5ce7',
                        bodyColor: textColor,
                        borderColor: isDarkMode ? '#3d4a54' : '#dfe6e9',
                        borderWidth: 1,
                        padding: 12,
                        usePointStyle: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: textColor
                        },
                        grid: {
                            color: gridColor,
                            drawBorder: false
                        }
                    },
                    x: {
                        ticks: {
                            color: textColor
                        },
                        grid: {
                            color: gridColor,
                            drawBorder: false
                        }
                    }
                }
            }
        });

        // رسم بياني لأنواع الهجمات (دائري)
        const attackTypesCtx = document.getElementById('attackTypesChart').getContext('2d');
        new Chart(attackTypesCtx, {
            type: 'doughnut',
            data: {
                labels: ['احتيال بطاقات', 'غسيل أموال', 'هجمات تصيد', 'أخرى'],
                datasets: [{
                    data: [40, 25, 20, 15],
                    backgroundColor: [
                        '#6c5ce7',
                        '#a29bfe',
                        '#fd79a8',
                        '#fdcb6e'
                    ],
                    borderWidth: 2,
                    borderColor: isDarkMode ? '#2d3436' : '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: textColor,
                            padding: 20,
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: isDarkMode ? '#2d3436' : '#ffffff',
                        titleColor: isDarkMode ? '#a29bfe' : '#6c5ce7',
                        bodyColor: textColor,
                        borderColor: isDarkMode ? '#3d4a54' : '#dfe6e9',
                        borderWidth: 1,
                        padding: 12,
                        usePointStyle: true
                    }
                },
                cutout: '70%',
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });

        // تحديث الرسوم البيانية عند تغيير الوضع
        if (themeToggleButton) {
            themeToggleButton.addEventListener('click', function() {
                setTimeout(() => {
                    window.location.reload();
                }, 300);
            });
        }
    }
});

// --- 9. تأثيرات الصفحة عند التحميل ---
window.addEventListener('load', function() {
    document.body.style.opacity = '1';
    
    // تأثيرات للأجهزة المحمولة
    if (window.innerWidth <= 768) {
        const elements = document.querySelectorAll('.stat-card, .chart-container, .team-member, .profile-card');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = `all 0.5s ease ${index * 0.1}s`;
            
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, 300 + (index * 100));
        });
    }
});