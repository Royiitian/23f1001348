from flask import Flask
from application.modeles import User, Role, db
from application.config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore
from application.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.register_blueprint(routes)
    app.app_context().push()
    return app

app = create_app()




if __name__ == "__main__":
    app.run()