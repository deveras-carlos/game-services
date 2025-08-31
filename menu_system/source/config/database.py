# /config/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

class Database:
    _db_session = None
    _engine = None

    @staticmethod
    def get_db():
        """Get the global database session."""
        if not Database._db_session:
            Database._db_session = sessionmaker(bind=Database.get_engine())()
        return Database._db_session

    @staticmethod
    def get_engine():
        """Create or retrieve the database engine."""
        if not Database._engine:
            DATABASE_URL = 'sqlite:///game_settings.db'
            Database._engine = create_engine(DATABASE_URL, echo=True)
            Base.metadata.create_all(Database._engine)  # Create tables if they don't exist
        return Database._engine

    @staticmethod
    def init_db():
        """Initialize the database and create tables."""
        if not Database._engine:
            Database.get_engine()  # Initialize engine if it hasn't been created yet
        Base.metadata.create_all(Database._engine)  # Ensure tables exist