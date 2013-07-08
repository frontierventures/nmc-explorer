from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

import config

engine = create_engine('sqlite:///database/domains.db', echo=False)
Session = sessionmaker(bind=engine)
db = Session()


Base = declarative_base()


class Domain(Base):
    __tablename__ = "domains"

    id = Column(Integer, primary_key=True)
    status = Column(String)
    createTimestamp = Column(String)
    updateTimestamp = Column(String)
    name = Column(String)
    record = Column(String)
    blocks = Column(String)
    rand1 = Column(String)
    rand2 = Column(String)
    confirmation = Column(String)

    def __init__(self, status, createTimestamp, updateTimestamp, name, record, blocks, rand1, rand2, confirmation): 
        self.status = status
        self.createTimestamp = createTimestamp
        self.updateTimestamp = updateTimestamp
        self.name = name
        self.record = record
        self.blocks = blocks
        self.rand1 = rand1
        self.rand2 = rand2
        self.confirmation = confirmation


def reset():
    Base.metadata.create_all(engine)

    timestamp = config.createTimestamp()

    domain = Domain('active', timestamp, timestamp, 'domain1', 'RESERVED', 10, 'xxx', 'xxx', 'xxx')
    db.add(domain)
    db.commit()
