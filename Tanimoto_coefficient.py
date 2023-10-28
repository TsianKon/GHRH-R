#Apply Tanimoto Similarity. Create a heatmap. 

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys
from rdkit import DataStructs
import pandas as pd
import os

# The folder containig the sdf files
sdf_folder = " "

# List Mol
mols = []
mol_names =[]
file_names= []

# Read sdf files and convert to Mol
for file in os.listdir(sdf_folder):
    if file.endswith(".sdf"):
        sdf_file = os.path.join(sdf_folder, file)
        suppl = Chem.SDMolSupplier(sdf_file)
        for mol in suppl:
            if mol is not None:
                mols.append(mol)
                mol_names.append(mol.GetProp("_Name"))
                file_names.append(file)

# Calculate MACCS for each compound
#fps = [MACCSkeys.GenMACCSKeys(mol) for mol in mols]

# Calculate RDKit fingerprint for each compound
fpgen = AllChem.GetRDKitFPGenerator(maxPath=2,fpSize=1024)
fps = [fpgen.GetFingerprint(mol) for mol in mols]

# Calculate tanimoto similarity for each pair
num_mols = len(mols)
num_mols
similarity_data=[]
for i in range(num_mols):
    #for j in range(i+1, num_mols):
    for j in range(i, num_mols):
        similarity = DataStructs.TanimotoSimilarity(fps[i], fps[j])
        similarity_data.append([file_names[i], file_names[j], similarity])
        if i != j:
            similarity_data.append([file_names[j], file_names[i], similarity])

df_similarity = pd.DataFrame(similarity_data, columns=["Compounds1", "Compounds2", "Tanimoto Similarity"])
df_similarity

# Lists to save the data
compounds = []
similarities = []

# Calculate mean for each compound
for compound in file_names:
    compound_similarities = []  # List for saving similarity values for each compound

    # Scan compared data
    for row in similarity_data:
        if compound in row[:2]:
            compound_similarities.append(row[2])
            compound_similarities
            len(compound_similarities)


    # Calculate mean for each compound
    avg_similarity = sum(compound_similarities) / len(compound_similarities)

    # Save data
    compounds.append(compound)
    similarities.append(avg_similarity)

# Dataframe from lists
df_avg_similarity = pd.DataFrame({"Compound": compounds, "Average Similarity": similarities})
df_avg_similarity
df_avg_similarity_sorted=df_avg_similarity.sort_values("Average Similarity")
df_avg_similarity_sorted.head(20)

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Create a pivot table for the heatmap
df_pivot = df_similarity.pivot_table(index="Compounds1", columns="Compounds2", values="Tanimoto Similarity")

# Generate a mask
mask = np.triu(np.ones_like(df_pivot, dtype=bool), k=1)

plt.figure(figsize=(55, 45))

# Create a heatmap using seaborn
ax = sns.heatmap(df_pivot, cmap="RdBu", mask=mask)

# Modify the axis labels to be bold and adjust the font size
#ax.set_xticklabels(ax.get_xticklabels(), weight='bold', fontsize=12)
#ax.set_yticklabels(ax.get_yticklabels(), weight='bold', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=20)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)

# Modify the axis and heatmap titles to be bold and adjust the font size
ax.set_xlabel(ax.get_xlabel(), weight='bold', fontsize=25)
ax.set_ylabel(ax.get_ylabel(), weight='bold', fontsize=25)
ax.set_title('Tanimoto Similarity HeatMap', weight='bold', fontsize=50)

plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')

# Display the heatmap
plt.show()
