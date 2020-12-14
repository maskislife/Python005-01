import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import sys


class transfer_operation:

    Base = declarative_base()

    class USER_TABLE(Base):
        __tablename__ = 'users'
        uid = Column(Integer(), primary_key=True)
        name = Column(String(20), nullable=False)

    class PROPERTY_TABLE(Base):
        __tablename__ = 'properties'
        pid = Column(Integer(), primary_key=True)
        amount = Column(Float(), default=0)

    class TRANSFER_TABLE(Base):
        __tablename__ = 'operations'
        oid = Column(Integer(), primary_key=True)
        from_id = Column(Integer(), nullable=False)
        to_id = Column(Integer(), nullable=False)
        amount = Column(Float(), nullable=False)
        operation_time = Column(DateTime(), default=datetime.now)

    dbURL = 'mysql+pymysql://username:password@dn_addr:3306/dn_names?charset=utf8mb4'
    engine = create_engine(dbURL, encoding='utf-8')
    Base.metadata.create_all(engine)


    def get_session(self):
        SessionClass = sessionmaker(bind=self.engine)
        session = SessionClass()

        return session


    def update_properties(self, uid, amount):
        
        session = self.get_session()

        exist_amount=session.query(self.PROPERTY_TABLE.amount).filter(self.PROPERTY_TABLE.pid == uid).first()
        exist_amount = float(exist_amount[0])

        query = session.query(self.PROPERTY_TABLE)
        query = query.filter(self.PROPERTY_TABLE.pid == uid)
        query.update({self.PROPERTY_TABLE.amount: exist_amount+amount})

        session.commit()


    def add_users(self, users: dict):
        
        session = self.get_session()

        for uid, name in users.items():
            data = self.USER_TABLE(uid=uid, name=name)
            session.add(data)

        session.commit()


    def add_property(self, properties: dict):
        
        session = self.get_session()

        for uid, prope in properties.items():
            data = self.PROPERTY_TABLE(pid=uid, amount=prope)
            session.add(data)

        session.commit()

    
    def add_record_transfer(self, from_id, to_id, amount):
        
        session = self.get_session()

        from_amount=session.query(self.PROPERTY_TABLE.amount).filter(self.PROPERTY_TABLE.pid == from_id).first()

        from_amount = float(from_amount[0])

        if from_amount < amount:
            print('amount is not enough.')
            session.commit()
            sys.exit(1)

        query = session.query(self.PROPERTY_TABLE)
        query = query.filter(self.PROPERTY_TABLE.pid == from_id)
        query.update({self.PROPERTY_TABLE.amount: from_amount-amount})

        to_amount=session.query(self.PROPERTY_TABLE.amount).filter(self.PROPERTY_TABLE.pid == to_id).first()
        to_amount = float(to_amount[0]) + amount
        query = session.query(self.PROPERTY_TABLE)
        query = query.filter(self.PROPERTY_TABLE.pid == to_id)
        query.update({self.PROPERTY_TABLE.amount: to_amount})
        

        data = self.TRANSFER_TABLE(from_id=from_id, to_id=to_id, amount=amount)
        session.add(data)

        session.commit()


if __name__ == '__main__':
    
    db = transfer_operation()

    # user_add = {
    #     1 : 'zhang3',
    #     2 : 'li4'
    # }

    # properties_add = {
    #     1 : 80,
    #     2 : 0
    # }

    # db.add_users(user_add)
    # db.add_property(properties_add)
    # db.update_properties(1, 200)

    db.add_record_transfer(2, 1, 100.0)


