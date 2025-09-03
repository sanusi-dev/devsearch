# DevSearch 🔍

**Developer Talent Marketplace Platform**

A comprehensive web-based marketplace that connects skilled developers with clients seeking technical expertise. The platform features dynamic developer portfolios showcasing skills, projects, and experience, enabling clients to easily discover and engage qualified talent.

## 🚀 Features

- **Professional Developer Profiles** - Create detailed portfolios showcasing skills, projects, and experience
- **Talent Discovery System** - Advanced browsing and search capabilities for clients to find developers
- **Integrated Communication** - Contact forms with automated email notifications
- **Community Quality Assurance** - Upvoting/downvoting system for projects
- **Rating & Reviews** - Comprehensive rating system with detailed feedback comments
- **Direct Messaging** - Seamless communication between developers and clients

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3
- **Database:** SQLite

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/sanusi-dev/devsearch.git
cd devsearch
```

### 2. Create Virtual Environment
```bash
pip install virtualenv
virtualenv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📂 Project Structure

```
devsearch/
├── devsearch/          # Main project directory
├── users/              # User management app
├── projects/           # Project portfolio app
├── profiles/           # Users profile app
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
├── media/              # User uploaded files
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## 🙏 Acknowledgments

- Django community for the amazing framework
- Denis Ivy who inspired me through his udemy course to create this project

## 📸 Screenshots

### Home Page
![Devsearch Home](https://github.com/user-attachments/assets/f6a75330-a46b-4f00-8ad4-65a127d7e466)

### Profile Page
![Devsearch Profile](https://github.com/user-attachments/assets/1b198682-b422-4d11-9fcf-3f8554315d23)

### Project Page
![DevSearch Projects](https://github.com/user-attachments/assets/3a2c6a72-daaf-4f45-a416-24a4add82829)

### Inbox Page
<img width="1273" height="518" alt="Devsearch Inbox" src="https://github.com/user-attachments/assets/bfc74987-22ed-4c8d-876c-c41c7c57401d" />

## 🔮 Future Enhancements

- [ ] Real-time chat functionality
- [ ] Advanced search filters
- [ ] Payment integration
- [ ] API endpoints for third-party integrations

---

⭐ If you found this project helpful, please give it a star!
