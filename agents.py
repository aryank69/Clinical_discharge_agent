from models.schemas import PatientState


class PlannerAgent:

    def __init__(self, max_steps=25):

        self.max_steps = max_steps

        self.trace = []

    # --------------------------------
    # Check Missing Fields
    # --------------------------------
    def get_missing_fields(self, state: PatientState):

        missing = []

        if not state.patient_name:
            missing.append("patient_name")

        if not state.admission_date:
            missing.append("admission_date")

        if not state.discharge_date:
            missing.append("discharge_date")

        if not state.principal_diagnosis:
            missing.append("principal_diagnosis")

        if not state.discharge_condition:
            missing.append("discharge_condition")

        return missing

    # --------------------------------
    # Decide Next Action
    # --------------------------------
    def choose_next_action(self, state: PatientState):

        missing = self.get_missing_fields(state)

        if len(missing) == 0:
            return "GENERATE_SUMMARY"

        field = missing[0]

        action_map = {
            "patient_name": "SEARCH_PATIENT_NAME",
            "admission_date": "SEARCH_ADMISSION_DATE",
            "discharge_date": "SEARCH_DISCHARGE_DATE",
            "principal_diagnosis": "SEARCH_DIAGNOSIS",
            "discharge_condition": "SEARCH_DISCHARGE_CONDITION"
        }

        return action_map.get(field, "UNKNOWN")

    # --------------------------------
    # Add Trace
    # --------------------------------
    def add_trace(
        self,
        step,
        reasoning,
        action,
        result,
        next_decision
    ):

        self.trace.append(
            {
                "step": step,
                "reasoning": reasoning,
                "action": action,
                "result": result,
                "next_decision": next_decision
            }
        )

    # --------------------------------
    # Main Agent Loop
    # --------------------------------
    def run(self, state: PatientState):

        step = 1

        while step <= self.max_steps:

            missing = self.get_missing_fields(state)

            if len(missing) == 0:

                self.add_trace(
                    step,
                    "All required fields found",
                    "STOP",
                    "Patient record complete",
                    "Generate Summary"
                )

                break

            action = self.choose_next_action(state)

            self.add_trace(
                step,
                f"Missing fields: {missing}",
                action,
                "Awaiting execution",
                "Execute selected action"
            )

            step += 1

        if step > self.max_steps:

            self.add_trace(
                step,
                "Maximum step limit reached",
                "TERMINATE",
                "Agent stopped",
                "Flag incomplete record"
            )

        return self.trace