from ..db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class StoredProcedure(Base):
    __tablename__ = "stored_procedures"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    schema_id = Column(String, ForeignKey("schemas.id"), nullable=False)
    definition = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    schema = relationship("Schema", back_populates="stored_procedures")
    parameters = relationship("StoredProcedureParameter", back_populates="stored_procedure")
    references = relationship("Reference", back_populates="stored_procedure")

    def __repr__(self):
        return f"<StoredProcedure(name={self.name})>"

class StoredProcedureParameter(Base):
    __tablename__ = "stored_procedure_parameters"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)
    stored_procedure_id = Column(String, ForeignKey("stored_procedures.id"), nullable=False)
    ordinal_position = Column(String, nullable=False)
    is_output = Column(String, nullable=False, default="NO")

    # Relationships
    stored_procedure = relationship("StoredProcedure", back_populates="parameters")

    def __repr__(self):
        return f"<StoredProcedureParameter(name={self.name}, type={self.data_type})>"
