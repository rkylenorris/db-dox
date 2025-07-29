from ..db import Base, get_db
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class View(Base):
    __tablename__ = "views"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    schema_name = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    database_id = Column(String, ForeignKey("databases.id"), nullable=False)
    database = relationship("Database", back_populates="views")

    def __repr__(self):
        return f"<View(name={self.name}, schema_name={self.schema_name})>"