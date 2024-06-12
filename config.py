from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print('SECRET_KEY :',SECRET_KEY)
    print('SQLALCHEMY_DATABASE_URI :',SQLALCHEMY_DATABASE_URI)
