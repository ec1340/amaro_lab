#------------------------------------------------------------
### WORKFLOW
#------------------------------------------------------------

#--1-Parse command line arguements

#--2-Parse config arguments

#--3-Set config parameters to MDA

#--4-Calculate Distance between COM of ligand and receptor 
    #--AND plot it


#------------------------------------------------------------

#NOTE - CURRENT SCRIPT WILL ONLY RUN IN PYTHON2.7


#IMPORT LIBRARIES

import argparse
import ConfigParser
import MDAnalysis 
from MDAnalysis.analysis.rms import rmsd, RMSD
from math import sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

#----------------------------------------------------
#--1-Parse command line arguements
#----------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument("input_conf", 
                    help="config file that sets input files and parameters")
parser.add_argument('out_csv',
                   help="specifies name of output csv file")
parser.add_argument('-R', 
                    action="store_true", 
                    dest="r_file", 
                    default="False",
                    help="if specified, imports list of indices selected for receptor")
parser.add_argument('-L',
                   action='store_true',
                   dest='l_file',
                   default="False",
                   help="if specified, imports list of indices selected for ligand")


args = parser.parse_args()

def parse_opt_args():
  if args.r_file == True:
      print("receptor indices selected!")
  else:
      print("no receptor indices given, will use atom selection phrase")


  if args.l_file == True:
      print("ligand indices selected!")
  else:
      print("no ligand indices given, will use atom selection phrase")


for i in range(5):
    print(".")

parse_opt_args()

#Set arguments as variables

config_file = args.input_conf

output_csv_file = args.out_csv

#OPTIONAL ASSIGNMENTS

#r_ind_list = list of indices for receptor 
#r_ind_list = parse_opt_args.r_indices_file

#l_ind_list = list of indices for ligand
#l_ind_list = parse_opt_args.l_indices_file

#----------------------------------------------------
#--2-Parse config arguments
#----------------------------------------------------

for i in range(5):
    print(".")


def Get_from_config(c_file):
    config = ConfigParser.ConfigParser()
    config.read(c_file)

    #set topo and traj files
    Get_from_config.topo = config.get('INPUT FILES','topology')
    Get_from_config.traj = config.get('INPUT FILES','trajectory')
        

    #extract receptor indices selection, if present
    if args.r_file == True:
        print('Getting indices for receptor selection...')
        r_conf_ind = config.get('RECEPTOR', 'indices')
        r_txt = open(r_conf_ind ,"r")
        r_ind = r_txt.read().split(',')
        #print("receptor indices: " + str(r_ind))
        Get_from_config.receptor = r_ind
        Get_from_config.r_is_list = 1
    else:
        Get_from_config.receptor = config.get('RECEPTOR','resname')
        Get_from_config.r_is_list = 0 # 0 if not a list


    #extract ligand indices selection, if present
    if args.l_file == True:
        l_conf_ind = config.get('LIGAND','indices')
        l_txt = open(l_conf_ind, 'r')
        l_ind = l_txt.read().split(',')
        Get_from_config.ligand = l_ind
        Get_from_config.l_is_list = 1
    else:
        Get_from_config.ligand = config.get('LIGAND', 'resname')
        Get_from_config.l_is_list = 0 #0 if not a list




Get_from_config(config_file) #config_file from section 1

for i in range(5):
    print(".")

print("topology file: " + str(Get_from_config.topo))

print("trajectory file: " + str(Get_from_config.traj))

print("receptor: " + str(Get_from_config.receptor))

print("ligand: " + str(Get_from_config.ligand))


for i in range(5):
    print(".")




#----------------------------------------------------
#--3-Set config parameters to MDA
#----------------------------------------------------

#import topologiy and trajectory

u = MDAnalysis.Universe(Get_from_config.topo, Get_from_config.traj)

def set_to_MDA():


    #script to iterate atom selections from list
    def create_atom_sel(inp_list):
    #initialize atom selection with first item on list
        num = int(inp_list[0])
        atom_sel = u.atoms[u.atoms.indices == num]
        rest_inp_list = inp_list[1:]
        for entry in rest_inp_list: #skips first item on list
            num2 = int(entry)
            atom_sel = atom_sel + u.atoms[u.atoms.indices == num2]
            create_atom_sel.atoms_selected = atom_sel


    #import receptor selection
    if Get_from_config.r_is_list == 1:
        #Get_from_config.receptor is a list if true
        create_atom_sel(Get_from_config.receptor)
        set_to_MDA.receptor = create_atom_sel.atoms_selected
        
       
    else:
        #Get_from_config.receptor is a selection string if false
        set_to_MDA.receptor = u.select_atoms(Get_from_config.receptor)

    #import receptor selection
    if Get_from_config.l_is_list == 1:
        #Get_from_config.receptor is a list if true
        create_atom_sel(Get_from_config.ligand)
        set_to_MDA.ligand = create_atom_sel.atoms_selected
    else:
        #Get_from_config.ligand is a selection string if false
        set_to_MDA.ligand = u.select_atoms(Get_from_config.ligand)

set_to_MDA()

print("receptor selection info: ")
print(set_to_MDA.receptor)

print("ligand selection info: ")
print(set_to_MDA.ligand)


for i in range(5):
    print(".")


#----------------------------------------------------
#--4-Calculate RMSD between COM of ligand and receptor
#----------------------------------------------------


def Distance_of_COM():
    #Calculate COM of ligand and receptor
    #r_COM = set_to_MDA.receptor.center_of_mass()
    #l_COM = set_to_MDA.ligand.center_of_mass()

    #Iterate over trajectory frames and calculate RMSD for each frame
    Dist_data = {}
    num_of_frames = len(u.trajectory)
    print("determing distance values....")
    for ts in u.trajectory:
        r_COM = set_to_MDA.receptor.center_of_mass()
        l_COM = set_to_MDA.ligand.center_of_mass()

        #RMSD(set_to_MDA.ligand, set_to_MDA.receptor, filename="test_out.dat")
        #R_COM = bb.center_of_mass()
    
        #L_COM = cc.center_of_mass() 
        #CACULATE DISTANCE BETWEEN COM COORD
        x1, y1, z1 = r_COM[0], r_COM[1], r_COM[2]
        x2, y2, z2 = l_COM[0], l_COM[1], l_COM[2]
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

        Dist_data[ts.frame] = distance
        print("current frame: " + str(ts.frame))



    #INITAL DISTANCE
    inital_distance = Dist_data.values()[0]
    print("Initial distance between receptor and ligand: " +
        str(inital_distance))

    #PLOT 
    #------------------------------------
    #CHOOSE NAME TO SAVE FIGURE TO
    plot_name = raw_input('Enter the name you wish to save the plot as: ')

    #ASSEMBLE PLOT DATA
    x = []
    y = []
    for key, value in Dist_data.iteritems():
       x.append(key)
       y.append(value)

    #ADD AVERAGE DISTANCE LINE TO PLOT
    mean_distance = np.mean(y)
    mean_y = []
    for i in range(len(y)):
        mean_y.append(mean_distance)

    #CONSTRUCT PLOT
    plt.plot(x,y, linewidth=0.6)
    plt.plot(x, mean_y, 'r--')
    plt.xlabel("timestep")
    plt.ylabel("Distance between COM (A)")
    plt.savefig(str(plot_name))
    plt.show

    #SAVE TO CSV
    df_data = {'frame': x,
            'distance': y}
    df = pd.DataFrame(df_data)
    df.to_csv(output_csv_file, columns=['frame','distance'])

    

Distance_of_COM()









