#!/usr/bin/env python
# coding: utf-8

# # PYTHON TASK 1

# Question 1: Car Matrix Generation
# Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# values from id_2 as columns
# values from id_1 as index
# dataframe should have values from car column
# diagonal values should be 0.

# In[1]:


import pandas as pd


# In[2]:


import pandas as pd

def generate_car_matrix(df):
    matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    for idx in matrix.index:
        matrix.loc[idx, idx] = 0
    
    return matrix

data = pd.read_csv('C:/Users/vheda/Downloads/MAPUP/MapUp-Data-Assessment-F-main/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')


car_matrix = generate_car_matrix(data)
print(car_matrix)


# Question 2: Car Type Count Calculation
# Create a Python function named get_type_count that takes the dataset-1.csv
# as a DataFrame. Add a new categorical column car_type based on values 
# of the column car:
# 
# low for values less than or equal to 15,
# medium for values greater than 15 and less than or equal to 25,
# high for values greater than 25.
# Calculate the count of occurrences for each car_type category and return 
# the result as a dictionary. Sort the dictionary alphabetically based on
# keys.

# In[3]:


import pandas as pd

def get_type_count(df) -> dict:
    # Add a new categorical column 'car_type' based on 'car' values
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=choices))

    # Calculate count of occurrences for each 'car_type' category
    car_type_count = df['car_type'].value_counts().sort_index().to_dict()
    return car_type_count

data = pd.read_csv('C:/Users/vheda/Downloads/MAPUP/MapUp-Data-Assessment-F-main/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')

car_matrix = get_type_count(data)
print(car_matrix)


# Question 3: Bus Count Index Retrieval
# Create a Python function named get_bus_indexes that takes the dataset-1.csv
# as a DataFrame. The function should identify and return the indices as a 
# list (sorted in ascending order) where the bus values are greater than 
# twice the mean value of the bus column in the DataFrame.

# In[4]:


import pandas as pd

def get_bus_indexes(df) -> list:
    bus_counts = df['car'].value_counts()  
    if 'bus' in bus_counts.index:
        mean_bus = bus_counts['bus'] * 2 
        filtered_df = df[df['car'] == 'bus']
        indexes = filtered_df[filtered_df['id_1'] > mean_bus].index.tolist()
        return indexes
    else:
        return []
car_matrix = get_bus_indexes(data)
print(car_matrix)


# Question 4: Route Filtering
# Create a python function filter_routes that takes the dataset-1.csv as
# a DataFrame. The function should return the sorted list of values of 
# column route for which the average of values of truck column is 
# greater than 7.

# In[5]:


import pandas as pd

def filter_routes(df) -> list:
    # Filter routes based on the condition of average 'truck' values greater than 7
    filtered_routes = df.groupby('route')['car'].mean()
    routes_above_7 = filtered_routes[filtered_routes > 7].index.tolist()
    
    return sorted(routes_above_7)

car_matrix = filter_routes(data)
print(car_matrix)


# Question 5: Matrix Value Modification
# Create a Python function named multiply_matrix that takes the resulting
# DataFrame from Question 1, as input and modifies each value according to 
# the following logic:
# 
# If a value in the DataFrame is greater than 20, multiply those values by
# 0.75,If a value is 20 or less, multiply those values by 1.25.
# The function should return the modified DataFrame which has values 
# rounded to 1 decimal place.

# In[6]:


import pandas as pd

def multiply_matrix(matrix) -> pd.DataFrame:
    modified_data = matrix.copy()  # Make a copy of the input matrix

    for col in modified_data.columns:
        for idx in modified_data.index:
            value = modified_data.loc[idx, col]
            if value > 20:
                modified_data.loc[idx, col] = round(value * 0.75, 1)
            else:
                modified_data.loc[idx, col] = round(value * 1.25, 1)

    return modified_data

data = pd.read_csv('C:/Users/vheda/Downloads/MAPUP/MapUp-Data-Assessment-F-main/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')

car_matrix = multiply_matrix(data)
print(car_matrix)


# Question 6: Time Check
# You are given a dataset, dataset-2.csv, containing columns id, id_2, and
# timestamp (startDay, startTime, endDay, endTime). The goal is to verify 
# the completeness of the time data by checking whether the timestamps for
# each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM
# to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns
# a boolean series that indicates if each (id, id_2) pair has incorrect 
# timestamps. The boolean series must have multi-index (id, id_2).

# In[7]:


def time_check(df) -> pd.Series:
    try:
        time_check_series = df.groupby(['id', 'id_2']).apply(
            lambda x: (x['date_time'].max() - x['date_time'].min()).total_seconds() >= (24 * 3600 * 7)
        )
    except KeyError:
        print("Column 'date_time' not found. Please ensure the column exists in the DataFrame.")
        return pd.Series()

    return time_check_series

data = pd.read_csv('C:\Users\vheda\Downloads\MAPUP\MapUp-Data-Assessment-F-main\MapUp-Data-Assessment-F-main\datasets\dataset-2.csv')
car_matrix = time_check(data)
print(car_matrix)

