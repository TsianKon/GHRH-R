#!/bin/bash

#set paths 
#smiles_dir=" "
sdf2d_dir=" "
sdf3d_dir=" "
rsalt_dir=" "
ph_dir=" "
pdbqt_dir=" "

for sdf2d in "$sdf2d_dir"/*.sdf; do
	
	#extract file name
	filename=$(basename $sdf2d .sdf)
	
	#convert from 2d sdf to 3d sdf
	obabel -isdf $sdf2d -osdf -O $sdf3d_dir/$filename.sdf --gen3D
	
	#convert from 3d sdf to 3d sdf -r
	obabel -isdf $sdf3d_dir/$filename.sdf -osdf -O $rsalt_dir/$filename.sdf -r
	
	#convert from 3d sdf -r to 3d sdf at ph=7
	obabel -isdf $rsalt_dir/$filename.sdf -osdf -O $ph_dir/$filename.sdf -p 7.0
	
	#convert from 3d sdf at ph=7 to pdbqt
	obabel -isdf $ph_dir/$filename.sdf -opdbqt -O $pdbqt_dir/$filename.pdbqt
	
done
