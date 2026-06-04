from tools.pdf_reader import PDFReader
from tools.ocr_reader import OCRReader
from tools.clinical_extractor import ClinicalExtractor

from models.schemas import (
    PatientState,
    Evidence
)


class ExtractionAgent:

    def __init__(self):

        self.pdf_reader = PDFReader()

        self.ocr_reader = OCRReader()

        self.extractor = ClinicalExtractor()

    # --------------------------------
    # Read Document
    # --------------------------------
    def read_document(self, pdf_path):

        result = self.pdf_reader.read_pdf(pdf_path)

        if (
            result["status"] == "success"
            and len(result["text"].strip()) > 50
        ):
            return result

        print(f"OCR fallback triggered for {pdf_path}")

        return self.ocr_reader.read_pdf_with_ocr(
            pdf_path
        )

    # --------------------------------
    # Add Evidence
    # --------------------------------
    def add_evidence(
        self,
        state,
        fact,
        source_document,
        page_number=1
    ):

        evidence = Evidence(
            fact=fact,
            source_document=source_document,
            page_number=page_number,
            confidence=1.0
        )

        state.evidence_store.append(evidence)

    # --------------------------------
    # Process Single PDF
    # --------------------------------
    def process_pdf(
        self,
        pdf_path,
        state: PatientState
    ):

        result = self.read_document(pdf_path)

        if result["status"] != "success":

            state.review_flags.append(
                {
                    "issue_type": "Document Error",
                    "description":
                        f"Unable to read {pdf_path}",
                    "severity": "high"
                }
            )

            return state

        text = result["text"]

        # -------------------------
        # Demographics
        # -------------------------

        patient_name = \
            self.extractor.extract_patient_name(text)

        if patient_name and not state.patient_name:

            state.patient_name = patient_name

            self.add_evidence(
                state,
                patient_name,
                pdf_path
            )

        age = self.extractor.extract_age(text)

        if age and not state.age:

            state.age = age

            self.add_evidence(
                state,
                str(age),
                pdf_path
            )

        gender = self.extractor.extract_gender(text)

        if gender and not state.gender:

            state.gender = gender

            self.add_evidence(
                state,
                gender,
                pdf_path
            )

        # -------------------------
        # Dates
        # -------------------------

        admission_date = \
            self.extractor.extract_admission_date(text)

        if admission_date:

            state.admission_date = admission_date

            self.add_evidence(
                state,
                admission_date,
                pdf_path
            )

        discharge_date = \
            self.extractor.extract_discharge_date(text)

        if discharge_date:

            state.discharge_date = discharge_date

            self.add_evidence(
                state,
                discharge_date,
                pdf_path
            )

        # -------------------------
        # Diagnoses
        # -------------------------

        diagnoses = \
            self.extractor.extract_diagnoses(text)

        for diagnosis in diagnoses:

            if diagnosis not in state.secondary_diagnoses:

                state.secondary_diagnoses.append(
                    diagnosis
                )

                self.add_evidence(
                    state,
                    diagnosis,
                    pdf_path
                )

        if (
            diagnoses
            and not state.principal_diagnosis
        ):
            state.principal_diagnosis = diagnoses[0]

        # -------------------------
        # Allergies
        # -------------------------

        allergies = \
            self.extractor.extract_allergies(text)

        for allergy in allergies:

            if allergy not in state.allergies:

                state.allergies.append(allergy)

                self.add_evidence(
                    state,
                    allergy,
                    pdf_path
                )

        # -------------------------
        # Procedures
        # -------------------------

        procedures = \
            self.extractor.extract_procedures(text)

        for procedure in procedures:

            if procedure not in state.procedures:

                state.procedures.append(
                    procedure
                )

                self.add_evidence(
                    state,
                    procedure,
                    pdf_path
                )

        # -------------------------
        # Follow Up
        # -------------------------

        followups = \
            self.extractor.extract_followup(text)

        for item in followups:

            if item not in \
                    state.follow_up_instructions:

                state.follow_up_instructions.append(
                    item
                )

                self.add_evidence(
                    state,
                    item,
                    pdf_path
                )

        return state