## SEEKR Tutorial - How to prepare a job


#### For this tutorial, we will be attempting to prepare a k-on calculation for the protein trypsin and its natural substrate benzamidine

#### [1. Setting up the configuration file (.seekr)](#section1.0)

- [1.1 Set Project Details](#section1.1)
- [1.2 Set Program Path Information](#section1.2)
- [1.3 Ligand/Receptor Information](#section1.3)
- [1.4 NAMD TCL Script Parameters](#section1.4)
- [1.5 Active Site Using Milestones](#section1.5)
- [1.6 Ligand Positions/Orientations](#section1.6)
- [1.7 MD Parameters](#section1.7)
- [1.8 BD Parameters](#section1.8)
- [1.9 APBS Parameters](#section1.9)

#### [2. Running SEEKR](#section2.0)
- [2.1 Running seekr.py](#section2.1)
- [2.2 Anchor notation](#section2.2)

#### [3. Running the MD](#section3.0)
- [3.1 Minimizations](#section3.1)
- [3.2 Temperature Equilibrations](#section3.2)
- [3.3 Ensemble Equilbration (Umbrella Sampling)](#section3.3)
- [3.4 Forward Reverse Stage](#section3.4)

#### [4. Running the BD](#section4.0)
- [4.1 bd_top](#section4.1)
- [4.2 B_surface Simulation](#section4.2)
- [4.3 Outermost Milestone BD Simulation](#section4.3)
- [4.4 Consolidation of BD Trajectories](#section4.4)

#### [5. Analysis](#section5.0)
- [5.1 Running Analyze.py](#section5.1)
___

## <a name="section1.0"></a>1. Setting up the configuration file (.seekr)

___

First, ensure that you have installed SEEKR and all its required software (see README for dependencies). It is also recommended that you use the README/manual to familiarize yourself with the parameters that SEEKR uses. This tutorial also assumes that you are proficient in VMD.

I have prepared a SEEKR input file for Trypsin in the tutorial files (tryp.seekr), but we are going to try to build one from scratch using the TEMPLATE.seekr file.

Start by opening TEMPLATE.seekr in a text editor. To avoid overwriting the template file, save the file as something else, like "my_tryp.seekr".

In TEMPLATE.seekr, you need to replace all the values labeled with the value "SOMETHING" and even some of the others. Notice that lines after the hashtag '#' character are merely comments for your benefit, and are ignored by SEEKR.

We will go through one by one to change them to desired values:



#### <a name="section1.1"></a>1.1 Set Project details

---


![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_1.png?raw=true "Section 1.1")


        - set 'project_name' to 'tryp'
        
        - set 'root_dir' to a directory to construct the file tree. 
   
- It should be someplace you don't mind running simulations from and containing large trajectory files, like a scratch directory. I will be refering to this directory as trypsin_project_directory from now on.

        - set 'master_temperature' to '298'. 
        
- This is the temperature used for all simulations and calculations (except temperature equilibration)

        - set 'ens_equil_len' to '10000000'. 

- This will be how many timesteps the umbrella sampling equilibrations will be. Of course, the longer the better, but must be carefully balanced among the milestones according to available computing resources. Umbrella sampling equilibrations seem to be the greatest cost in these SEEKR calculations.

        - set 'number_of_ens_equil_frames' to '10000'. 
- This many frames will be written to the DCD files during the umbrella sampling equilibrations (assuming the runs finish). The 'dcdfreq' parameters are automatically set and so are other parameters elsewhere in the calculation.

        - set 'number_of_ens_equil_frames_skipped' to '3000'. 
- It's probably a good idea to skip some initial amount of time in the umbrella sampling simulations. This tells how many of the DCD frames to skip.

        - set 'extract_stride' to '1'. 
- This gives the stride between frames of the umbrella sampling simulations that will be run in the reversal stage. A stride of '1' means that all frames will be used. Using this and the parameters above, it means that 700 frames of the umbrella sampling will continue on to be used in a reversal stage. It seems to be good to aim in the order of high hundreds or low thousands when choosing how many reversals to run.

#### <a name="section1.2"></a>1.2 Set Program path information

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_2.png?raw=true "Section 1.2")

*If these paths are already specified in something like a bashrc, you can skip this step...*

These two are likely already aliased for Amarolab users:
        
        - browndye_bin_dir SOMETHING # the path to the browndye bin
        
        - inputgen_location /(your path)/src
        
        - apbs_executable SOMETHING

- #for Amarolab users: /soft/pdb2pqr/latest/src -- this should already be defined as an environment variable!


#### <a name="section1.3"></a>1.3 Ligand/Receptor Information

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_3.png?raw=true "Section 1.3")

        - set 'lig_pdb_filename' to point to 'benzamidine.pdb' in the tutorial folder. 
- Notice that this file is an ordinary pdb file of the ligand without any waters.
        
        - set 'lig_pqr_filename' to point to 'benzamidine.pqr' in the tutorial folder. 
- This is a pqr file of the ligand that contains charge and radius information for each of the atoms.
        
        - set 'rec_pdb_filename' to point to 'tryp_wet_lastframe.pdb' in the tutorial folder. 
- This is a pdb file of the receptor molecule that DOES contain waters and dissolved salt ions. I usually take this PDB file from the last frame of an apo MD simulation, so it has had time to relax, and the waters have arranged around it.
        
        - Leave 'rec_psf_filename' as it is. 
- Since we are not using a CHARMM forcefield, but AMBER, no PSF files are required.
        
        - set 'rec_dry_pdb_filename' to point to 'tryp_dry_lastframe.pdb' in the tutorial folder. 
- This is a pdb file of the receptor molecule that contains NO waters or dissolved ions. This is usually the same structure as 'rec_pdb_filename' with the solvent removed.
        
        - set 'rec_dry_pqr_filename' to point to 'tryp_dry_lastframe.pqr' in the tutorial folder. 
- This is usually the same 'rec_dry_pdb_filename.pdb' structure, but has been run through a tool like PDB2PQR or has been written as a PQR file straight from the trajectory that 'rec_pdb_filename' came from.

#### <a name="section1.4"></a>1.4 NAMD TCL script parameters

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_4.png?raw=true "Section 1.4")

        - set 'script_interval' to '5'. 
- This determines the stride between timesteps that the milestoning.tcl script is evaluated by NAMD. Therefore, a value of '5' will cause the milestones and the system to be evaluated every five timesteps in the MD simulations.
 
        - set 'abort_on_crossing' to 'True'. 
- If this is set to 'True', then forward phases will be stopped upon reaching another milestone. If set to 'False', then forward phases will continue past touching an adjacent milestone, and the simulations must be stopped using another method.

        - set 'ligrange' to 'auto' 
- This will automatically find the VMD-like selection of indeces that represent the ligand.

        - set 'lig_com_indeces' to 'auto'. 
- This is the same as 'ligrange' above, but represents the center of mass of the ligand during the MD simulations. This could be changed if it is thought that it might save computation time.

*MAYBE USE VMD TO DO THE FOLLOWING STEPS...*

        - set 'recrange' to 'auto'
- This will automatically find the VMD-like selection of indeces that represent the receptor.

        - set 'rec_com_indeces' to 'auto_ca'. 
- This will automatically find a range of all atoms that are alpha carbons in the receptor. The atoms with these indeces will be monitored during the simulation to determine the center of mass of the receptor. Notice the difference of this selection from 'recrange' above. This is because this list of indeces represents the alpha carbons of the receptor.

        - set 'recrot' to 'True'. 
- This is irrelevant for spherical milestones, but if planar milestones are being used, it should be 'True' if you want the planar milestones to rotate with the receptor. Otherwise, if you want the planar milestone to retain the same rotation, then set this to 'False'.

#### <a name="section1.5"></a>1.5 Active Site using milestones

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_5.png?raw=true "Section 1.5")

Now we are going to edit the parameters for the binding site in trypsin. This will require us to find some parameters by sight.

If one has a PDB structure with the ligand bound, then finding the binding site and associated residues are relatively easy tasks. For Trypsin and Benzamidine, one such structure is PDB structure: 3PTB

Open VMD and load PDB structure 3PTB. Color the protein white and view in a surface representation, then view "resname BEN" in licorice represenation. You should be able to clearly see the benzamidine ligand in the binding site.

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_16.png?raw=true "Section 1.5")

Now load the structure 'tryp_wet_lastframe.pdb' from the tutorial folder. Hide the waterbox, showing only the protein in a surface representation. Show residues 172 173 174 177 191 193 194 196 202 206 197 in a special color to highlight the binding site of trypsin. These will have different residue numbering than in the crystal structure because of the MD simulation done on 'tryp_wet_lastframe.pdb' previously. If desire, you can overlay the apo structure to the holo crystal structure using the MultiSeq tool in the VMD Extensions menu. I chose them because these are residues that appear to be interacting with the ligand, therefore, we can use the center of mass of these residues as the origin of our binding site.


![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_18.png?raw=true "Section 1.5")


Within the site1 block, set 'anchor_function' to 'concentric_spheres_atom'. This option means that our milestones will be concentric spheres centered around an atom selection.

        - set 'r' to '14.0'. 
- This means that the largest spherical milestone will extend with a radius of 14 Angstroms.
        
        - set 'r_low' to '2.0'. 
- This is the radius of the innermost milestone in Angstroms.

---

In VMD, make the 'tryp_wet_lastframe.pdb' file be the top molecule. 


In the tkconsole window, type: *set site [atomselect top "name CA and resid 172 173 174 177 191 193 194 196 202 206 197"]*


Then type: *measure center $site*


Take note of the resulting coordinates. They should be approximately: "-1.536, 13.860, 16.540"

        - Set 'x' to be '-1.536'. Set 'y' to be '13.860'. Set 'z' to be '16.540'.

Now, in the tkconsole window, type: *$site get serial*

The following numbers should be returned: '2479 2490 2500 2536 2719 2746 2770 2788 2795 2868 2927'.

        - set 'atomid' to be '2479 2490 2500 2536 2719 2746 2770 2788 2795 2868 2927'

Now we need to choose where to place the ligand on each milestone.

In the SEEKR/tools/setup direcory, there should be a script called 'moduseful.tcl'.


In the tkconsole window, type "source /path/to/moduseful.tcl". 


Then run the following command: *eye_vec "-1.536 13.860 16.540"*

---
*Tcl console*

![Tcl console](SEEKR-tutorial-files/seekr_tut_20.png?raw=true "Section 1.5a")

---

These are the coordinates for the center of binding site. The script should draw a thin line running from the binding site to where your eye was on the screen. Rotate the molecule to see the line. In order to obtain a good result for this vector, you will want to rotate your view in VMD so that you can see directly into the binding pocket. You can use the above command to draw another line, note the values for the vector. Don't worry about the magnitude of this line, SEEKR will automatically normalize it.


![Vector](SEEKR-tutorial-files/seekr_tut_15.png?raw=true "Section 1.5a")


Alternatively, on the VMD website, there is a page that contains all the scripts (http://www.ks.uiuc.edu/Research/vmd/script_library/). Download the script called 'eye_line', though some modifications will be needed to make it return the vector from the atom selection to your eye.

**In my case, it was '4.336 203.9 99.89'**

        - Set the 'vx', 'vy', 'vz' values to be the values you obtained. Or you can use my values on the line above.

- The parameters 'startvx', 'startvy', and 'startvz' allow more control over how the ligand is arranged along the milestones. This vector points from the origin to the location on the first milestone where to start the (vx, vy, vz) vector. If unsure how to modify this, then make 'startvx', 'startvy', and 'startvz' to be the same as 'vx', 'vy', and 'vz'.

        - Set the 'increment' value to be '2.0'. 
        
- This is the spacing, in Angstroms, between the milestones.

Alternatively, you can manually specify the placement of milestones using the
radius list option and provide a string of distances (e.g. 1 2 3 4 6 8 )

the option looks like this: 'radius_list 1 1.5 2 2.5 3 4 6 8 10 12 14'

NOTE: the radius lis option will override the increment option

**Our SEEKR setup for this system used 'radius_list 1 1.5 2 2.5 3 4 6 8 10 12 14'

#### <a name="section1.6"></a> 1.6 Ligand Positions/Orientations

---


![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_6.png?raw=true "Section 1.6")

We have finished defining the binding site of Trypsin, now we are filling out details of the MD portion of the calculation

        - set 'hedron' to 'single'. This is a future feature concerning rotational milestones.

        - set 'reject_clashes' to 'True'. 
- This will ensure that there are no steric clashes when the holo structure is generated for each milestone. If there is a steric clash, then no directory will be generated for that milestone, although it will still be monitored for crossing events.


#### <a name="section1.7"></a> 1.7 MD Parameters

---


![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_7.png?raw=true "Section 1.7")

        - set 'ff' to 'amber'.

        
#### LEAP

Now we need to fill out the LEAP commands. You can do this by hand by entering values into the 'leap_preload_commands' and 'leap_postload_commands' parameters, or by using 'sample_leap_file' and providing a sample LEAP script that SEEKR can use to parse the locations and specifics of generating a holo structure.

We will do the former. Write the following into the file:

    leap_preload_commands [
      source leaprc.ff14SB,
            source leaprc.gaff,
            set default FlexibleWater on,
            set default PBRadii mbondi2,
            loadoff /path/to/tutorial/Ca2.lib,
            loadoff /path/to/tutorial/benzamidine.lib,
            loadamberparams /path/to/tutorial/benzamidine.frcmod,
            WAT= T4E,
            HOH= T4E,
            loadAmberParams frcmod.ionsjc_tip4pew,
            loadAmberParams frcmod.tip4pew,
    
      ]




Of course change /path/to/tutorial to the true path to the tutorial files...

And write the following also:
      
      leap_postload_commands [
            bond holo.7.SG holo.137.SG,
            bond holo.25.SG holo.41.SG,
            bond holo.109.SG holo.210.SG,
            bond holo.116.SG holo.183.SG,
            bond holo.148.SG holo.162.SG,
            bond holo.173.SG holo.197.SG,
            charge holo,
            check holo,
          ]

This will create the necessary disulfide bonds for our system.


        - Set 'leap_program' to 'tleap'

#### MIN

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_8.png?raw=true "Section 1.7a")

We will want to run minimizations, so set 'min' to 'True'

        - Set 'min_constrained' to the list: ['ligand','receptor']. 
- We don't want either the ligand or receptor to move during minimizations: solvent only.

        - Set 'min_num_steps' to '5000'.

        - Set 'min_out_freq' to '500'.

        - Set 'min_ensemble' to 'nve'.

#### TEMP_EQUIL

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_9.png?raw=true "Section 1.7b")

        - Set 'temp_equil' to 'True'. 
- Temperature equilibrations heat up the solvent to allow the waters and ions to relax around the biomolecules. We ramp up the temperature and then let it fall back again.

        - Set 'temp_equil_constrained' to [ 'ligand', 'receptor' ]. 
- We don't want either the ligand or receptor to move during temperature equilibrations: solvent only.

        - Set 'temp_equil_peak_temp' to '350'. 
- This defines the peak temperature (in K) to heat the simulation to.

        - Set 'temp_equil_temp_increment' to '10'. 
- How many degrees K per increment while rising temperature.

        - Set 'temp_equil_num_steps' to '1000'. 
- This is the number of steps per temperature increment

        - Set 'temp_equil_ensemble' to 'nvt'. 


#### ENS_EQUIL

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_10.png?raw=true "Section 1.7c")

        - Set 'ens_equil' to 'True'. 
- This is whether we will run constrained runs for ensemble equilibrations (umbrella sampling) in order to generate the equilibrium distribution.

        - Set 'ens_equil_colvars' to 'True'. 
- Whether collective variables should be imposed between the ligand and the receptor. This is the umbrella sampling.

        - Set 'ens_equil_colvar_sel' to [ 'ligand', 'receptor' ]. 
- This is a list of what parts of the system will have collective variables imposed. Options include 'ligand', 'receptor', 'water', 'relative' (for relative colvars between ligand/receptor), or a list of all indeces in pdb to be constrained

        - Set 'ens_equil_colvar_force' to '90.0' # kcal/mol
        
        - Set 'ens_equil_colvarstrajfrequency' to '100000'

        - Set 'ens_equil_colvarsrestartfrequency' to '100000'

        - Set 'ens_equil_colvar_ligand_indeces' to '3234 to 3251'. 
- These are the indeces that represent the ligand.

        - Set 'ens_equil_colvar_receptor_indeces' to '2475 2487 2498 2756 2798 2909'. 
- These are the indeces that represent the receptor.

        - Set 'ens_equil_ensemble' to 'nvt'

#### FORWARD and REVERSAL

---

![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_11.png?raw=true "Section 1.7d")

        - Set 'fwd_rev_ensemble' to 'nve'. Forward and reverse phases should be run in the NVE ensemble.

        - Set 'fwd_rev_type' to 'protein'. 
- This can be 'protein' or 'membrane', and merely affects the parameters used.

        - Set 'fwd_rev_dcdfreq' to '1000'. 
- This is how frequently to write the DCD files.

        -Set 'fwd_rev_restart_freq' to '1000'. 
- This is how frequently to write the restart files.

        - Set 'fwd_rev_run_freq' to '1000'. 
- This is how freqently to check whether a simulation terminated because a milestone was crossed.

        - Set 'fwd_rev_launches_per_config' to '1'. 
-This is the number of times per config to reinitialize the velocities to obtain more crossing events in the reversal stage. This can be increased to observe more reversal runs that succeed in crossing to the forward stage.

        - Set 'fwd_rev_frame_chunk_size' to '1700'. 
- This specifies how many frames to submit to the replicas at any one time. If this number is too large (>10000), then memory overflows can occur.


#### <a name="section1.8"></a> 1.8 BD Parameters

---


![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_12.png?raw=true "Section 1.8")


Now we will fill out details concerning the BD portion of the simulation

        - Set 'bd_threads' to '10'. 
- This represents the number of cores to use for the BD calculation and will vary based on your computer. You can change this to better fit your computer by determining how many cores your computer has (check the hardware under About My Computer to see how many processors you have) and input that number here.

        - Set 'bd_prods_per_anchor' to '1000000'. 
- This is the number of BD simulations to run per surface that they are started on.

        - Set 'bd_rec_pqr_filename' to 'tryp_dry_lastframe.pqr'.

#### <a name="section1.9"></a> 1.9 APBS Parameters

---


![Setting up the configuration file](SEEKR-tutorial-files/seekr_tut_13.png?raw=true "Section 1.9")


Last, we will fill out details concerning the electrostatics calculations used in the BD simulations. We are using a 20mM NaCl solution, and the nonlinear PBE for the calculations.

        - Set 'ion1rad' to '1.6700'. 
- This is the radius of the anion: Cl-.

        - Set 'ion2rad' to '1.5700'. 
- This is the radius of the cation: Na+.

        - Set 'ion1conc' to '0.02'. 
- The concentration of Cl-.

        - Set 'ion2conc' to '0.02'. 
- The concentration of Na+.
        
        - Set 'lpbe_npbe' to 'npbe' 
- To use the nonlinear PB equation solver. The nonlinear PBE may be useful for situations of high salt concentration or highly charged molecules like DNA.

        - Set 'inputgen_fadd' to '130.0'. 
- The number of angstroms to add to each side of the molecule in the electrostatic grid.

        - Set 'inputgen_cfac' to '5.0'. This adjusts the size of the coarse grid calculation in APBS.

Now save the file as "trypsin.seekr".

___

## <a name="section2.0"></a>2. Running SEEKR

___


#### <a name="section2.1"></a>2.1 Running seekr.py

---


Now we are finished with the preparations of the input file. Run the SEEKR program using the following command:

    python /path/to/SEEKR/bin/seekr.py trypsin.seekr

The program may take take many minutes or even an hour to complete. Once finished, you will see the folder 'tryp' in the directory you provided as 'root_dir', called something along the lines as trypsin_project_directory.

The tryp/ directory contains a filetree that SEEKR constructed. Inside, you will see several folders that begin with the word 'anchor' and a folder that is called 'b_surface'. Additionally, you will see a milestones.xml file, which the program uses to represent the milestone surfaces, and will be used for analysis in the end. There are also several '.pkl' files. The '.pkl' files are python "pickle" files that allow subsequent runs of seekr.py to be completed more quickly and easily, but you will never interact with them.

#### <a name="section2.2"></a> 2.2 Anchor Notation

---

The directories that begin with "anchor" are designed to be informative. The format looks like: "anchor_A_B_C_D_E_F_G" The numbers correspond to:

- A: The index of the milestone (can be positional or rotational)
- B: The index of the positional milestone
- C: The site ID for multiple binding locations on the receptor
- D: The X-coordinate of the anchor (location where the center-of-mass of the ligand was placed)
- E: The Y-coordinate of the anchor (location where the center-of-mass of the ligand was placed)
- F: The Z-coordinate of the anchor (location where the center-of-mass of the ligand was placed)
- G: The index of the rotational milestone. (Until this feature is fully developed, it is likely only to be zero.)

Each anchor directory corresponds to a milestone surface. Since we set the 'reject_clashes' option to 'True', it is likely that some anchors were not created because the ligand had a steric clash with the receptor. This is highly dependent on the vector generated by 'eye_vec'. The missing anchors can always be added later, but for now we will continue with just those created here.

Look inside one of the directories that begins with 'anchor'. In these directories, you will see at least one subdirectory "md", and in the outermost one you'll see the subdirectory 'bd'. Look inside the "md" subdirectory. You will see the directories: "building", "min", "temp_equil", "ens_equil", and "fwd_rev" directories. You'll also see a "holo_wet.pdb" structure. Take a look at the structure in VMD and verify that it looks OK. 

Look inside the "building" directory. Inside will be a LEAP file used to prepare a PRMTOP and INPCRD file, as well as LEAP output and a PDB file generated by LEAP. The LEAP output file can be useful for debugging problems running LEAP in other projects.

Back up into the "md" folder. The other directories will be useful for running preparations of this particular milestone for simulation.

Now back up two directories and enter the "b_surface" directory. Inside here are a number of files that will be used for BD simulations starting at this anchor.

___

## <a name="section3.0"></a> 3. Running the MD

___

Back up a directory so that you can see all the anchor folders.

NOTE: It is VERY IMPORTANT in cases when you will be using SEEKR for real research, that you verify the validity of the NAMD input files with an expert in Molecular Dynamics.

#### <a name="section3.1"></a> 3.1 MINIMIZATIONS:

Run the following command to minimize the holo structures:

    for i in anchor_*/md/min; do echo "now running minimizations on anchor $i"; cd $i; namd2 min1.namd > min1.out; cd ../../..; done

It may take several minutes or an hour. This command goes into each of the anchors' minimization folders and uses namd to minimize the solvent molecules for those systems.

It's worth it to load the PRMTOP (found in your trypsin_project_directory as /anchor_*/md/building/holo.prmtop) and minimization DCD files into VMD to observe that all went according to plan. The number of frames found in the DCD files are determined by the input file.


#### <a name="section3.2"></a> 3.2 TEMPERATURE EQUILIBRATIONS:


Now that the minimizations are complete, we want to heat up the solvent slowly and then let it slowly cool to allow the waters to arrange themselves and relax around the ligand and receptor. 

First, look inside one of the anchor directories, then past the md/ directory, and into the temp_equil/ directory. Note the numbering of the temp_equil .namd scripts. They should be numbered from 1 to 13. We will run each of these in succession.

To do this, change directory to be in your trypsin_project_directory and run the following command:

        for i in anchor_*/md/temp_equil; do echo $i; cd $i; for f in {1..13}; do echo "  $f"; namd2 +idlepoll +p4 temp_equil$f.namd >    temp_equil$f.out; done; cd ../../..; done

This will run the temperature equilibrations, it should finish within an hour or so. I recommend loading the DCD files into VMD to verify that everything is still OK after the temperature equilibrations. The length of the equilibration is determined by the input file.

To save time loading all of the DCD files into VMD, use the following command in the VMD TkConsole after loading the /anchor_*/md/building/holo.parm7  found in trypsin_project_directory and opening vmd in the temp_equil directory:
SEEKR Tutorial - How to prepare a job

        for {set i 1} {$i <= 13} {incr i} {mol addfile temp_equil$i.dcd}


#### <a name="section3.3"></a> 3.3 ENSEMBLE EQUILIBRATIONS (Umbrella Sampling):

Back up the filetree until you are above the trypsin_project_directory. Enter the following command to create a tarball:

        tar -czf tryp_pre_equil.tgz trypsin_project_directory/

Once that command is done, use scp or sftp to transfer to your scratch directory on Stampede and unpack using the following command:

        tar -xzf tryp_pre_equil.tgz

Calculations in this section are typically performed on a supercomputer. This
tutorial assumes you will be running on the TACC Stampede supercomputer.

We will first compile a special version of NAMD needed for the fwd_rev
phase...

How to compile for Stampede:
A tarball of the NAMD source code is located in the SEEKR/namd directory.

Create a directory named, say, namd_compile. Then 'cd' into it. From here, run:

        cp SEEKR/namd/NAMD_CVS-2015-11-02_Source.tar.gz .

Then unpack it with tar -xzf NAMD_CVS-2015-11-02_Source.tar.gz

Now you will copy some code files from the same folder into your source folder
using these commands:

        cp /(path to)/SEEKR/namd/gauss.C NAMD_CVS-2015-11-02_Source/src/.
        cp /(path to)/SEEKR/namd/eigeng.c NAMD_CVS-2015-11-02_Source/src/.
        cp /(path to)/SEEKR/namd/namd/TclCommands.C NAMD_CVS-2015-11-02_Source/src/.
        cp /(path to)/SEEKR/namd/TclVec.C NAMD_CVS-2015-11-02_Source/src/.

This will overwrite the existing TclVec.C and TclCommands.C source files
because SEEKR requires adaptations of the NAMD code. Trust us... we know what
we're doing ;)

Next, copy over the script that you will use to build charmrun, which NAMD
needs to run on a parallel system like Stampede. Do so using this command:

        cp /(path to)/SEEKR/namd/build_namd.bash ./

View the script if you want, and modify the variables at the top as you see
fit. The $WORKDIR variable is where the program is downloaded and compiled.
Then the $HOMEDIR variable is actually where the final program will be placed.
Run using this command:

        bash build_namd.bash

This script will probably run for a long time (about an hour). In fact, if it
stops instantly, check the output for errors because it probably didn't work,
even if it says it worked. If you have trouble, try copying the charm-6.7.0
tarball from the SEEKR/namd directory:

        cp /(path to)/SEEKR/namd/charm-6.7.0.tar $WORK/charm-6.7.0-verbs-linux-x86_64-iccstatic

Then run this command:

        tar -xf $WORK/charm-6.7.0-verbs-linux-x86_64-iccstatic/charm-6.7.0.tar

Then go into the build_namd.bash script and remove or comment out the line that begins with 'wget'. Then re-run the script.

Now we need to compile NAMD. The default way to do this is pretty well described in the notes.txt file in the NAMD directory. But we will give
detailed instructions here.

The following commands download and install TCL and FFTW libraries:
  
        (cd to NAMD_2.10_Source if you're not already there)
        wget http://www.ks.uiuc.edu/Research/namd/libraries/fftw-linux-x86_64.tar.gz
        tar xzf fftw-linux-x86_64.tar.gz
        mv linux-x86_64 fftw
        wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64.tar.gz
        wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64-threaded.tar.gz
        tar xzf tcl8.5.9-linux-x86_64.tar.gz
        tar xzf tcl8.5.9-linux-x86_64-threaded.tar.gz
        mv tcl8.5.9-linux-x86_64 tcl
        mv tcl8.5.9-linux-x86_64-threaded tcl-threaded

Edit the Make.charm configuration file:
  
        vi Make.charm

Once inside, set CHARMBASE to full path to charm. In our case, this is the
directory: ${HOME}/charm-6.7.0

       CHARMBASE = ${HOME}/charm-6.7.0

Set up build directory and compile:
                
       ./config Linux-x86_64-g++ --charm-arch verbs-linux-x86_64-iccstatic
       cd Linux-x86_64-g++
       make

This last step is likely to take a long time. (about 15 minutes)

Copy the mpiexec program from the namd directory to a location of your choice.
Your home directory is fine:

      cp /(path to)/SEEKR/namd/mpiexec $HOME

The program that we use to control jobs on the supercomputer is called control.py. Make sure that control.py exists in your home directory on Stampede.

the program we will use to run calculations on the supercomputer, control.py, requires you to define the environment variables "NAMD_SEEKR", "CHARM_SEEKR", and "MPIEXEC" that reflect the paths to the software you just compiled.

To do this, in your home directory, edit the .bashrc file: "vi .bashrc" 
 
add the following lines, changing the path to reflect where the special build is installed
                
        export NAMD_SEEKR="/path/to/new/compile/NAMD_CVS-2015-11-02_Source/Linux-x86_64-g++/namd2"
        export CHARM_SEEKR="/path/to/new/compile/NAMD_CVS-2015-11-02_Source/Linux-x86_64-g++/charmrun"
        export MPIEXEC="/path/to/mpiexec"
        export INPUTGEN="/path/to/inputgen.py"


#### Running Ensemble Equilibrations:

Now, cd into the project directory you just unpacked on Stampede. I like to test everything by running a short simulation for one of the anchors to ensure that it was prepared properly.

To prepare the anchor files for umbrella sampling, determine the lowest anchor number (in this case, it's four), type the following command:

        python ~/control.py submit 4 ens_equil 

Even though the output says that it's executing an sbatch command, it actually is not beacuse Stampede does not allow this. It is always a good idea to check that it did not submit, though, by typing 
"showq -u"

We will have to submit it manually later.

The control.py program takes commands according to the following template:

        python ~/control.py action anchor stage

The "action" category can take several possible arguments:

submit, resubmit, check, prep, etc...

The "anchor" category takes a comma-separated series of anchor indeces to launch. These correspond to the first number in the the directories in the tryp/ folder. Commas delineate numbers and dashes allow one to specify ranges of numbers. One may also use the "all" keyword to launch all the anchors in this directory.

The "stage" category specifies which stage to launch. So far, only "ens_equil" and "fwd_rev" are allowed stages.  

Now cd in anchor 4, then md/, then ens_equil/. You will see four files. Two colvar files that specify information about the umbrella sampling, a NAMD input file, and a submission file, perhaps named something like: "ens_equil256_1.submit"

Open the submission file using vim or vi.

Change the amount of time to run from 48 hours to only 10 minutes. You can do this by finding an SBATCH argument near the top of the file specified by "-t" and contains the text: "48:00:00". Change this text to "00:10:00", which corresponds to ten minutes. (This can also be done with the '-t' argument to control.py)

Change the number of processors from 256 to 128. This can also be done using the -p argument in control.py

Finally, you will need to add your account information after the -A option.
This can also be done using the -a argument in control.py

You can also change other information about the submission at this time if you desire. You can also change the NAMD file if desired, although SEEKR should have specified everything properly.

Now submit the umbrella sampling job:

        sbatch ens_equil256_1.submit

Of course, if your submission script has a different name, you'll have to change the command above. Assuming that all is well with your stampede allocation and the submission file, the job should be submitted to the queue. You can check on it by typing: "showq -u". 


Your job will only run for 10 minutes, but a true umbrella sampling job should run for much more time. In fact, you will likely need to run several different submissions. To resubmit the jobs, the "resubmit" argument for control.py can be used. Use the following command to see the progress of your umbrella sampling:

        python ~/control.py check all ens_equil

This will print out a series of information about each of the anchors, and the number of timesteps that have been completed for the umbrella sampling. If the "last timestep" output is less than the number of timesteps wanted for the umbrella sampling, you would use a command similar to the following:

        python ~/control.py resubmit 4 ens_equil

Of course, you might use a different anchor index. You will need to enter the ens_equil/ directory again, find the submission file named something like: "ens_equil256_2.submit", modify any parameters, and then submit it using sbatch.


#### <a name="section3.4"></a> 3.4 FWD REV STAGE:

**Note: This tutorial is currently written to reflect the commands you would execute while ssh'd into your own Stampede account from TACC.**

Once the umbrella sampling stage is complete, it's time to start the fwd_rev stage. This is the trickiest of all. You can control this stage using control.py also.

Obtain the milestoning.tcl file from the SEEKR directory and place it into the trypsin_project_directory you determined in your input file.

Then, you will need to obtain or compile a special build of NAMD2 as well as a program called Charm++.

Submitting the fwd_rev stage:

Since earlier in the tutorial, you probably only ran the umbrella sampling simulations for 10 minutes, which is far shorter than you actually would. For this reason, you don't have the whole umbrella sampling simulation. You can run these for the required time, but you should probably obtain the completed trajectories that we have already prepared. However, these must be carefully placed in their appropriate directories with the appropriate names.

You will need access to an AmaroLab computer like Honolua for this commands. Log into an 

###Fix file location###
scp /extra/banzai/alheynem/seekr/tryp_dcds/tryp_ens_equil_trajectories.tgz your_username_here@stampede.tacc.utexas.edu:/scratch/directory/on/stampede

Of course, replace /scratch/directory/on/stampede with the true path (Log into Stampede and type: "echo $SCRATCH" to see a path to this), along with your_username_here replaced with your Stampede username.

Now, with a terminal open in Stampede, 'cd' to your SEEKR project root directory, where you can see all the directories that begin with "anchor". 

Now run the following commands (NOTE: You may run into errors if SEEKR didn't create one of the anchor files, like anchor_3. If so, then just skip those commands):

                tar -xzf $SCRATCH/tryp_ens_equil_trajectories.tgz
                mv anchor_3_ens_equil_0_1.restart.xsc ens_equil_0_1.restart.xsc; mv ens_equil_0_1.restart.xsc anchor_3_*/md/ens_equil/
                mv anchor_3_ens_equil_0_1.dcd ens_equil_0_1.dcd; mv ens_equil_0_1.dcd anchor_3_*/md/ens_equil/
                mv anchor_3_ens_equil_0_2.dcd ens_equil_0_2.dcd; mv ens_equil_0_2.dcd anchor_3_*/md/ens_equil/
                mv anchor_3_ens_equil_0_3.dcd ens_equil_0_3.dcd; mv ens_equil_0_3.dcd anchor_3_*/md/ens_equil/
                mv anchor_4_ens_equil_0_1.restart.xsc ens_equil_0_1.restart.xsc; mv ens_equil_0_1.restart.xsc anchor_4_*/md/ens_equil/
                mv anchor_4_ens_equil_0_1.dcd ens_equil_0_1.dcd; mv ens_equil_0_1.dcd anchor_4_*/md/ens_equil/
                mv anchor_4_ens_equil_0_2.dcd ens_equil_0_2.dcd; mv ens_equil_0_2.dcd anchor_4_*/md/ens_equil/
                mv anchor_4_ens_equil_0_3.dcd ens_equil_0_3.dcd; mv ens_equil_0_3.dcd anchor_4_*/md/ens_equil/
                mv anchor_4_ens_equil_0_4.dcd ens_equil_0_4.dcd; mv ens_equil_0_4.dcd anchor_4_*/md/ens_equil/
                mv anchor_5_ens_equil_0_1.restart.xsc ens_equil_0_1.restart.xsc; mv ens_equil_0_1.restart.xsc anchor_5_*/md/ens_equil/
                mv anchor_5_ens_equil_0_1.dcd ens_equil_0_1.dcd; mv ens_equil_0_1.dcd anchor_5_*/md/ens_equil/
                mv anchor_5_ens_equil_0_2.dcd ens_equil_0_2.dcd; mv ens_equil_0_2.dcd anchor_5_*/md/ens_equil/
                mv anchor_5_ens_equil_0_3.dcd ens_equil_0_3.dcd; mv ens_equil_0_3.dcd anchor_5_*/md/ens_equil/
                mv anchor_5_ens_equil_0_4.dcd ens_equil_0_4.dcd; mv ens_equil_0_4.dcd anchor_5_*/md/ens_equil/
                mv anchor_5_ens_equil_0_5.dcd ens_equil_0_5.dcd; mv ens_equil_0_5.dcd anchor_5_*/md/ens_equil/
                mv anchor_6_ens_equil_0_1.restart.xsc ens_equil_0_1.restart.xsc; mv ens_equil_0_1.restart.xsc anchor_6_*/md/ens_equil/
                mv anchor_6_ens_equil_0_1.dcd ens_equil_0_1.dcd; mv ens_equil_0_1.dcd anchor_6_*/md/ens_equil/
                mv anchor_6_ens_equil_0_2.dcd ens_equil_0_2.dcd; mv ens_equil_0_2.dcd anchor_6_*/md/ens_equil/

(Optional) Now you can 'rm $SCRATCH/tryp_ens_equil_trajectories.tgz' to delete the tarball there.

If you have no access to an Amaro Lab computer, you may have to run the umbrella sampling trajectories yourself for a longer period of time.

(Optional) If you have it installed on Stampede, use the 'catdcd' command to see how long the trajectories are. However, if you don't have catdcd on Stampede, it's difficult to use the catdcd command. Download catdcd, place it in your work directory on Stampede, and edit your .bashrc file in your home directory using vim or vi. Add this line in your .bashrc file:

        alias catdcd="$WORK/catdcd"

Once you have edited and saved your .bashrc file, source it so the changes can be implemented with the command done within your home directory:

source .bashrc

Then use the following command:

        catdcd anchor_3*/md/ens_equil/ens_equil_0_*.dcd

This will show you how many frames are in each trajectory file. This command was just applied to anchor 3, try it with the other anchors.

Now, it's time to submit the forward-reverse stage job. Run the following command using control.py:
**From the trypsin_project_directory

        python /path/to/SEEKR/bin/control.py -p 64 -nr 16 -t 12:00:00 submit all fwd_rev

Of course, replace /path/to/control.py with the path to the control.py SEEKR program. The '-p' option will request 64 processors. If you find that you can perform calculations more efficiently with a different number of processors, you can change this number. The '-nr' option defines the number of replicas, that is, the number of concurrent fwd-rev stage jobs running at once. The number of processors per replica is equal to (number of processors / number of replicas). The '-t' option specifies the amount of time to run in hours:minutes:seconds. Run control.py with the '-h' option to see additional arguments that are available.

Change directory into one of the anchors, say anchor 4. Go through the 'md' and 'fwd_rev' directories. From here, you can view the '.namd' and '.submit' files to see how the fwd-rev stage is run. There is a lot of special code in the '.namd' files that helps in the assignment of simulations to replicas, as well as switching between reverse and forward stages, starting up where jobs are left off etc.

Submit the jobs using the following command:

       sbatch fwd_rev64_1.submit

The job will run for up to 12 hours. You can check on the job the same way using the 'showq -u' or 'qstat' commands.

___

## <a name="section4.0"></a> 4. Running the BD: 

___

This stage can be run independantly of any of the MD stages, and it can fill time during the supercomputer simulations of the previous sections.

#### <a name="section4.1"></a> 4.1 bd_top

BD is run starting from both the b-surface, and also the outermost milestone(s). 

**We need to start with the b-surface**, because the starting distribution on the outermost milestone(s) will be determined from this. From the trypsin system root directory, 'cd' into the directory named 'b_surface'. Open 'input.xml' to make sure that the parameters are OK (For instance, make sure that the Debye length and dielectric values are good). From here, run the BrownDye program 'bd_top' on the input file.

        bd_top input.xml

This will generate all the auxiliary files needed to run Brownian Dynamics simulations starting from the b-surface. It's worth it to open the file that ends with '-simulation.xml', which contains all the simulation parameters, and it's worth it to check out and make sure that everything looks good from your point of view. It's probably also worth it to open the rxns.xml file, view which atom indeces are involved in the reactions, then highlight these atoms on the 'bd_receptor_dry_pqr.pqr' file in a molecular viewer like VMD. For instance, if the <atoms> tag in the rxns.xml file has the pair of atoms '3233' and '19', then we can load 'bd_receptor_dry_pqr.pqr' into VMD, then create a new representation with the selection "serial 3233" and draw using VDW to see where the atom is located. We can do the same with the ligand pqr file, and highlight atom number 19.

#### <a name="section4.2"></a> 4.2 B_surface simulation

Now we can run the simulations:

        nam_simulation bd_receptor_dry_pqr-0_0_site1_30.1_33.4_27.8_0-simulation.xml

Your '-simulation.xml' file may be named slightly differently from what is above.

Once the simulations are done (probably a couple of hours later), you can view the results by opening the 'results.xml' file in a text editor like vi or gedit. You can find the number of reactions in the <n> tag. The larger this number is, the better. Hopefully at least 100, but preferably thousands.


#### <a name="section4.3"></a> 4.3 Outermost Milestone BD Simulation

**Now, we are going to run the BD simulations for the outermost milestone** 'cd' back one, then go into the outermost anchor (anchor 6). Go into the 'bd' directory this time. Unlike the b-surface simulation, where you run all your simulations from random places on the b-surface, this anchor will have all its BD simulations started from points where this milestone was crossed in the bd simulations. Therefore, there will be many many separate runs of BrownDye starting from different conformations.


To do this, we must extract frames from the b-surface trajectories. Make sure you specified the 'empty_pqrxml_path' parameter in your SEEKR input file. If no path has been specified, the default path is *./empty.pqrxml* There is a copy of 'empty.pqrxml' inside the SEEKR program directory.

Run the following command:

        python extract_bd_frames.py

This will run for an hour or more, extracting structures from the last frames of the b-surface simulations. Once complete, you can look inside the trajs/ folder to see the output of the script. There will be a thousand ligand .pqr files, and a thousand .xml files that characterize additional information about the last frame of each of these trajectories. These .pqr files are technically called 'encounter complexes'. We won't be using the .xml files, but we will be using the .pqr files in later steps.


So, inside the bd/ directory of anchor 6, run the following command: (NOTE TO SASHA AND BEN: Download the latest version of BrownDye to make sure that this works right.)

        python make_fhpd.py

This takes all of the encounter complexes that we made in the last step, and prepares and then runs a BD simulation for each of them. This calculation will take awhile, probably several hours. (**This took me several days with 16 cores with the increased dx map. We should probably suggest this on the supercomputer)

#### <a name="section4.4"></a> 4.4 Consolidation of BD trajectories

When that is done, run the next script:


        python fhpd_consolidate.py

This will descend into every directory of fhpd/ and pull out the results files, combining them together into a single results.xml file which will be used in the final analysis step of the system.

___

 ## <a name="section5.0"></a> 5. Analysis:

___

This is the final stage of a SEEKR calculation. We will use the analyse.py program included with SEEKR. To familiarize yourself with the input of this script, run the following command:

#### <a name="section5.1"></a> 5.1 Running Analyze.py

        python analyze.py -h

This will print out a help file for this analyze.py and can give a hint about how to run it.

Argument breakdown:

We will be using the '--on' option because we are computing the k-on.
The '-m' argument points to the 'milestones.xml' file in the bottom of the trypsin system directory, alongside all the anchor folders.
The '--skip' and '--number' arguments are used in the computation of error margins for the k-on value. Since this is found using a Monte-Carlo algorithm that samples matrices, '--number' tells how many matrices to sample to get the error bars, and '--skip' is how many trial matrices to skip between extractions of actual matrices to compute the error margins for. The numerical value '1000' is good for both of these arguments.

Analyze.py is likely to run for several hours, depending on the '--skip' and '--number' values.

The following command will run analyze.py for an on rate calculation, sampling 100 error matrices, with the zeroth anchor as the sink state:

        python /path/to/seekr/analyze.py -m milestones.xml -b 0 --skip 100 --number 1000 --on

When complete, it will print out a k-on and other useful information.

To see the free energy profile, run the following command:

        python ~/seekr/analyze.py --free_energy -m milestones.xml -b 0 --skip 100 --number 1000

Use the -h option of analyze.py for help and to wiew all the possible commands.

For further analysis, there is a collection of scripts in the SEEKR/tools/analysis/ directory.


