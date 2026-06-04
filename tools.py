from itertools import combinations


class DrugInteractionChecker:

    def __init__(self):

        # Mock interaction database
        self.interactions = {

            frozenset(
                ["warfarin", "aspirin"]
            ): {
                "severity": "high",
                "message":
                "Increased bleeding risk"
            },

            frozenset(
                ["lisinopril", "spironolactone"]
            ): {
                "severity": "medium",
                "message":
                "Risk of hyperkalemia"
            },

            frozenset(
                ["insulin", "metformin"]
            ): {
                "severity": "low",
                "message":
                "Monitor blood glucose levels"
            }
        }

    # -----------------------------
    # Check Interactions
    # -----------------------------
    def check_interactions(
        self,
        medication_list
    ):

        results = []

        meds = [
            med.lower()
            for med in medication_list
        ]

        for pair in combinations(meds, 2):

            key = frozenset(pair)

            if key in self.interactions:

                interaction_info = \
                    self.interactions[key]

                results.append({

                    "medications": list(pair),

                    "severity":
                    interaction_info["severity"],

                    "message":
                    interaction_info["message"]
                })

        return results