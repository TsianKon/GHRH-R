#!/bin/bash

docking_directory=" "

NR_CPUS=8
echo $NR_CPUS

function nrwait() {
 local nrwait_my_arg
 if [[ -z $1 ]] ; then
  nrwait_my_arg=2
 else
  nrwait_my_arg=$1
 fi

 while [[ $(jobs -p | wc -l) -ge $nrwait_my_arg ]] ; do
  sleep 0.01
 done
}

mkdir $docking_directory/Results

for R in Receptor_GHRHr_inactive/*.pdbqt; do
	
	#extract only receptor name
	r=`basename $R .pdbqt`
	mkdir $docking_directory/Results/$r
	
	#extract only ligand name
	for L in pdbqts_L1_L2/*.pdbqt;do
		l=`basename $L .pdbqt`
	
		#run docking
		/opt/vina --receptor Receptor_GHRHr_inactive/${r}.pdbqt --ligand pdbqts_L1_L2/${l}.pdbqt --config Config.txt --out $docking_directory/Results/${r}/${l}.pdbqt --log Log/${l}.log --cpu=4 --num_modes 1 & nrwait NR_CPUS				

	done
done




