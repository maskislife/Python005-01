import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class orm_demo:
    
    Base = declarative_base()

    class Person_table(Base):
        __tablename__ = 'person'
        pid = Column(Integer(), primary_key=True)
        name = Column(String(20), nullable=False)
        age = Column(Integer())
        birth = Column(DateTime(), default=datetime.now)
        gender = Column(String(4), nullable=False)
        education = Column(String(10))
        created_on = Column(DateTime(), default=datetime.now)
        updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

        def __repr__(self):
            return f"{self.pid} - {self.name} - {self.gender} - {self.education}"
    
    dbURL = 'mysql+pymysql://username:password@db_addr:3306/dn_name?charset=utf8mb4'
    engine = create_engine(dbURL, echo=True, encoding='utf-8')
    Base.metadata.create_all(engine)

    def get_session(self):
        SessionClass = sessionmaker(bind=self.engine)
        session = SessionClass()

        return session

    def conn_test(self):
        
        session = self.get_session()

        data = self.Person_table(name = "Jack", gender='male')
        session.add(data)
        session.flush()

        query = session.query(self.Person_table)
        for i in query:
            print(i)

        session.commit()

    def query_all(self):
        
        session = self.get_session()

        query = session.query(self.Person_table)
        for i in query:
            print(i)

        session.commit()



def insert_by_pymysql():
    db = pymysql.connect('db_addr', 'username', 'password', 'db_name')

    try:  
        with db.cursor() as cursor:
            sql = 'INSERT INTO person (pid, name, gender) VALUES (%s, %s, %s)'
            value = (
                (1000, "star trek", 'f'),
                (1004, "iron man", 'm'),
                (110, "bat man", 'm')
            )
            cursor.executemany(sql, value)
        db.commit()
        print(cursor.rowcount)
        
    except Exception as e:
        print(f'insert error, {e}')

    finally:
        db.close()

if __name__ == "__main__":
    test_object = orm_demo()

    # test_object.conn_test()
    # insert_by_pymysql()
    test_object.query_all()