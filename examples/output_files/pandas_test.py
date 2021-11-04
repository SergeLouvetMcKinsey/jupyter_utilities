#
# Jupyter Notebook conversion utility version 0.2
# Converted on 2021-11-04 15:53:11
#
# Cell 1
!pip install pandas
!pip install openpyxl

print("Done with cell 1")

# Cell 2
import pandas as pd
# Cell 3
#
# read a comma separated file
#
transactions = pd.read_csv('data_input/transactions.csv', sep=',')

#
# read a tab separated file
#
customers_1 = pd.read_csv('data_input/customers.txt', sep='\t')

# note that the phone numbers are loosing their leading zeroes:
print(customers_1)

print("Done with cell 3")

# Cell 4
#
# we need to prevent pandas to convert loaded text to a numeric field type
#
# read a text file (here a tab separated file) and force all fields to string
#
customers = pd.read_csv('data_input/customers.txt', sep='\t', dtype='str')
print(customers)

print("Done with cell 4")

# Cell 5
costs = pd.read_excel('data_input/costs.xlsx', sheet_name='Sheet1')

print("Done with cell 5")

# Cell 6

print(f"Nomber of rows: {customers.shape[0]}")
print(f"Nomber of columns: {customers.shape[1]}")
print("Columns:", customers.columns)

print("Done with cell 6")

# Cell 7
pd.set_option('display.max_columns', None)

print("Done with cell 7")

# Cell 8
transactions.head(n=5)

print("Done with cell 8")

# Cell 9
transactions

print("Done with cell 9")

# Cell 10
transactions.describe()

print("Done with cell 10")

# Cell 11
#
# count number of distinct values in a column
#
print(transactions["customer_id"].nunique())

print("Done with cell 11")

# Cell 12
#
# list of distinct values in a column
#
print(transactions["customer_id"].unique())

print("Done with cell 12")

# Cell 13
#
# list of distinct values in a column with their frequency
#
print(transactions["customer_id"].value_counts())

print("Done with cell 13")

# Cell 14
transactions.dtypes

print("Done with cell 14")

# Cell 15
transactions.info()

print("Done with cell 15")

# Cell 16
transactions.shape[0]

print("Done with cell 16")

# Cell 17
transactions_subset = transactions.copy()
transactions_subset = transactions_subset[['customer_id', 'product_id']]
transactions_subset.dtypes

print("Done with cell 17")

# Cell 18
transactions_drop = transactions.copy()
transactions_drop.drop(['row_id', 'geo', 'bu', 'customer_level_2', 'product_level_2'], axis=1, inplace=True)
transactions_drop.dtypes

print("Done with cell 18")

# Cell 19
transactions_rename = transactions.copy()
transactions_rename.rename(columns={'customer_level_2':'customer_category', 'product_level_2':'product_category'}, inplace=True)
transactions_rename.dtypes

print("Done with cell 19")

# Cell 20
customers_add_columns = customers.copy()

# adding a new column to form a unique city name

customers_add_columns["unique_city"] = customers_add_columns["country"] + "-" + customers_add_columns["city"]

customers_add_columns

print("Done with cell 20")

# Cell 21
transactions_type = transactions.copy()

#To text
transactions_type['row_id'] = transactions_type['row_id'].astype(str)
transactions_type.dtypes

#To number
transactions_type['row_id'] = pd.to_numeric(transactions_type['row_id'], errors='coerce')
transactions_type.dtypes

#To date
transactions_type['transaction_date'] = pd.to_datetime(transactions_type['transaction_date'])
transactions_type.dtypes

print("Done with cell 21")

# Cell 22
# the costs dataset contains one column per month for product price in different geography:
print(costs.info())
costs.head(n=5)

costs_transpose = pd.melt(costs, id_vars=['product_id','geo'], value_vars=['2019-01','2019-02','2019-03','2019-04','2019-05','2019-06','2019-07','2019-09','2019-10','2019-11','2019-12','2020-01'])
costs_transpose.rename(columns={'variable':'year_month'}, inplace=True)
costs_transpose.rename(columns={'value':'average_unit_cost'}, inplace=True)

print(costs_transpose.info())
costs_transpose.head(n=5)

print("Done with cell 22")

# Cell 23
#
# if you do not want to type the list of columns to pivot, you can build it from the definition of the dataframe:
#

# get the list of columns as a Python list
costs_columns_to_pivot = list(costs.columns)

# remove the columns we want to retain as is
costs_columns_to_pivot.remove("product_id")
costs_columns_to_pivot.remove("geo")
print(costs_columns_to_pivot)

# transpose
costs_transpose_2 = pd.melt(costs, id_vars=['product_id','geo'], value_vars=costs_columns_to_pivot)
costs_transpose_2.rename(columns={'variable':'year_month'}, inplace=True)
costs_transpose_2.rename(columns={'value':'average_unit_cost'}, inplace=True)

# check results
print(costs_transpose_2.info())
costs_transpose_2.head(n=5)


print("Done with cell 23")

# Cell 24
left_source_df = pd.DataFrame({"column_join": ["A","B","C"], "column_b": ["X1","Y1","W1"], "column_c":[111,222,333]})
right_source_df = pd.DataFrame({"column_join": ["A","B","D"], "column_b": ["X2","Y2","Z2"], "column_d":[444,555,666]})

print("\nLeft source")
print(left_source_df)

print("\nRight source")
print(right_source_df)

print("\nExample inner join")
example_inner = pd.merge(left_source_df, right_source_df, 
                         how='inner', 
                         left_on=['column_join'], 
                         right_on=['column_join'], 
                         suffixes=('_LEFT', '_RIGHT'))
print(example_inner)

