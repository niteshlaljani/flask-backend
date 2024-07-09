from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

# Correct connection URL with driver specified
mysql_db_url = "mysql+mysqldb://root:MyNewPass@localhost:3306/tutorial"

# Create engine
engine = create_engine(mysql_db_url)

# Define Base
Base = declarative_base()

class User(Base):
    __tablename__ = "newusers"
    id = Column(Integer, primary_key = True)
    name = Column(String(100), nullable=False)
    number = Column(Integer, nullable=False)
    role = Column(String(50), nullable=False)
    email = Column(String(50), unique = True, nullable=False)
    password = Column(String(64), nullable=False)

# Create all tables
Base.metadata.create_all(engine)