import json, requests, pandas as pd

## import zenodo key
with open("hide/personnal-keys.json") as f  : 
    ACCESS_TOKEN = json.load(f)["ZENODO_KEY"]

def get_doctype_aggregation(date_range) : 
    """
    req zenodo API , filter for one year
    output aggregation of types records
    """

    req = requests.get(
        "https://zenodo.org/api/records",
        params = {
             "q" : f"publication_date:{date_range}",
             "size" : 100,
             "sort" : "mostrecent",
             "all_version" : False,
             "access_tpoken" : ACCESS_TOKEN
         }
        )

    res = req.json()
    ## output de la liste d'agrégation des doctype qui se subdivise par sous type
    return res["aggregations"]["type"]["buckets"]


def reduce_aggregation(deep_data_list) : 
    """
    type aggregation from zenodo include subtype
    reduce aggregation to the fist level only
    """
    clean_dict = {}
    for elem in deep_data_list : 
        
        clean_dict.update(
            {elem["key"] : elem["doc_count"]}
            )

    return clean_dict  

# dictionnary to paste data
data = {}

date_range_schema = "[XXXX-01-01 TO XXXX-12-31]"

## iterate throw years
for year in range(2013, 2023) : 

    # deduce date range
    date_range = date_range_schema.replace("XXXX", str(year))
    print(date_range)

    # retrieve data from zenodo 
    raw_data = get_doctype_aggregation(date_range)

    # reduce doctype aggregation
    data[year] = reduce_aggregation(raw_data)


# transform dict to df (each doctype as a column)
df = pd.DataFrame.from_dict(data, orient = "index")
# export & name index col "year"
df.to_csv("zenodo-doctype-2013-23-dictionnaries.csv", index_label = "year")

