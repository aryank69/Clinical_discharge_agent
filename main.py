import os

from models.schemas import PatientState

from agents.extraction_agent import ExtractionAgent
from agents.planner_agent import PlannerAgent
from agents.reconciliation_agent import ReconciliationAgent
from agents.conflict_agent import ConflictAgent
from agents.summary_agent import SummaryAgent

from tools.drug_interaction_checker import (
    DrugInteractionChecker
)

from models.schemas import ReviewFlag


# ----------------------------------
# Load Patient Documents
# ----------------------------------
folder_path = "patient 2 (1).pdf"
def load_patient_documents(folder_path):

    pdfs = []

    if not os.path.exists(folder_path):

        print(
            f"Folder not found: {folder_path}"
        )

        return pdfs

    for file in os.listdir(folder_path):

        if file.lower().endswith(".pdf"):

            pdfs.append(
                os.path.join(
                    folder_path,
                    file
                )
            )

    return pdfs


# ----------------------------------
# Main Workflow
# ----------------------------------

def run_patient_pipeline(
    patient_folder
):

    print("\nStarting Patient Processing")

    state = PatientState()

    extraction_agent = ExtractionAgent()
    planner_agent = PlannerAgent(max_steps=25)

    reconciliation_agent = (
        ReconciliationAgent()
    )

    conflict_agent = (
        ConflictAgent()
    )

    interaction_tool = (
        DrugInteractionChecker()
    )

    summary_agent = (
        SummaryAgent()
    )

    # ----------------------------------
    # Step 1: Read Documents
    # ----------------------------------

    documents = load_patient_documents(
        patient_folder
    )

    if not documents:

        print("No PDFs found.")

        return

    print(
        f"\nFound {len(documents)} documents"
    )

    # ----------------------------------
    # Step 2: Extract Information
    # ----------------------------------

    for pdf in documents:

        print(
            f"\nProcessing: {pdf}"
        )

        state = (
            extraction_agent.process_pdf(
                pdf,
                state
            )
        )

    # ----------------------------------
    # Example Medication Lists
    # Replace with extracted data later
    # ----------------------------------

    state.admission_medications = [

        "Metformin",

        "Lisinopril"

    ]

    state.discharge_medications = [

        "Lisinopril",

        "Empagliflozin"

    ]

    # ----------------------------------
    # Step 3: Medication Reconciliation
    # ----------------------------------

    state = (
        reconciliation_agent.reconcile(
            state
        )
    )

    # ----------------------------------
    # Step 4: Drug Interaction Check
    # ----------------------------------

    interactions = (
        interaction_tool
        .check_interactions(
            state.discharge_medications
        )
    )

    for item in interactions:

        state.review_flags.append(

            ReviewFlag(

                issue_type=
                "Drug Interaction",

                severity=
                item["severity"],

                description=
                item["message"]
            )
        )

    # ----------------------------------
    # Step 5: Example Conflict Detection
    # ----------------------------------

    diagnoses = [

        "Pneumonia",

        "CHF Exacerbation"

    ]

    sources = [

        "Progress_Note.pdf",

        "Discharge_Order.pdf"

    ]

    state = (
        conflict_agent
        .check_diagnosis_conflict(
            diagnoses,
            sources,
            state
        )
    )

    # ----------------------------------
    # Step 6: Agent Planning Loop
    # ----------------------------------

    trace = planner_agent.run(
        state
    )

    # ----------------------------------
    # Step 7: Generate Summary
    # ----------------------------------

    summary = (
        summary_agent
        .generate_summary(
            state
        )
    )

    medication_changes = (
        summary_agent
        .medication_changes(
            state
        )
    )

    review_flags = (
        summary_agent
        .review_flags(
            state
        )
    )

    conflicts = (
        summary_agent
        .conflicts(
            state
        )
    )

    # ----------------------------------
    # Display Results
    # ----------------------------------

    print("\n" + "=" * 60)
    print("DISCHARGE SUMMARY DRAFT")
    print("=" * 60)

    for key, value in summary.items():

        print(f"\n{key}")

        print(value)

    print("\n" + "=" * 60)
    print("MEDICATION CHANGES")
    print("=" * 60)

    for item in medication_changes:

        print(item)

    print("\n" + "=" * 60)
    print("CONFLICTS")
    print("=" * 60)

    for item in conflicts:

        print(item)

    print("\n" + "=" * 60)
    print("REVIEW FLAGS")
    print("=" * 60)

    for item in review_flags:

        print(item)

    print("\n" + "=" * 60)
    print("AGENT TRACE")
    print("=" * 60)

    for item in trace:

        print(item)

    return state


# ----------------------------------
# Entry Point
# ----------------------------------

if __name__ == "__main__":

    PATIENT_FOLDER = (
        "data/patient_pdfs"
    )

    run_patient_pipeline(
        PATIENT_FOLDER
    )