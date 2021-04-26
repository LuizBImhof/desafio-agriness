from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bookStore.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Classe que representa os livros no banco de dados 

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(100),)
    author = Column(String(60))
    status = Column(Integer)
    reserveTime = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Clients")

    def save(self):
        db_session.add(self)
        db_session.commit()

# Classe que representa os livros no banco de dados 

class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))

    def save(self):
        db_session.add(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()