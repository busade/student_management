from flask import request
from flask_restx import Namespace,Resource, fields
from ..model.students import Students, Form,Score
from ..model.courses import Course
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from ..utils import db
from ..course.courses import score_model
from ..utils.grades import Getgrade

student_namespace = Namespace('student', description='namesapce for students')
 

student_model= student_namespace.model(
    'student',{
        'id': fields.Integer(),
        'name':fields.String(required = True, Description= " Student full name"),
        'email':fields.String(required = True, Description = 'Student email'),
        
    }

)








@student_namespace.route('/student')
class Create(Resource):

    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self):
        '''returning registered students'''
        students = Students.query.all()

        return students, HTTPStatus.OK
    





@student_namespace.route('/student/<int:student_id>')
class GetUpdateDelete(Resource):

    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self,student_id):
        ''''getting a particular student by id'''
        student = Students.get_by_id(student_id)

        return student, HTTPStatus.OK


    @student_namespace.marshal_with(student_model)
    @student_namespace.expect(student_model)
    @jwt_required()
    def put(self,student_id):
        '''updating a particular student details'''
        student = Students.get_by_id(student_id)
        data = student_namespace.payload

        student.name = data['name']
        student.email = data['email']


        db.session.commit()
        
        return student, HTTPStatus.OK
    @jwt_required()
    def delete(self, student_id):
        '''deleting a particular student by id'''
        student = Students.get_by_id(student_id)

        student.delete()

        return {'message': 'student deleted successfully'}


@student_namespace.route('/<int:student_id>/score')
class GetScore(Resource):

    @student_namespace.marshal_list_with(score_model)
    def get(self, student_id):
        score = Score.query.filter_by(student_id=student_id).all()
        print (score)

        return score, HTTPStatus.OK

@student_namespace.route('/<int:student_id>/gpa')
class Calc_Gpa(Resource):
    @student_namespace.marshal_with(score_model)
    def post(self, student_id):
        courses= Score.query.filter_by(student_id=student_id).all()
        a=courses.score
        grade=[]
        points=[]
        for score in a:
            w= Getgrade(score)
            grade.append(w)
            
      
        course= Course.get_by_id(course_id = courses.course_id)
        credit_hr= course.course_weight
        unit=[]
        for  weight in credit_hr:
            y = weight
            unit.append(y)

        grade_point = grade*unit




        
        