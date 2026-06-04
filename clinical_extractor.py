import re


class ClinicalExtractor:

    def __init__(self):
        pass

    # --------------------------------
    # Patient Name
    # --------------------------------
    def extract_patient_name(self, text):

        pattern = r"Patient Name[:\s]+([A-Za-z\s]+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

        return None

    # --------------------------------
    # Age
    # --------------------------------
    def extract_age(self, text):

        pattern = r"Age[:\s]+(\d+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return int(match.group(1))

        return None

    # --------------------------------
    # Gender
    # --------------------------------
    def extract_gender(self, text):

        pattern = r"(Male|Female)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

        return None

    # --------------------------------
    # Admission Date
    # --------------------------------
    def extract_admission_date(self, text):

        pattern = r"Admission Date[:\s]+([\d\/\-]+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

        return None

    # --------------------------------
    # Discharge Date
    # --------------------------------
    def extract_discharge_date(self, text):

        pattern = r"Discharge Date[:\s]+([\d\/\-]+)"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

        return None

    # --------------------------------
    # Diagnoses
    # --------------------------------
    def extract_diagnoses(self, text):

        diagnoses = []

        keywords = [
            "pneumonia",
            "sepsis",
            "hypertension",
            "diabetes",
            "heart failure",
            "copd",
            "asthma",
            "aki",
            "stroke",
            "covid"
        ]

        text_lower = text.lower()

        for diagnosis in keywords:

            if diagnosis in text_lower:
                diagnoses.append(diagnosis.title())

        return list(set(diagnoses))

    # --------------------------------
    # Allergies
    # --------------------------------
    def extract_allergies(self, text):

        allergies = []

        pattern = r"Allerg(?:y|ies)[:\s]+([^\n]+)"

        matches = re.findall(pattern, text, re.IGNORECASE)

        for allergy in matches:
            allergies.append(allergy.strip())

        return allergies

    # --------------------------------
    # Procedures
    # --------------------------------
    def extract_procedures(self, text):

        procedures = []

        procedure_keywords = [
            "bronchoscopy",
            "intubation",
            "catheterization",
            "angioplasty",
            "dialysis",
            "biopsy"
        ]

        text_lower = text.lower()

        for proc in procedure_keywords:

            if proc in text_lower:
                procedures.append(proc.title())

        return procedures

    # --------------------------------
    # Medications
    # --------------------------------
    def extract_medications(self, text):

        medications = []

        medication_keywords = [
            "metformin",
            "lisinopril",
            "aspirin",
            "atorvastatin",
            "insulin",
            "empagliflozin",
            "vancomycin",
            "ceftriaxone",
            "amoxicillin"
        ]

        text_lower = text.lower()

        for med in medication_keywords:

            if med in text_lower:
                medications.append(med.title())

        return medications

    # --------------------------------
    # Follow Up
    # --------------------------------
    def extract_followup(self, text):

        followups = []

        pattern = r"follow[- ]?up[:\s]+([^\n]+)"

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for item in matches:
            followups.append(item.strip())

        return followups