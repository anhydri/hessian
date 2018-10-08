#!/Users/angu0022/miniconda3/bin/python3

import os, sys, itertools

def vib_mode_info(input_file):
    # Define variables used throughout the function
    nu_atom = 1
    nu_vib = 1
    list_dict_vib = []

    # Define temporary file nams
    vib_coord_file = "vib_coord.txt"
    vib_list_file = "vib_list.txt"
    nu_atom_file = "nu_atom.txt"
    nu_vib_file = "nu_vib.txt"

    command_1 = "grep 'Number of atoms:' " + input_file + " > " + nu_atom_file
    command_2 = "grep 'VIBRATIONAL MODES ARE USED IN THERMOCHEMISTRY' " + input_file + " > " + nu_vib_file
    command_3 = "sed -n '/MODE FREQ(CM\*\*-1)  SYMMETRY  RED. MASS  IR INTENS./,/THERMOCHEMISTRY/p' " + input_file + " > " + vib_list_file
    command_4 = "sed -n '/ANALYZING SYMMETRY OF NORMAL MODES/,/REFERENCE ON SAYVETZ CONDITIONS/p' " + input_file + " > " + vib_coord_file

    os.system(command_1)
    os.system(command_2)
    os.system(command_3)
    os.system(command_4)

    with open(nu_atom_file, "r") as f:
        list_txt_nu_atom = f.read().split()
        nu_atom = int(list_txt_nu_atom[-1])

    with open(nu_vib_file, "r") as f:
        list_txt_nu_vib_1 = f.read().split("-")
        list_txt_nu_vib_2 = list_txt_nu_vib_1[-1].split()
        nu_vib = int(list_txt_nu_vib_2[0])

    with open(vib_list_file, "r") as f:
        for line in itertools.islice(f, 1, nu_vib + 1):
            
            list_line = line.split()
            
            dict_vib = {}
            dict_vib["mode"] = int(list_line[0])
            dict_vib["frequency"] = float(list_line[1])
            dict_vib["symmetry"] = list_line[2]
            dict_vib["red_mass"] = float(list_line[3])
            dict_vib["ir_intens"] = float(list_line[4])
                                      
            list_dict_vib.append(dict_vib)

    # All information for a vibration is saved in the variable list_dict_vib.
    # print(list_dict_vib[0])

    nu_coord_line_per_geom = nu_atom * 3

    with open(vib_coord_file, "r") as f:
        list_line_1 = f.read().splitlines()
        list_line_2 = list_line_1[9:-2]
        list_line_2 = list(filter(None, list_line_2))     # complete list without empty lines

        vib_coord_len = len(list_line_2)
        nu_line_per_block = nu_coord_line_per_geom + 5 + 8    # 127 lines
        nu_block = int(vib_coord_len/nu_line_per_block)       # 23 blocks

        list_dict_geom = []

        for i in range(0, nu_block):   # loop over 23 blocks
            ini = i * 127
            end = (i + 1) * 127
            list_line_block = list_line_2[ini:end]    # a blok of frequencies and coordinates
            list_vib_mode = list_line_block[0].split()
            nu_freq = len(list_vib_mode)    # number of vibration modes per block, corresponding to number of geometries
            list_coord_block = list_line_block[5:5 + nu_coord_line_per_geom]

            list_line_comp_block =[]

            for line in list_coord_block:
                line_comp = line.split()
                list_line_comp_block.append(line_comp)
            
            # loop over the frequency number in a block
            for k in range(0, nu_freq):
                dict_mode_geom = {}
                dict_mode_geom["mode"] = int(list_vib_mode[k])

                freq_ind = k - nu_freq

                list_geom = []    # list of atom coordinates of one structure

                # loop over each atom in a column (each structure/column)
                for j in range(0, nu_atom):
                    ind = 3 * j
                    x_ind = ind + 0
                    y_ind = ind + 1
                    z_ind = ind + 2

                    dict_atom_coord = {}
                    dict_atom_coord["atom"] = list_line_comp_block[x_ind][1]
                    dict_atom_coord["x"] = float(list_line_comp_block[x_ind][freq_ind])
                    dict_atom_coord["y"] = float(list_line_comp_block[y_ind][freq_ind])
                    dict_atom_coord["z"] = float(list_line_comp_block[z_ind][freq_ind])
                    list_geom.append(dict_atom_coord)
                
                dict_mode_geom["geometry"] = list_geom
            
                list_dict_geom.append(dict_mode_geom)

    # print(list_dict_geom[-1])

    # At this step, we've gotten the geometry for each frequency mode. 
    # All is save in the variable list_dict_geom.
    # Also, the vibration mode information is saved in the varible list_dict_vib.

    command_5 = "rm -f vib_coord.txt vib_list.txt nu_atom.txt nu_vib.txt"
    os.system(command_5)

    # Merge two lists
    for i in range(0, len(list_dict_vib)):
        list_dict_vib[i]["geometry"] = list_dict_geom[i].get("geometry")

    return(list_dict_vib)