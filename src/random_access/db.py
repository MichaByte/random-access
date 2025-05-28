from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:////home/micha/Documents/random-access/database.db"  # sync SQLite URL

# connect_args needed for SQLite to allow multithreaded access
connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
