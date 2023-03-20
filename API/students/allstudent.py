from flask import request
from flask_restx import Namespace,Resource, fields
from ..model.students import Students, Form,Score
from ..model.courses import Course
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from ..utils import db
from ..course.courses import score_model

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

@student_namespace.route('/<int:student_id>/scores')
class GetStudentScores(Resource):
    @student_namespace.marshal_with(score_model)
    def get(self,student_id):

        scores = Score.query.filter_by(student_id=student_id).all()
        
        
        if scores:
            return scores, HTTPStatus.OK
        return{'message':'No scores yet'}, HTTPStatus.FORBIDDEN
    



@student_namespace.route('/<int:student_id>/gpa')
class Calc_Gpa(Resource):
    @student_namespace.marshal_with(score_model)
    def post(self, student_id):
        scores= Score.query.filter_by(student_id=student_id).all()
        a = scores.score
        print (a)
        grade=[]
        points=[]
        for score in a:
            # s = list(score)
            grade.append(score)
            if grade>= 85:
                points.append(4.0)
            elif grade>=70:
                points.append(3.0)
            elif grade>= 60:
                points.append(2.0)
            elif grade>= 45:
                points.append(1.0)
            elif grade < 45:
                points.append(0.0)
            elif grade is None:
                points.append(0.0)
        
        grade_point = []
        total_grade_point =0.0
        course_ids = scores.course_id
        courses=[]
        unit =[]
        for c in course_ids:
            credit_hr = Course.get_by_id(c)
            courses.append(credit_hr.course_weight)
        total_credit_hrs=0.0
        for w in courses:
            total_credit_hrs+=w
            unit.append(w)
        for point in points:
            cal = point* unit
            grade_point.append(cal)


        for grade in grade_point:
            total_grade_point+=grade

        cgpa = total_grade_point/total_credit_hrs if  total_credit_hrs > 0 else 0


        return {'cgpa': cgpa}, HTTPStatus.OK


        
        

        