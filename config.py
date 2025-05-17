import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cs50_pranav'
    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') or 'postgresql://postgres:vsp2004@localhost:5432/personal_dashboard'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
