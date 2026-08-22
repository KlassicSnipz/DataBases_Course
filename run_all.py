import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Each script, in the exact order they must run
scripts = [
    "1_CSVtoPOSTGRES/run_stage_schema.py",
    "1_CSVtoPOSTGRES/load_data.py",
    "2_DataWarehouse/run_target_schema.py",
    "2_DataWarehouse/load_target.py",
    "3_SelectStatements/run_assignments.py",
    "4_StoredProcedures/run_stage1_procedures.py",
    "4_StoredProcedures/run_stage2_procedures.py",
    "5_PackagesExceptionHandling/run_stage5_procedures.py",
]

for script in scripts:
    script_path = os.path.join(BASE_DIR, script)
    print(f"\n{'='*60}")
    print(f"Running: {script}")
    print('='*60)

    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 0:
        print(f"\nFAILED at: {script}")
        print("Stopping. Fix the error above before continuing.")
        sys.exit(1)

print(f"\n{'='*60}")
print("All stages completed successfully.")
print('='*60)