from ..db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Reference(Base):
    __tablename__ = "references"

    id = Column(String, primary_key=True, index=True)
    ref_type = Column(String, nullable=False)  # 'view' or 'stored_procedure'
    ref_id = Column(String, nullable=False)    # id of the view or stored procedure
    table_id = Column(String, ForeignKey("tables.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    table = relationship("Table", back_populates="references")
    stored_procedure = relationship("StoredProcedure", back_populates="references", foreign_keys=[ref_id], primaryjoin="Reference.ref_id==StoredProcedure.id", viewonly=True)

    def __repr__(self):
        return f"<Reference(ref_type={self.ref_type}, ref_id={self.ref_id}, table_id={self.table_id})>"
