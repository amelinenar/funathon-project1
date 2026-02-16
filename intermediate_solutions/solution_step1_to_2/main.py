# %%
import pandas as pd
from sklearn.compose import make_column_selector as selector
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
import time
# %%
data = pd.read_parquet('s3://confpns/synthetic-transactions/rawdata/transactions/transactions_flats_final.parquet')
data_h = pd.read_parquet("s3://confpns/synthetic-transactions/rawdata/transactions/transactions_houses_final.parquet")

# %%
if data.columns.all() == data_h.columns.all():
    data_all = pd.concat([data, data_h])

# Setting data type of dteloc to a more meaningful category 
data_all["dteloc"] = pd.Categorical(
    data_all["dteloc"],
    categories=["1", "2"],
    ordered=False  # Set to True if the categories have a meaningful order
).rename_categories({"1": "House", "2": "Flat"})

data_all["price_sqm"] = data_all["valeurfonc"] / data_all["dsupdc"]
# Selecting the only cols we want to use

# %%
# Sample some data
data_small = data_all.sample(100000)
data_features = data_small[["depcom", "dteloc", "dnbppr", "dnbcha", "dsupdc"]]
data_target = data_small[["valeurfonc"]]
# depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc

# %%
# Encoding issue - differentiate between numeric and other
cols_cat = selector(dtype_exclude="number")
cols_num = selector(dtype_include="number")

# %%
data_features.sample(100000).hist(bins=10)
# Features are not troncated
# %%
data_features.sample(1000000).hist(log=True)
# %%
data_target.sample(100000).hist(bins=10)  # skewed to 0 bcs prices
# %%
data_target.sample(100000).plot(kind='hist', logx=True, logy=True)  # sharp decrease for assets above 1Me
