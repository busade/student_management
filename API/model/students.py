from ..utils import db
from datetime import datetime




class Students(db.Model):
    __tablename__ ='students'
    id = db.Column(db. Integer, primary_key=True)
    name = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(40), unique = True, nullable = False)
    password_hash = db.Column(db.String(40), nullable = False)
    courses = db.relationship('Course',backref="students",lazy = True,secondary='forms')
    student = db.relationship('Students', backref='score', lazy = True, secondary= 'score')
    
    __mapper_args__ ={
        'polymorphic_identity':'students',
    }
    def __repr__(self):
        return f'<Students{self.id}>'
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    

    def save(self):
        db.session.add(self)
        db.session.commit()



    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Form(db.Model):
    __tablename__ ='forms'
    id = db.Column(db.Integer(), primary_key = True)
    student_id = db.Column(db.Integer(),db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    



    

    __mapper_args__ ={
        'polymorphic_identity':'forms',
    }

    def __repr__(self):
        return f"<Form{self.course_id}>"
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), nullable=False)
    form = db.relationship('Form', backref='score')

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    course = db.relationship('Course', backref='score',  lazy = True)
    score = db.Column(db.Integer, nullable=False)
    
    
    __mapper_args__ ={
        'polymorphic_identity':'score',
    }

    

    def __repr__(self):
        return f"<Score{self.id}>"
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

