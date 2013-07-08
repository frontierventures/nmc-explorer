from data import Domain
from data import db

import config


def reset():
    timestamp = config.createTimestamp()

    domain = Domain('active', timestamp, timestamp, 'hallo1', 'RESERVED', 114844, 'TEST', 'TEST', 'TEST')
    db.add(domain)
    print domain.name
    
    db.commit()

def reset1(name):
    domain = db.query(Domain).filter(Domain.name == name).first()
    rand1 = domain.rand2
    rand2 = domain.rand1
    print rand1, rand2

    domain.rand1 = rand1
    domain.rand2 = rand2
    print domain.rand1, domain.rand2
    db.commit()


reset()
