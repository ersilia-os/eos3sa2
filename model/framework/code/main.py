import pandas as pd
import csv
import os
import sys
import subprocess

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]


input_smiles_list = pd.read_csv(input_file, sep="\n", header=None)[0].tolist()

input_smiles = ["CCCCCCCCCC" for i in range(16)]


input_smiles.extend(input_smiles_list)
print(input_smiles)
print(len(input_smiles))

number_input = len(input_smiles)


activity_list = ["1.0" for i in range(number_input)]
activity_list[0:8] = ["0.0" for i in range(8)]
chembl_id_list = ["CHEMBL641707" for i in range(number_input)]
std_value_list = ["0.0" for i in range(number_input)]
log_std_value_list = ["1.0" for i in range(number_input)]
std_relation_list = ["=" for i in range(number_input)]
assay_type_list = ["B" for i in range(number_input)]


data = {
    "smiles": input_smiles,
    "activity": activity_list,
    "chembl_id": chembl_id_list,
    "standard_value": std_value_list,
    "log_standard_value": log_std_value_list,
    "standard_relation": std_relation_list,
    "assay_type": assay_type_list,
}

# Make data frame of above data
df = pd.DataFrame(data)

# append data frame to CSV file
root = os.path.dirname(os.path.abspath(__file__))

df.to_csv(
    os.path.join(root, "fs_mol/preprocessing/chembl/CHEMBL641707.csv"),
    mode="w",
    index=False,
    header=True,
)

# print message
print("Data appended successfully.")

cmd1 = "python {0}/fs_mol/preprocessing/featurize.py {0}/fs_mol/preprocessing/chembl datasets/fs-mol/test".format(
    root, root
)
cmd2 = "python {0}/fs_mol/protonet_test.py fs-mol-checkpoints/PN-Support64_best_validation.pt  {0}/datasets/fs-mol".format(
    root, root
)

import tempfile
import shutil


def run_command(cmd, quiet=None):
    if quiet is None:
        quiet = False
    if type(cmd) == str:
        if quiet:
            with open(os.devnull, "w") as fp:
                subprocess.Popen(
                    cmd, stdout=fp, stderr=fp, shell=True, env=os.environ
                ).wait()
        else:
            subprocess.Popen(cmd, shell=True, env=os.environ).wait()
    else:
        if quiet:
            subprocess.check_call(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=os.environ,
            )
        else:
            subprocess.check_call(cmd, env=os.environ)


def run_command_check_output(cmd):
    if type(cmd) is str:
        assert ">" not in cmd
        tmp_folder = tempfile.mkdtemp(prefix="ersilia-")
        tmp_file = os.path.join(tmp_folder, "out.txt")
        cmd = cmd + " > " + tmp_file
        with open(os.devnull, "w") as fp:
            subprocess.Popen(cmd, shell=True, stderr=fp, stdout=fp).wait()
        with open(tmp_file, "r") as f:
            result = f.read()
        shutil.rmtree(tmp_folder)
        return result
    else:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, env=os.environ)
        return result.stdout


def conda_prefix(is_base):
    o = run_command_check_output("which conda").rstrip()
    if o:
        o = os.path.abspath(os.path.join(o, "..", ".."))
        return o
    if is_base:
        o = run_command_check_output("echo $CONDA_PREFIX").rstrip()
        return o
    else:
        o = run_command_check_output("echo $CONDA_PREFIX_1").rstrip()
        return o


BASE = "base"


def activate_base():
    snippet = """
	source {0}/etc/profile.d/conda.sh
	conda activate {1}
	""".format(
        conda_prefix(False), BASE
    )
    return snippet


def run_commandlines_in_conda(commandlines):
    """
	Run commands in a given conda environment.
	"""
    environment = "fsmol"  # TODO: Update with eos identifier
    tmp_folder = tempfile.mkdtemp(prefix="ersilia-")
    tmp_script = os.path.join(tmp_folder, "script.sh")
    bash_script = activate_base()
    bash_script += """
	source {0}/etc/profile.d/conda.sh
	conda activate {1}
	conda env list
	{2}
	""".format(
        conda_prefix(True), environment, commandlines
    )
    with open(tmp_script, "w") as f:
        f.write(bash_script)

    tmp_folder = tempfile.mkdtemp(prefix="ersilia-")
    tmp_folder = root
    tmp_log = os.path.join(tmp_folder, "log.log")
    cmd = "bash {0} > {1} 2>&1".format(tmp_script, tmp_log)
    run_command(cmd)


run_commandlines_in_conda(cmd1)
run_commandlines_in_conda(cmd2)

embeddings = list(csv.reader(open(os.path.join(root, "embeddings.csv"))))

output_smiles = pd.read_csv(os.path.join(root, "output.txt"), sep="\n", header=None)[
    0
].tolist()

output_list = []
for s in input_smiles:
    row = [s]
    idx = output_smiles.index(s)
    row = row + embeddings[idx]
    output_list.append(row)

header = ["Emb" + str(i) for i in range(1, 513)]
header.insert(0, "smiles")
with open(output_file, "w") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
    wr.writerow(header)
    for e in output_list[16:]:
        wr.writerow(e)