import numpy as np
import pandas as pd
MEAN = 1000
VAR = 150
LOW = 500
HIGH = 1500

SWEETS = ['Milka', 'Mieszanka studencka', 'Lindor', 'Prince polo', 'Delicje', 'Kinder niespodzianka'
    , 'Jeżyki', 'Ferrero Rocher', 'Merci', 'Raphaello']

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


print(gen_similarity(SWEETS))
gen_sweets(SWEETS)
