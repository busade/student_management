from ..utils import db






class Course(db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer(), primary_key= True)
    course_title = db.Column(db.String(100), nullable = False, unique = True)
    teacher= db.Column(db.String(100), nullable = False)
    course_weight= db.Column(db.Integer(), nullable= False)
    student_id = db.Column(db.Integer(), db.ForeignKey("students.id"))
    


    
    

    def __repr__(self) -> str:
        return f'<Course{self.id}>'
    

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)




    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()