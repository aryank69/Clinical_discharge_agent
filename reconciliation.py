from models.schemas import (
    MedicationChange,
    ReviewFlag,
    PatientState
)


class ReconciliationAgent:

    def __init__(self):
        pass

    # --------------------------------
    # Compare Medication Lists
    # --------------------------------
    def reconcile(
        self,
        state: PatientState
    ):

        admission_set = set(
            med.lower()
            for med in state.admission_medications
        )

        discharge_set = set(
            med.lower()
            for med in state.discharge_medications
        )

        # -----------------------------
        # Added Medications
        # -----------------------------

        added = discharge_set - admission_set

        # -----------------------------
        # Stopped Medications
        # -----------------------------

        stopped = admission_set - discharge_set

        # -----------------------------
        # Continued Medications
        # -----------------------------

        continued = admission_set.intersection(
            discharge_set
        )

        # -----------------------------
        # Process Added
        # -----------------------------

        for med in added:

            change = MedicationChange(
                medication=med.title(),
                change_type="Added",
                reason=None
            )

            state.medication_changes.append(
                change
            )

            state.review_flags.append(
                ReviewFlag(
                    issue_type="Medication Change",
                    description=
                    f"{med.title()} added without documented reason",
                    severity="medium"
                )
            )

        # -----------------------------
        # Process Stopped
        # -----------------------------

        for med in stopped:

            change = MedicationChange(
                medication=med.title(),
                change_type="Stopped",
                reason=None
            )

            state.medication_changes.append(
                change
            )

            state.review_flags.append(
                ReviewFlag(
                    issue_type="Medication Change",
                    description=
                    f"{med.title()} stopped without documented reason",
                    severity="high"
                )
            )

        # -----------------------------
        # Process Continued
        # -----------------------------

        for med in continued:

            change = MedicationChange(
                medication=med.title(),
                change_type="Continued",
                reason=None
            )

            state.medication_changes.append(
                change
            )

        return state