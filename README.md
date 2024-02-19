Install virtual environment 
**pip install virtualenv**

Create Virtual envirnoment
**virtualenv venv**

Activate virtual environment
**source venv/bin/activate** (Linux)
**venv\Scripts\activate** (Windows)

Install Requirements
**pip install -r requirements.txt**

**Add "export DJANGO_SETTINGS_MODULE=authentication.settings" in "venv/bin/activate"**

Run application
**python manage.py runserver 0.0.0.0:8000**

Run Tests
**pytest**
