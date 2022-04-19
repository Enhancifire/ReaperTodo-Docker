from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "postgresql://qgeuntlkoscyek:0faccf0da66f50acbe743f51deb10146cac62fcd54163e9a0fbb274c23afdf92@ec2-34-246-227-219.eu-west-1.compute.amazonaws.com:5432/d3gpbk693kb642"

engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        )

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()
