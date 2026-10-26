
import uuid
import json
from pathlib import Path

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

# Store the database in the same folder as this file.
# This avoids accidentally creating databases in other folders.
DATABASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = DATABASE_DIR / "synthomed.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ============================================================
# PROJECT MODEL
# ============================================================

class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    name = Column(String, nullable=False)
    purpose = Column(String, default="Research")

    patients = relationship(
        "SyntheticPatient",
        back_populates="project",
        cascade="all, delete-orphan",
    )


# ============================================================
# SYNTHETIC PATIENT MODEL
# ============================================================

class SyntheticPatient(Base):
    __tablename__ = "synthetic_patients"

    id = Column(
        String,
        primary_key=True,
        default=lambda: f"SYN-{str(uuid.uuid4())[:8].upper()}",
    )

    project_id = Column(
        String,
        ForeignKey("projects.id"),
    )

    age = Column(Integer)
    sex = Column(String)
    severity = Column(String)

    conditions_json = Column(Text, default="[]")
    symptoms_json = Column(Text, default="[]")

    project = relationship(
        "Project",
        back_populates="patients",
    )

    @property
    def conditions(self):
        return json.loads(self.conditions_json or "[]")

    @conditions.setter
    def conditions(self, value):
        self.conditions_json = json.dumps(value)

    @property
    def symptoms(self):
        return json.loads(self.symptoms_json or "[]")

    @symptoms.setter
    def symptoms(self, value):
        self.symptoms_json = json.dumps(value)


# ============================================================
# HEALTH SUMMARY REPORT MODEL
# ============================================================

class HealthSummaryReport(Base):
    __tablename__ = "health_reports"

    id = Column(
        String,
        primary_key=True,
        default=lambda: f"REP-{str(uuid.uuid4())[:8].upper()}",
    )

    # Input data
    age = Column(Integer)
    demographics = Column(String)
    medical_history = Column(Text)
    current_symptoms = Column(Text)
    uploaded_reports_text = Column(Text)

    # Generated report output stored as JSON text
    report_json = Column(Text, default="{}")

    @property
    def report_data(self):
        return json.loads(self.report_json or "{}")

    @report_data.setter
    def report_data(self, value):
        self.report_json = json.dumps(value)


# ============================================================
# AUTOMATIC DATABASE INITIALIZATION
# ============================================================

# Create missing tables automatically.
# Existing database records are preserved.
Base.metadata.create_all(bind=engine)


# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():
    """
    Return a new SQLAlchemy database session.

    The caller is responsible for closing the session
    after completing its database operations.
    """
    return SessionLocal()
