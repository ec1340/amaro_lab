## MDA_COM_CODE GUIDE:

This script will determine the distance traveled by a ligand (either specified by atom selection syntax or a list of atom indices) from a receptor (either specified by atom selection syntax or a list of atom indices)

The current output is a plot showing distance between the COM of the ligand and COM of the receptor over the course of the trajectory


REQUIREMENTS:

Python2.7
MDAnalysis
ArgParse
ConfigParser
matplotlib

### COMMAND LINE INPUT


To run script, use the following:

python MD_ligand_distance.py *your_config_file*.conf* *output_file_name*.dat 

OPTIONAL ARGUMENTS

**-R**: will set script to take the text file of indices (specified in the config file) and use them to calculate the COM of the receptor

**-L**: will set script to take the text file of indices (specified in the config file) and use them to calculate the COM of the ligand


### CONFIG FILE


- trajectory file		

  - can be .prmtop or .psf file

- topology 		

  - .dcd trajectory file

- resname			

   - atom_selection is made using selection syntax used by MDAnalysis 
   - Some selection terms:
				- protein, backbone, nucleic, nucleicbackbone
				- segid 'seg-name' (ex. segid DMPC)
				- resid 'residue-number:range' (ex. resid 1:5)						
        - resname 'residue-name' (resname LYS]
- indices 
  - list of index numbers for atoms selected to calculate COM stored in a txt file using a ',' delimiter
  - 
  - 

## NOTE

- the output file feature does not work yet - rather it will output a graph of distance traveled 
AN OUTPUT FILE NAME STILL NEEDS TO BE SPECIFIED HOWEVER

- The indices selection method is not yet working
