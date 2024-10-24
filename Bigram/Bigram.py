# Bigram implementation of name generation

import torch

N_NAMES = 20 # define the number of names to be created

# Creating generator for having the same results
generator = torch.Generator().manual_seed(15)

# Loading the dataset
all_names = open('list_of_names.txt', 'r').read().split("\n")
# combining all the names
single_names_list = ''.join(all_names)
# Finding the characters
chars = sorted(list(set(single_names_list))) + ["."]

# mapping characters to index
char_to_index = {c:i for i, c in enumerate(chars)}
# mapping index to character
index_to_char = {i:c for i, c in enumerate(chars)}

# Creating the lookup table
table = torch.zeros((len(chars), len(chars)), dtype = torch.int32)

# Updating the table to find the number of repeats for each index
for name in all_names:
    name = ["."] + list(name) + ["."]
    for idx in range(len(name)-1):
        idx1, idx2 = char_to_index[name[idx]], char_to_index[name[idx + 1]]
        table[idx1, idx2] += 1
        
# Finding the probability
P_char = table/table.sum(1).unsqueeze(1)

# Looping through number of desired names
for _ in range(N_NAMES):
    i = 0
    idx = 0
    name = ""
    while True:
        i += 1
        # Predict the next character by its probablity
        idx = torch.multinomial(P_char[idx,:], 1, replacement = True, generator = generator).item()
        name += index_to_char[idx]
        if idx == len(chars) - 1 and i > 3:
            print(name[:-1])
            break
        if idx == len(chars) - 1:
            name = name[:-1]
            i -= 1