#Scan the log files generated from molecular docking.
#Sort the docking scores and select the top 100 compounds with the best score. 

import os
import re

# The folder containing the log files
path = r"C: "
directory=os.listdir(path)
print(directory)

# New txt file name
output_file = "Top_100_compounds.txt"

# Create empty lists
ligands=[] 
affinities=[] 

# Open new file for writing
with open(output_file, "w") as f_out:
    
    # Examine each file in the folder
    for filename in directory:
        if filename.endswith(".log"):
            file_path = os.path.join(path, filename)
            ligands.append(filename)
            print("Ligand:"+filename)
            
            with open(file_path, "r") as f_in:
                lines = f_in.readlines()
                
                # Find first pose affinity value with re.search
                for i, line in enumerate(lines):
                    match = re.search(r"^\s*1\s+(\S+)", line)
                    if match:
                        affinity = match.group(1)
                        f_out.write(f"{filename}: {affinity}\n")
                        affinities.append(float(affinity))
                        print("Affinity: " + affinity)

with open(output_file, "w") as f_out:
    # Find best docking scores 
    top_affinities = sorted(set(affinities))[:100]  # With set remove duplicates values
    print("Top 100 scores:", str(top_affinities), "\n")

    affinity_dict = {}  # Dictionary to match affinities with compounds
    for affinity, ligand in zip(affinities, ligands):
        if affinity in affinity_dict:
            affinity_dict[affinity].append(ligand)
        else:
            affinity_dict[affinity] = [ligand]

    count = 0
    for affinity in top_affinities:
        ligands_with_affinity = affinity_dict[affinity]
        for ligand in ligands_with_affinity:
            print(f"Ligand {ligand}: {affinity}")
            f_out.write(f"Ligand {ligand}: {affinity}\n")
            count += 1
            if count == 100:
                break
        if count == 100:
            break


