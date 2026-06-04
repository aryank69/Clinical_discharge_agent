from models.schemas import PatientState


class SummaryAgent:

    def __init__(self):
        pass

    # -----------------------------
    # Safe Value Helper
    # -----------------------------
    def safe_value(self, value):

        if value is None:
            return "Not documented"

        if isinstance(value, str):

            if value.strip() == "":
                return "Not documented"

        return value

    # -----------------------------
    # Safe List Helper
    # -----------------------------
    def safe_list(self, values):

        if not values:
            return ["Not documented"]

        return values

    # -----------------------------
    # Generate Summary
    # -----------------------------
    def generate_summary(
        self,
        state: PatientState
    ):

        summary = {

            "Patient Demographics": {
                "Name":
                    self.safe_value(
                        state.patient_name
                    ),
                "Age":
                    self.safe_value(
                        state.age
                    ),
                "Gender":
                    self.safe_value(
                        state.gender
                    )
            },

            "Admission Date":
                self.safe_value(
                    state.admission_date
                ),

            "Discharge Date":
                self.safe_value(
                    state.discharge_date
                ),

            "Principal Diagnosis":
                self.safe_value(
                    state.principal_diagnosis
                ),

            "Secondary Diagnoses":
                self.safe_list(
                    state.secondary_diagnoses
                ),

            "Hospital Course":
                self.safe_value(
                    state.hospital_course
                ),

            "Procedures":
                self.safe_list(
                    state.procedures
                ),

            "Discharge Medications":
                self.safe_list(
                    state.discharge_medications
                ),

            "Allergies":
                self.safe_list(
                    state.allergies
                ),

            "Follow-Up Instructions":
                self.safe_list(
                    state.follow_up_instructions
                ),

            "Pending Results":
                self.safe_list(
                    state.pending_results
                ),

            "Discharge Condition":
                self.safe_value(
                    state.discharge_condition
                )
        }

        return summary

    # -----------------------------
    # Medication Changes
    # -----------------------------
    def medication_changes(
        self,
        state: PatientState
    ):

        changes = []

        if not state.medication_changes:

            return ["No medication changes found"]

        for item in state.medication_changes:

            reason = (
                item.reason
                if item.reason
                else "Reason not documented"
            )

            changes.append(
                {
                    "Medication":
                    item.medication,

                    "Change":
                    item.change_type,

                    "Reason":
                    reason
                }
            )

        return changes

    # -----------------------------
    # Review Flags
    # -----------------------------
    def review_flags(
        self,
        state: PatientState
    ):

        flags = []

        for item in state.review_flags:

            flags.append(
                {
                    "Type":
                    item.issue_type,

                    "Severity":
                    item.severity,

                    "Description":
                    item.description
                }
            )

        return flags

    # -----------------------------
    # Conflicts
    # -----------------------------
    def conflicts(
        self,
        state: PatientState
    ):

        output = []

        for item in state.conflicts:

            output.append(
                {
                    "Field":
                    item.field_name,

                    "Values":
                    item.values,

                    "Sources":
                    item.source_documents
                }
            )

        return output