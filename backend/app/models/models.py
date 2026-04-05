from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


disease_symptoms = Table(
    "disease_symptoms",
    Base.metadata,
    Column("disease_id", Integer, ForeignKey("diseases.id"), primary_key=True),
    Column("symptom_id", Integer, ForeignKey("symptoms.id"), primary_key=True),
)


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    causes = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    symptoms = relationship("Symptom", secondary=disease_symptoms, back_populates="diseases")
    treatments = relationship("Treatment", back_populates="disease", uselist=False)


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)

    diseases = relationship("Disease", secondary=disease_symptoms, back_populates="symptoms")


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=False, unique=True)
    immediate_action = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)

    disease = relationship("Disease", back_populates="treatments")
