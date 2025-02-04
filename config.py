class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = True

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hsv2.sqlite3'
    DEBUG = True

    SECRET_KEY = 'shouvik_roy'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'household_service_2'
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'