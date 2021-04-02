"""
Group Members:
1. 17IM30032 - BIMAL KUMAR SAHOO
2. 17IM10027 - VIKASH KUMAR
3. 17IM30013 - NARAYANE VANAD VIVEK
4. 17IM30012 - JITENDER SWAMI

"""

import pandas as pd

def data_input(path_cars, path_distance):
    """
    :param path_cars: Path to CSV file containing information about CARS
    :param path_distance: Path to CSV file Containing Distance Matrix
    :return: CAR DATA Frame,Distance matrix Dataframe
    """
    car_df = pd.read_csv(path_cars)
    distance_df = pd.read_csv(path_distance)

    return car_df, distance_df