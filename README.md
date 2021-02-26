# Badger-Bytes-OrderManagement-System

## Project Structure

```bash
├── LICENSE
├── README.md
├── __init__.py
├── core
│   ├── __init__.py
│   ├── models
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── main.py
├── requirements.txt
├── static
│   ├── css
│   ├── html
│   └── js
├── templates
│   └── index.html
└── tests
    └── __init__.py
```

Core: 

- This will contain core implementations of the application
- Models: DB structure for each accounts 
- Utils: Functionalities implementation

 Static: 

 - HTML, JS and CSS static files directory

 Templates:

 - Jinja templates for UI

 ## Dev Setup
 - Install Virtualenv
 ```bash
 sudo pip3 install virtualenv
 ```
 - Create virtualenv folder
 ```bash
python3 -m venv en
 ```
 Activate Virtualenv
 ```bash
 source env/bin/activate
 ```
 Install requirements
 ```bash
 pip3 install -r requirements.txt
 ```
 Deactivate Virtualenv
 ```bash
deactivate
```

## Seeing All Data
```python
from server import db, app
from models import User
app.app_context().push()
User.query.all()
```
