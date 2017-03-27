## MDA_ligand_distance.py GUIDE:

This script will determine the distance traveled by a ligand (either specified by atom selection syntax or a list of atom indices) from a receptor (either specified by atom selection syntax or a list of atom indices) by utlizing the [MDAnalysis](http://www.mdanalysis.org) package

The current output is a plot showing distance between the COM of the ligand and COM of the receptor over the course of the trajectory and a csv containing distance per frame values. 


### REQUIREMENTS:

- Python2.7
- MDAnalysis
- ArgParse
- ConfigParser
- matplotlib
- pandas


(if these requirements conflict with your systems current package versions, I recommend creating a [conda virtual environment](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) in which to install the required packages)

### COMMAND LINE INPUT


To run script, use the following:

		python MD_ligand_distance.py <*your_config_file*.conf> <*output_file_name*.csv>

OPTIONAL ARGUMENTS

**-R**: will set script to take the text file of indices (specified in the config file) and use them to calculate the COM of the receptor

		python MD_ligand_distance.py <*your_config_file*.conf> <*output_file_name*.csv> -R
	
**-L**: will set script to take the text file of indices (specified in the config file) and use them to calculate the COM of the ligand

		python MD_ligand_distance.py <*your_config_file*.conf> <*output_file_name*.csv> -L

### CONFIG FILE

Example config file:

		[INPUT FILES]
		trajectory = MD_OA_2_1_run_1.dcd
		topology = OA-2-1.prmtop

		[RECEPTOR]
		resname = resname OCT
		indices = None

		[LIGAND]
		resname = resname MOL
		indices = None



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



