from flask import Flask
from flask_restx import Api
from .utils import db 
from .config.config import config_dict
from flask_migrate import Migrate
from .auth.views import auth_namespace
from .course.courses import course_namespace
from .students.allstudent import student_namespace
from .model.students import Form,Students
from .model.courses import Course
from flask_jwt_extended import JWTManager



def create_app(config = config_dict['dev']):
    app = Flask(__name__)
    app.config['SECRET_KEY']="ba06f31fc148b172db2e77"
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    

    migrate = Migrate(app,db)
    
    api = Api(app)

    api.add_namespace(course_namespace, path = '/course')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(student_namespace,path='/student')



    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'courses':Course,
            'students':Students,
            'grades':Form

        }


    @app.before_first_request
    def create_table():
        db.create_all()
    return app