print("\nExample left join")
example_left = pd.merge(left_source_df, right_source_df, 
                        how='left', left_on=['column_join'], 
                        right_on=['column_join'], 
                        suffixes=('_LEFT', '_RIGHT'))
print(example_left)

print("\nExample right join")
example_right = pd.merge(left_source_df, right_source_df, 
                         how='right', 
                         left_on=['column_join'], 
                         right_on=['column_join'], 
                         suffixes=('_LEFT', '_RIGHT'))
print(example_right)

print("\nExample outer join")
example_outer = pd.merge(left_source_df, right_source_df, 
                         how='outer', 
                         left_on=['column_join'], 
                         right_on=['column_join'], 
                         suffixes=('_LEFT', '_RIGHT'))
print(example_outer)

print("Done with cell 24")

# Cell 25
# the merge() function can add a column with the source of the data (left_only, right_only, both) 
# by default, this column is named "_merge"
# we can apply a filter on this column to retain only rows available in left data source, right data source or both.

print("\nExample outer join with indicator")
example_outer_with_indicator = pd.merge(left_source_df, right_source_df, indicator=True, how='outer', left_on=['column_join'], right_on=['column_join'], suffixes=('_LEFT', '_RIGHT'))
print(example_outer_with_indicator)

print("\nExample left only join")
example_left_only = pd.merge(left_source_df, right_source_df, indicator=True, how='left', left_on=['column_join'], right_on=['column_join'], suffixes=('_LEFT', '_RIGHT'))
example_left_only = example_left_only[example_left_only["_merge"] == "left_only"]
print(example_left_only)

print("\nExample right only join")
example_right_only = pd.merge(left_source_df, right_source_df, indicator=True, how='right', left_on=['column_join'], right_on=['column_join'], suffixes=('_LEFT', '_RIGHT'))
example_right_only = example_right_only[example_right_only["_merge"] == "right_only"]
print(example_right_only)

print("Done with cell 25")

# Cell 26
#
# we can, of course, extract the three subsets from the results of our outer join with indicator
#
example_outer_left_only = example_outer_with_indicator[example_outer_with_indicator["_merge"] == "left_only"]
example_outer_right_only = example_outer_with_indicator[example_outer_with_indicator["_merge"] == "right_only"]
example_outer_common_only = example_outer_with_indicator[example_outer_with_indicator["_merge"] == "both"]

print("\nExample right only from outer join")
print(example_outer_left_only)

print("\nExample right only from outer join")
print(example_outer_right_only)

print("\nExample common only from outer join")
print(example_outer_common_only)

print("Done with cell 26")

# Cell 27
transactions_enriched = transactions.copy()
transactions_enriched['transaction_date'] = transactions_enriched['transaction_date'].astype(str)
transactions_enriched['year_month'] = transactions_enriched['transaction_date'].str[:7]
transactions_enriched[['transaction_date', 'year_month']]

print("Done with cell 27")

# Cell 28
merge_inner = pd.merge(transactions_enriched, costs_transpose, how='inner', left_on=['product_id', 'geo', 'year_month'], right_on=['product_id', 'geo', 'year_month'], suffixes=('_LEFT', '_RIGHT'))
merge_inner.info()

print(f"Nunmber of rows in transaction data {transactions_enriched.shape[0]}")
print(f"Number of rows in merged dataset: {merge_inner.shape[0]}")

print("Done with cell 28")

# Cell 29
# Since the column names are identical in both dataframes, we can used a simplified version:

merge_left = pd.merge(transactions_enriched, costs_transpose,
                      indicator=True,
                      how='left', 
                      on=['product_id', 'geo', 'year_month'], 
                      suffixes=('_LEFT', '_RIGHT'))

merge_left.info()

print(f"Nunmber of rows in transaction data {transactions_enriched.shape[0]}")
print(f"Number of rows in merged dataset: {merge_left.shape[0]}")

transactions_without_costs = merge_left[merge_left["_merge"] == "left_only"]
print(f"Number of transaction rows without costs: {transactions_without_costs.shape[0]}")

print("Done with cell 29")

# Cell 30
# All columns from the transaction dataset will be set to NaN, so we retain only the columns used as key

 
merge_right_only = pd.merge(transactions_enriched[['product_id', 'geo', 'year_month']], costs_transpose, 
                            indicator=True, 
                            how='right', 
                            on=['product_id', 'geo', 'year_month'], 
                            suffixes=('_LEFT', '_RIGHT'))

merge_right_only = merge_right_only[merge_right_only["_merge"] == "right_only"]

merge_right_only
 

print("Done with cell 30")

# Cell 31
customers_copy = customers.copy()
#
# for this example, we add the country code as a prefix to the phone number if the prefix is not yet there
# there are a lot of things that can go wrong and are not covered hereunder.
#

for row_number, row_data in customers_copy.iterrows():
   
    phone_nbr = row_data["phone_nbr"]
    country = row_data["country"]
    
    
    if country == "BE":
        prefix = "0032"
    elif country == "FR":
        prefix = "0033"
    else:
        prefix = ""
        
# update the dataframe, as required

    if len(prefix) > 0 and phone_nbr[0:4] != prefix:
        new_phone_nbr = prefix + phone_nbr
        customers_copy.loc[row_number,"phone_nbr"] = new_phone_nbr

print(customers_copy)

print("Done with cell 31")

# Cell 32
transactions.to_csv('data_output/transactions_output.csv', sep=',', header=True, index=False, encoding='utf-8')

print("Done with cell 32")

# Cell 33
merge_inner.to_excel('data_output/merge.xlsx', sheet_name='merge_inner', index=False)

print("Done with cell 33")
