from Bio import SeqIO
import RNA
import pandas as pd
import json
from tqdm import tqdm
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import pickle
import pathlib

protein_RNA_mapping = {
    'A': {'GCU', 'GCC', 'GCA', 'GCG'}, # Ala
    'C': {'UGU', 'UGC'}, # Cys
    'D': {'GAU', 'GAC'}, # Asp
    'E': {'GAA', 'GAG'}, # Glu
    'F': {'UUU', 'UUC'}, # Phe
    'G': {'GGU', 'GGC', 'GGA', 'GGG'}, # Gly
    'H': {'CAU', 'CAC'}, # His
    'I': {'AUU', 'AUC', 'AUA'}, # Ile
    'K': {'AAA', 'AAG'}, # Lys
    'L': {'UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'}, # Leu
    'M': {'AUG',}, # Met
    'N': {'AAU', 'AAC'}, # Asn
    'P': {'CCU', 'CCC', 'CCA', 'CCG'}, # Pro
    'Q': {'CAA', 'CAG'}, # Gln
    'R': {'CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'}, # Arg
    'S': {'UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'}, # Ser
    'T': {'ACU', 'ACC', 'ACA', 'ACG'}, # Thr
    'V': {'GUU', 'GUC', 'GUA', 'GUG'}, # Val
    'W': {'UGG', }, # Trp
    'Y': {'UAU', 'UAC'}, # Tyr
}

protein_RNA_list_mapping = {kk:list(protein_RNA_mapping[kk]) for kk in protein_RNA_mapping}
protein_list = [kk for kk in protein_RNA_mapping]

def one_hot_encode(indice, num_classes):
        # Create a matrix of zeros with shape (number of samples, number of classes)
        one_hot_matrix = np.zeros((num_classes, ))
        
        # Set the appropriate elements to 1
        one_hot_matrix[indice] = 1
        
        return one_hot_matrix

def process_aa(i, aa, rna):
    if aa == '*':
        return None, None, None, None, None
    rna_pos = i * 3
    codon = rna[rna_pos:rna_pos+3]
    
    if codon not in protein_RNA_mapping[aa]:
        return None, None, None, None, None
    
    aa_indices = protein_list.index(aa)
    obs = one_hot_encode(aa_indices, len(protein_list))
    act = protein_RNA_list_mapping[aa].index(codon)
    rew = RNA.fold(rna[:rna_pos+3])[1]
    term = False

    return obs, act, rew, term, i

def dataset_construct(protein, rna):
    observation = np.zeros((len(protein), len(protein_list)))
    action = np.zeros((len(protein), ))
    rewards = np.zeros((len(protein), ))
    terminal = np.zeros((len(protein), ))

    with ProcessPoolExecutor(max_workers=40) as executor:
        futures = {executor.submit(process_aa, i, aa, rna): i for i, aa in enumerate(protein)}
        for future in tqdm(as_completed(futures), total=len(protein)):
            obs, act, rew, term, i = future.result()
            if obs is None:  # handle '*' or invalid codon cases
                return None
            # observation.append(obs)
            # action.append(act)
            # rewards.append(rew)
            # terminal.append(term)
            observation[i] = obs
            action[i] = act
            rewards[i] = rew
            terminal[i] = term

    # return observation, action, rewards, terminal
    return {'observation': observation, 'action': action, 'rewards': rewards, 'terminal': terminal}
    
    

if __name__ == '__main__':
    all_data = pd.read_csv("./data/home_sapiens_final.csv", index_col=0)
    print(len(all_data))
    idxs = []
    for i in range(len(all_data)):
        if all_data['coding'][i] == 'Sequence unavailable' or all_data['3utr'][i] == 'Sequence unavailable' or all_data['5utr'][i] == 'Sequence unavailable':
            continue
        idxs.append(i)
    print(len(idxs))
    
    if pathlib.Path("data/rl_databse.pkl").exists():
        with open("data/rl_databse.pkl", 'rb') as fin:
            data_dict = pickle.load(fin)
            rl_database = data_dict['rl_database']
            rna_sequence_set = data_dict['rna_sequence_set']
    else:
        rl_database = []
        rna_sequence_set = set()

    for i in idxs:
        # print(i)
        rna_sequence = all_data['coding'][i].replace("T", 'U')
        if rna_sequence not in rna_sequence_set:
            rna_sequence_set.add(rna_sequence)
        else:
            continue
        # print(len(all_data['peptide'][i]))
        single_traj = dataset_construct(all_data['peptide'][i], rna_sequence)
        if single_traj is not None:
            rl_database.append(single_traj)
        
        if i% 10 == 0:
            with open("data/rl_databse.pkl", 'wb') as fin:
                pickle.dump({
                    'rl_database': rl_database,
                    'rna_sequence_set': rna_sequence_set,
                    }, fin)