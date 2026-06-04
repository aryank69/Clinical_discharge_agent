from pydantic import BaseModel, Field
from typing import List, Optional


# -----------------------------
# Evidence Record
# -----------------------------

class Evidence(BaseModel):
    fact: str
    source_document: str
    page_number: int
    confidence: float = 1.0


# -----------------------------
# Medication Change
# -----------------------------

class MedicationChange(BaseModel):
    medication: str
    change_type: str
    reason: Optional[str] = None


# -----------------------------
# Conflict Record
# -----------------------------

class Conflict(BaseModel):
    field_name: str
    values: List[str]
    source_documents: List[str]


# -----------------------------
# Clinician Review Flag
# -----------------------------

class ReviewFlag(BaseModel):
    issue_type: str
    description: str
    severity: str = "medium"


# -----------------------------
# Patient State
# -----------------------------

class PatientState(BaseModel):

    patient_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None

    principal_diagnosis: Optional[str] = None
    secondary_diagnoses: List[str] = []

    hospital_course: Optional[str] = None

    procedures: List[str] = []

    allergies: List[str] = []

    admission_medications: List[str] = []
    discharge_medications: List[str] = []

    medication_changes: List[MedicationChange] = []

    follow_up_instructions: List[str] = []

    pending_results: List[str] = []

    discharge_condition: Optional[str] = None

    evidence_store: List[Evidence] = []

    conflicts: List[Conflict] = []

    review_flags: List[ReviewFlag] = []

    missing_fields: List[str] = []


# -----------------------------
# Final Discharge Summary
# -----------------------------

class DischargeSummary(BaseModel):

    patient_demographics: dict

    admission_date: Optional[str]
    discharge_date: Optional[str]

    principal_diagnosis: Optional[str]

    secondary_diagnoses: List[str]

    hospital_course: Optional[str]

    procedures: List[str]

    discharge_medications: List[str]

    medication_changes: List[MedicationChange]

    allergies: List[str]

    follow_up_instructions: List[str]

    pending_results: List[str]

    discharge_condition: Optional[str]

    conflicts: List[Conflict]

    review_flags: List[ReviewFlag]

    missing_information: List[str]