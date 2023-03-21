from flask import request
from flask_restx import Namespace,Resource, fields
from ..model.courses import Course
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..model.students import Students, Form, Score
from http import HTTPStatus
from ..utils import db






course_namespace = Namespace('course', description='namesapce for courses')




course_addition_model = course_namespace.model(
    'Add',{
        'id': fields.Integer(),
        'course_title':fields.String(required= True, Description= "name of the course"),
        'teacher':fields.String(required=True, Description = 'name of tutor'),
        'course_weight': fields.Integer(required = True, Description = ' The credit hours of the course')
    }
)
course_reg= course_namespace.model(
    "form",{
        'id': fields.Integer(),
        'student_id': fields.Integer( Description= 'id of the student'),
        'course_id':fields.Integer()
        
    }

)

score_model= course_namespace.model(
    "Scores",{
    'id': fields.Integer(),
    'form_id': fields.Integer(Description= 'id from the course registerd'),
    'student_id': fields.Integer(Description = 'student id '),
    'course_id': fields.Integer(Description='course id'),
    "score": fields.Integer(description= 'score of student in  the course')
    }
)





@course_namespace.route('/course_reg')
class  CourseReg(Resource):
    

    @course_namespace.expect(course_addition_model)
    @course_namespace.marshal_with(course_addition_model)
    @jwt_required()
    def post(self):
        ''' register courses'''
      

        data = course_namespace.payload

        new_course = Course(
            course_title = data['course_title'],
            teacher = data['teacher'],
            course_weight = data['course_weight']

        )
        

        new_course.save()

        return new_course, HTTPStatus.CREATED


    @course_namespace.marshal_with(course_addition_model)
    @jwt_required
    def get (self):
        '''get all courses from data base'''
        courses = Course.query.all()
        print(courses)

        if courses:
            return courses, HTTPStatus.ok
        return HTTPStatus.BAD_REQUEST




@course_namespace.route('/course_reg/<int:course_id>')
class Get_edit_delete(Resource):

    @course_namespace.marshal_with(course_addition_model)
    @jwt_required()
    def get (self, course_id):
        '''show a  particular course'''
        course = Course.get_by_id(course_id)
        return course, HTTPStatus.OK

    @course_namespace.expect(course_addition_model)
    @course_namespace.marshal_with(course_addition_model)
    @jwt_required()
    def put(self,course_id):
        '''edit course reg'''
        course_to_edit = Course.get_by_id(course_id)
        data = course_namespace.payload

        course_to_edit.course_title = data['course_title']
        course_to_edit.teacher = data['teacher']
        course_to_edit.course_weight = data['course_weight']

        db.session.commit()


        return course_to_edit,HTTPStatus.OK


    def delete(self, course_id):
        '''delete a registered course'''

        course_to_delete = Course.get_by_id(course_id)


        course_to_delete.delete()
        return {'message': "deleted successfully"}, HTTPStatus.OK





@course_namespace.route('/student/<int:student_id>/course/<int:course_id>')
class Course_Register(Resource):

    @course_namespace.marshal_with(course_reg)
    def post(self,student_id,course_id):
        ''' register student for a course'''
        

        new_course = Form(
            course_id = course_id,
            student_id = student_id

        )
        course_check = Course.get_by_id(id = course_id)
        if course_check:
            student_check = Students.get_by_id(id=student_id)
            if student_check :
                data_check = Form.query.filter_by(course_id=course_id,student_id=student_id).first()
                if data_check:
                    return{'message': 'course already registered'}, HTTPStatus.CONFLICT
                else:   
                    new_course.save()
                    return new_course, HTTPStatus.ACCEPTED
            else:
                return{'message': "stduent does not exist"}, HTTPStatus.BAD_GATEWAY
        else:
            return{'mesage': " course does not exist"}, HTTPStatus.BAD_REQUEST
        

    # def post(self,student_id):
    #     '''enter grades for a particular course '''




@course_namespace.route('/course/<int:course_id>/students')
class GetUpdateDelete(Resource):
    

    @course_namespace.marshal_list_with(course_reg)
    def get(self, course_id):
        ''' for retrieving a student that register for a particular course'''
    
    
        course = Form.query.filter_by(course_id = course_id).all()

        return course, HTTPStatus.OK
    




@course_namespace.route('/course/<int:course_id>/student/<int:student_id>')
class Get_edit_delete(Resource):

    @course_namespace.marshal_with(course_reg)
    # @jwt_required()
    def get (self, student_id, course_id):
        '''retrieve a student that registered for a course by id'''
        course = Form.query.filter_by(course_id =course_id, student_id=student_id).first()
        return course, HTTPStatus.OK

    @jwt_required
    def delete(self, student_id,course_id):
        '''delete a registered course for a student'''

        course_to_delete = Form.query.filter_by(course_id= course_id, student_id=student_id)


        course_to_delete.delete()
        return {'message': "deleted successfully"}, HTTPStatus.OK
    



@course_namespace.route('/student/<int:student_id>/course/<int:course_id>/grade')
class AddGradeToCourse(Resource):
    
    @course_namespace.marshal_with(score_model)
    @course_namespace.expect(score_model)
    @jwt_required()
    def post(self, student_id, course_id):
        ''' addition of student grades'''
        

        data = request.get_json()
        form_from_id = Form.query.filter_by(course_id=course_id, student_id= student_id).first()
        new_score= Score(
            form_id= form_from_id.id,
            student_id= student_id,
            course_id= course_id,
            score= data['score']


        )
        # check if student registered for the course
        if form_from_id:   
            check = Score.query.filter_by(course_id=course_id,student_id=student_id).first()
            # check if a score has been inputed for the student in the course before
            if check:
                return{'message': 'score already added'}, HTTPStatus.ALREADY_REPORTED
            else:
                # try:
                    new_score.save()
                    return new_score, HTTPStatus.ACCEPTED
                # except:
                    # return {'message': 'error adding score'}, HTTPStatus.BAD_GATEWAY
        return{'message': ' student didnt register for this course'}, HTTPStatus.NO_CONTENT
    
    @jwt_required()
    def put(self,course_id,student_id):
         ''' update a student score'''
         data = request.get_json()

         edit = Score.query.filter_by(course_id=course_id,student_id=student_id).first()

         edit.score= data['score']

         db.session.commit()
         return {'message': 'score updated'}, HTTPStatus.ACCEPTED






