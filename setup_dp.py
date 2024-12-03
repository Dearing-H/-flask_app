from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# Base class for ORM models
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    todos = relationship('ToDo', back_populates='user')

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)

# ToDo model
class ToDo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    done = Column(Boolean, default=False)
    due_date = Column(Date, nullable=True)  # Added due_date column
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='todos')

    # Method to mark task as done
    def mark_as_done(self):
        self.done = True

if __name__ == '__main__':
    # Database setup
    engine = create_engine('sqlite:///todo.db')
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")