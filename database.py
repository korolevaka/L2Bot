from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///school.db')
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    parent_name = Column(String)
    student_name = Column(String)
    password = Column(String)
    grades = relationship("Grades", backref="parent")

class Grades(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'))
    math = Column(Integer)
    russian = Column(Integer)
    history = Column(Integer)
    literature = Column(Integer)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)




