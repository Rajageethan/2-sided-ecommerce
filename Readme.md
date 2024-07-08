# Home Grown Heaven

A simple Two sided E-commerce platform build to support local Farmer by eliminating the middlemen.

## Setup

### Prerequisites

Flask==2.0.2
Flask-MySQLdb==0.2.0
Flask-Bcrypt==0.7.1
Flask-Login==0.5.0
Flask-Mail==0.9.1
geopy==2.2.0
requests==2.26.0

### Installation

#### 1. Root FOlder setup

Use the Tree given below and set up your root folder

project-root/
├── app_farmer/
│   ├── farmer_app.py
│   ├── forms.py
│   ├── static/
│   │   └── your images
│   │       
│   ├── templates/
│   │   |
│   │   ├── farmer_home.html
│   │   ├── farmer_login.html
│   │   └── farmer_signup.html
│   └── ...
│
├── app_consumer/
│   ├── consumer_app.py
│   ├── forms.py
│   ├── static/
│   │   └── your images
│   │       
│   ├── templates/
│   │   |
│   │   ├── buyer_home.html
│   │   ├── buyer_login.html
│   │   └── buyer_signup.html
│   └── ...
│
├── create_database.py
│   
│
├── README.md
├── requirements.txt

#### 2.Install Dependencies

Run - "pip install -r requirements.txt" on terminal

#### 3.Create Database

Run - "python create_database.py" on terminal

## NOTE

Not completed
Has basic functionalities of a e-commerce site.
Need to add payment method#   2 - s i d e d - e c o m m e r c e  
 