#Check the coordinates of the z-axis in a set of SDF files.
#Save in a text file the names of those SDF files where the z-axis is zero.

import os
from rdkit import Chem

# The folder containig the sdf files
path=r"C: "
files=os.listdir(path)

def check_z_coordinates(sdf_files, output_file):
    with open(output_file, 'w') as output:
        
        for sdf_file in sdf_files:
            suppl = Chem.SDMolSupplier(sdf_file)
            
            for mol in suppl:
                if mol is not None:
                    # Check 3rd column (coordinate z)
                    coords = mol.GetConformer().GetPositions()
                    z_coordinates = [coord[2] for coord in coords]
                    if all(coord == 0.000 for coord in z_coordinates):
                        # Save the name of the file to a txt file
                        output.write(os.path.basename(sdf_file) + '\n')

# Determine input folder with the sdf files
input_folder = r'C: '

# Find all sdf files at the input folder
sdf_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.sdf')]
#sdf_files

# Select specific number of sdf files (etc :10 selects first 10 files)
#sdf_files = sdf_files[:500]

# Determine txt output file
output_file = 'output.txt'

# Execute the check and save the result to a text file
check_z_coordinates(sdf_files, output_file)

