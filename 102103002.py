#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pandas as pd
import os
import sys

def main():
    # Arguments not equal to 5
    print("Checking for Errors...\n")
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dt, res = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        nCol = len(res.columns.values)

        # less then 3 columns in input dataset
        if nCol < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, nCol):
            pd.to_numeric(dt.iloc[:, i], errors='coerce')
            dt.iloc[:, i].fillna(
                (dt.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if nCol != len(weights)+1 or nCol != len(impact)+1:
            print(
                "ERROR : Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        print(" No error found\n\n Applying Topsis Algorithm...\n")
        Topsis(dt, res, nCol, weights, impact)


# In[56]:


def Normalize(dataset, nCol, weights):
    print(" Normalizing the DataSet...\n")
    for i in range(1, nCol):
        temp = 0
        for j in range(len(dataset)):
            temp = temp + dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(dataset)):
            dataset.iat[j, i] = (dataset.iloc[j, i] / temp)*weights[i-1]
    return dataset


# In[57]:


def Calc_Values(dataset, nCol, impact):
    print(" Calculating Positive and Negative values...\n")
    p_sln = (dataset.max().values)[1:]
    n_sln = (dataset.min().values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
    return p_sln, n_sln


# In[58]:


def Topsis(dt, res, nCol, weights, impact):
    dt = Normalize(dt, nCol, weights)
    p_sln, n_sln = Calc_Values(dt, nCol, impact)
    print(" Generating Score and Rank...\n")
    score = []
    for i in range(len(dt)):
        dt_p, dt_n = 0, 0
        for j in range(1, nCol):
            dt_p = dt_p + (p_sln[j-1] - dt.iloc[i, j])**2
            dt_n = dt_n + (n_sln[j-1] - dt.iloc[i, j])**2
        dt_p, dt_n = dt_p**0.5, dt_n**0.5
        score.append(dt_n/(dt_p + dt_n))
    res['Topsis Score'] = score
    
    res['Rank'] = (res['Topsis Score'].rank(method = 'max', ascending = False))
    res = res.astype({"Rank": int})
    
    print(" Writing Result to CSV...\n")
    res.to_csv(sys.argv[4], index = False)
    
    print(" Successfully Terminated")


# In[59]:


if __name__ == "__main__":
    main()


# In[ ]:




