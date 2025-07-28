from ..db import Base, get_db
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Database(Base):
    __tablename__ = "databases"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    views = relationship("View", back_populates="database")
    schemas = relationship("Schema", back_populates="database")

    def __repr__(self):
        return f"<Database(name={self.name})>"
    

class Schema(Base):
    __tablename__ = "schemas"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    database_id = Column(String, ForeignKey("databases.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    database = relationship("Database", back_populates="schemas")

    def __repr__(self):
        return f"<Schema(name={self.name})>"