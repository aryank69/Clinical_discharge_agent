from models.schemas import (
    Conflict,
    ReviewFlag,
    PatientState
)


class ConflictAgent:

    def __init__(self):
        pass

    # --------------------------------
    # Generic Conflict Check
    # --------------------------------
    def check_conflict(
        self,
        field_name,
        values,
        source_documents,
        state: PatientState
    ):

        unique_values = list(
            set(
                value.strip()
                for value in values
                if value
            )
        )

        if len(unique_values) > 1:

            conflict = Conflict(
                field_name=field_name,
                values=unique_values,
                source_documents=source_documents
            )

            state.conflicts.append(conflict)

            state.review_flags.append(
                ReviewFlag(
                    issue_type="Conflict",
                    description=
                    f"Conflicting values detected for {field_name}",
                    severity="high"
                )
            )

        return state

    # --------------------------------
    # Diagnosis Conflict
    # --------------------------------
    def check_diagnosis_conflict(
        self,
        diagnoses,
        source_documents,
        state
    ):

        return self.check_conflict(
            field_name="Diagnosis",
            values=diagnoses,
            source_documents=source_documents,
            state=state
        )

    # --------------------------------
    # Allergy Conflict
    # --------------------------------
    def check_allergy_conflict(
        self,
        allergies,
        source_documents,
        state
    ):

        return self.check_conflict(
            field_name="Allergies",
            values=allergies,
            source_documents=source_documents,
            state=state
        )

    # --------------------------------
    # Admission Date Conflict
    # --------------------------------
    def check_admission_date_conflict(
        self,
        dates,
        source_documents,
        state
    ):

        return self.check_conflict(
            field_name="Admission Date",
            values=dates,
            source_documents=source_documents,
            state=state
        )

    # --------------------------------
    # Discharge Date Conflict
    # --------------------------------
    def check_discharge_date_conflict(
        self,
        dates,
        source_documents,
        state
    ):

        return self.check_conflict(
            field_name="Discharge Date",
            values=dates,
            source_documents=source_documents,
            state=state
        )