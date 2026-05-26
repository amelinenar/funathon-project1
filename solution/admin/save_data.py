# %% 
# Run it from bash with
# uv run solution/admin/save_data.py or
# uv run solution/admin/save_data.py intermediate_solutions/2_preprocessing.py
# default path is intermediate_solutions/2_preprocessing.py
import sys
import os

# Append parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import shutil
import subprocess
import argparse

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_script", nargs="?", help="Path to the input script", default="intermediate_solutions/2_preprocessing.py")
args = parser.parse_args()

input_script = args.input_script

# Debug
# input_script = "intermediate_solutions/2_preprocessing.py"

# Step 1: Copy script to temp.py
os.makedirs("temp", exist_ok=True)
shutil.copy(input_script, "temp/temp.py")

# Step 2: Add lines to temp script to dump model
with open("temp/temp.py", "a") as f:
    f.write("import sys\n")
    f.write("import os\n")
    f.write("sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n")
    f.write("from solution.utils import store_datasets\n")
    # f.write("datasets_to_store = {'df_zoubisou': df}\n")  # test
    f.write("datasets_to_store = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train.to_frame(), 'y_test': y_test.to_frame(), 'df': df}\n")
    f.write("store_datasets(datasets_to_store=datasets_to_store)\n")

# Step 3: Run temp.py
subprocess.run(["uv", "run", "temp/temp.py"])

# Step 4: Cleanup temporary files
print('Remove temporary files')
os.remove("temp/temp.py")

# %%
