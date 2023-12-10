import pandas as pd


def generate_car_matrix(df):
    matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    for idx in matrix.index:
        matrix.loc[idx, idx] = 0
    
    return matrix

data = pd.read_csv('C:/Users/vheda/Downloads/MAPUP/MapUp-Data-Assessment-F-main/MapUp-Data-Assessment-F-main/datasets/dataset-1.csv')


car_matrix = generate_car_matrix(data)
print(car_matrix)



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




def filter_routes(df) -> list:
    # Filter routes based on the condition of average 'truck' values greater than 7
    filtered_routes = df.groupby('route')['car'].mean()
    routes_above_7 = filtered_routes[filtered_routes > 7].index.tolist()
    
    return sorted(routes_above_7)

car_matrix = filter_routes(data)
print(car_matrix)




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
