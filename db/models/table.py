from ..db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Table(Base):
    __tablename__ = "tables"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    schema_id = Column(String, ForeignKey("schemas.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    schema = relationship("Schema", back_populates="tables")
    columns = relationship("TableColumn", back_populates="table")
    references = relationship("Reference", back_populates="table")

    def __repr__(self):
        return f"<Table(name={self.name})>"

class TableColumn(Base):
    __tablename__ = "columns"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    table_id = Column(String, ForeignKey("tables.id"), nullable=False)
    is_nullable = Column(String, nullable=False, default="YES")
    default_value = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    table = relationship("Table", back_populates="columns")

    def __repr__(self):
        return f"<TableColumn(name={self.name}, type={self.data_type})>"
