import numpy as np
import pandas as pd
import random
ELFS_NUMBER = 20
PACZKI_PER_ELF = 20
LOW = 60
HIGH = 100


SWEETS = ['Milka', 'Mieszanka studencka', 'Lindor', 'Prince polo', 'Delicje', 'Kinder niespodzianka'
    , 'Jeżyki', 'Ferrero Rocher', 'Merci', 'Raphaello']
DESCRITPIONS = ['mały', 'duży', 'mądry', 'głupi']
COUNTRIES = ['Polska', 'Japonia', 'Tadżykistan', 'Kolumbia', 'USA']

def gen_similarity(SWEETS):
    sweets_size = len(SWEETS)
    similarity = np.random.uniform(0, 1, size=(sweets_size, sweets_size)).round(decimals=2)
    data = pd.DataFrame()
    for i in range(sweets_size):
        for j in range(sweets_size):
            if(i > j):
                data = data.append(pd.DataFrame([[SWEETS[i], SWEETS[j], similarity[i,j]]]))
            elif(j > i):
                data = data.append(pd.DataFrame([[SWEETS[i], SWEETS[j], similarity[j,i]]]))
    data.to_csv('./data/similarity.csv', index=False, header=False)
    return data

def gen_sweets(SWEETS):
    sweets_amount = np.random.uniform(LOW, HIGH, size=(len(SWEETS), 1)).astype(int)
    df0 = pd.DataFrame(SWEETS)
    df1 = pd.DataFrame(sweets_amount)
    df = pd.concat([df0,df1], axis=1)
    df.to_csv('./data/sweets.csv', index=False, header=False)
    # print(df)

def gen_paczki(SWEETS):
    data = pd.DataFrame()
    for i in range(ELFS_NUMBER*PACZKI_PER_ELF):
        data = data.append(pd.DataFrame([[i, random.choice(COUNTRIES), random.choice(DESCRITPIONS), SWEETS[int(i % len(SWEETS))], int((i % 10) * (HIGH+LOW)/5 * len(SWEETS)/(2 * ELFS_NUMBER * PACZKI_PER_ELF) + random.uniform(-2,1) + 1)]]))
    data.to_csv('./data/paczki.csv', index=False, header=False)



print(gen_similarity(SWEETS))
gen_sweets(SWEETS)
gen_paczki(SWEETS)
