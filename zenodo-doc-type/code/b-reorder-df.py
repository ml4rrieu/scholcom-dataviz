import json, requests, pandas as pd


df = pd.read_csv("zenodo-doctype-2013-23-dictionnaries.csv")


# create new df w 3 columns year, doctype, doc_count
df2 = pd.DataFrame({
    "year" : [], "doctype" : [], "doc_count" : []
})


## create a list w all the doctype (without the year)
print(df.columns)
cols = list(df.columns)
cols.remove("year")

# transform df
for col in cols : 
    for i in range(len(df)) : 
        ## add a row for each cols, col is doctype
        df2.loc[ len(df2)] = [ str(df.loc[i, "year"]), col, df.loc[i, col] ]

df2.to_csv("zenodo-doctype-2013-23-w-3-columns.csv", index = False)