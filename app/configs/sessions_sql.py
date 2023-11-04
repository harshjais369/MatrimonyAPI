from sqlalchemy import Column, String
from app.configs import BASE, SESSION

class Session(BASE):
    __tablename__ = "sessions"
    token = Column(String(255), primary_key=True)
    mobile = Column(String(255))

    def __init__(self, token, mobile):
        self.token = token
        self.mobile = mobile

    def __repr__(self):
        return "<Session %s>" % self.token
    
Session.__table__.create(checkfirst=True, bind=SESSION.bind)

def addSession_sql(token, mobile):
    try:
        adder = SESSION.query(Session).get(token)
        if adder:
            SESSION.delete(adder)
        adder = Session(str(token), str(mobile))
        SESSION.add(adder)
        SESSION.commit()
        return True
    except Exception as e:
        print(e)
        SESSION.rollback()
        return False
    finally:
        SESSION.close()

def getSession_sql(token):
    try:
        return SESSION.query(Session).get(token)
    except Exception as e:
        print(e)
        SESSION.rollback()
        return None
    finally:
        SESSION.close()

def deleteSession_sql(token):
    try:
        adder = SESSION.query(Session).get(token)
        if not adder:
            return False
        SESSION.delete(adder)
        SESSION.commit()
        return True
    except Exception as e:
        print(e)
        SESSION.rollback()
        return False
    finally:
        SESSION.close()

def generateToken():
    # TODO: Generate a random string of 32 characters
    pass