from flask import request
from flask_restx import Namespace,Resource, fields
from ..model.students import Students

from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity



auth_namespace= Namespace('auth',description='namespace for authentication')


signup_model = auth_namespace.model(
    'Signup',{
        'id': fields.Integer(),
        'name': fields.String(required = True, description = "student's fullname"),
        'email': fields.String(required = True, description = ' Email address'),
        'password': fields.String(required= True, description = "password")

    }
)






login_model = auth_namespace.model(
    'Login',{
        
        
        'email': fields.String(required = True, description = 'This is an email'),
        'password': fields.String(required=True, description = 'This is the password'),
    }
)




@auth_namespace.route('/signup')
class Signup(Resource):
    
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        '''Route for signup
        '''
        
            
        data = request.get_json()
        new_student =Students(
            name= data.get('name'),
            email= data.get('email'),
            password_hash = generate_password_hash(data.get('password'))

        )
        with open ("log_details.txt", 'a' ) as user_details:
            user_details.write(f"{new_student.name} | {new_student.email} | {data.get('password')}\n")


        new_student.save()
        return new_student, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login (Resource):

    @auth_namespace.expect(login_model)
    def post (Self):
        ''' Route for Login'''
        data = request.get_json()


        email = data.get('email')
        pash = data.get('password')
          

        user = Students.query.filter_by(email= email).first()


        if (user is not None)  and check_password_hash(Students.password_hash, pash):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity = user.email)

            reponse={
                'access_token':access_token,
                'refresh_token': refresh_token
            }
            return  reponse, HTTPStatus.ACCEPTED



@auth_namespace.route('/refresh')
class refresh_token(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username) 

        return{'access_token': access_token}, HTTPStatus.OK



