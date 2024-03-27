import time
import sqlalchemy as db
from sqlalchemy import URL, Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from boot import *

api = ShoonyaApiPy()

# connection_string = URL.create(
#   'postgresql',
#   username='rishabhmaniyar',
#   password='90raWKtwUZBf',
#   host='ep-soft-unit-44308222.cloud.argon.aws.neon.build',
#   database='karthik',
# )

engine = db.create_engine(
    "postgresql://rishabhmaniyar:90raWKtwUZBf@ep-square-wildflower-40600057.us-east-2.aws.neon.tech/karthik?sslmode=require&options=endpoint=tight-dawn-32779436")

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users-new'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    key = Column(String, nullable=True)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, unique=True, nullable=True)


# Base.metadata.create_all(engine)
class userRepo:
    def findAllUsers(self):
        allUsers = session.query(User.username).all()
        return allUsers

    #
    # # Query a specific user by ID
    # user = session.query(User).filter_by(id=1).first()

    def findByUserName(self, username):
        user = session.query(User).filter_by(username=username).first()
        print("Fetching ", username)
        return user

    def saveNewUser(self, username, password, phone, key, token):
        print("Saving to DB for user ", username)
        # new_user = User(username='FA137726', password='Mali@01',phone='7021473220',token=api.generateTotp('6755I3PZ6L6GE2K7KBU2G2373Y2565H6'))
        new_user = User(username=username, password=password, phone=phone, key=key, token=token)
        # session.add(new_user)
        # session.commit()
