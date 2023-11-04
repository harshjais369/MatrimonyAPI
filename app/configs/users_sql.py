from sqlalchemy import Column, String
from app.configs import BASE, SESSION

class User(BASE):
    __tablename__ = "users"
    mobile = Column(String(255), primary_key=True)
    name = Column(String(255))
    age = Column(String(255))
    gender = Column(String(255))
    location = Column(String(255))
    password = Column(String(255))

    def __init__(self, mobile, name, age, gender, location, password):
        self.mobile = mobile
        self.name = name
        self.age = age
        self.gender = gender
        self.location = location
        self.password = password

    def __repr__(self):
        return "<User %s>" % self.mobile

User.__table__.create(checkfirst=True, bind=SESSION.bind)

def addUser_sql(mobile, name, age, gender, location, password):
    try:
        adder = SESSION.query(User).get(mobile)
        if adder:
            SESSION.delete(adder)
        adder = User(str(mobile), str(name), str(age), str(gender), str(location), str(password))
        SESSION.add(adder)
        SESSION.commit()
        return True
    except Exception as e:
        print(e)
        SESSION.rollback()
        return False
    finally:
        SESSION.close()


def getAllUsers_sql():
    try:
        return SESSION.query(User).all()
    except Exception as e:
        print(e)
        SESSION.rollback()
        return None
    finally:
        SESSION.close()

def getUser_sql(mobile):
    try:
        return SESSION.query(User).get(mobile)
    except Exception as e:
        print(e)
        SESSION.rollback()
        return None
    finally:
        SESSION.close()

def deleteUser_sql(mobile):
    try:
        SESSION.query(User).filter(User.mobile == mobile).delete()
        SESSION.commit()
        return True
    except Exception as e:
        print(e)
        SESSION.rollback()
        return False
    finally:
        SESSION.close()
