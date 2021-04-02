# -*- coding: utf-8 -*-
"""AIFA Assignment1.ipynb
1. 17IM30032 - BIMAL KUMAR SAHOO
2. 17IM10027 - VIKASH KUMAR
3. 17IM30013 - NARAYANE VANAD VIVEK
4. 17IM30012 - JITENDER SWAMI
"""

from CARS import cars, schedule
from INPUT import data_input
import os
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 40)

def main():
    path = os.getcwd()
    path1 = os.path.join(path, "cars.csv")
    path2 = os.path.join(path, "distance.csv")
    cars_data, distance_data = data_input(path1, path2)
    distance_data.drop('Distance matrix', axis=1, inplace=True)
    distance_data = np.asarray(distance_data).tolist()
    print("File Import Success.")
    print ('\nCars Data:')
    print (cars_data)
    print ('\nDistance matrix:')
    for i in distance_data:
        print (i)

    src = dict(cars_data['Source'])
    destination = dict(cars_data['destination'])
    battery_status = dict(cars_data['battery_status'])
    charging_rate = dict(cars_data['charging_rate'])
    discharge_rate = dict(cars_data['discharge_rate'])
    Max_battery = dict(cars_data['Max_battery'])
    avg_speed = dict(cars_data['avg_speed'])

    arrival_time = [[float("inf") for i in range(cars_data.shape[0])] for i in range(len(distance_data))]

    # __init__(self,id, src, destination, battery_status, charge_rate, discharge_rate, Maxim_battery, avg_speed, distance_data)
    all_cars = {}
    for i in range(cars_data.shape[0]):
        obj = cars(i, src[i], destination[i], battery_status[i], charging_rate[i], discharge_rate[i], Max_battery[i]
                   , avg_speed[i], distance_data)
        arrival_time = obj.shortest_path(arrival_time)
        all_cars[i] = obj

    # for idx in all_cars.keys():
    #     print(all_cars[idx])

    global_time_list = []
    for conflict_node in range(len(distance_data)):
        cars_present = [all_cars[i] for i in range(cars_data.shape[0]) if
                        arrival_time[conflict_node][i] != float("inf")]
        charge_time_left_list = [0] * cars_data.shape[0]
        for i in cars_present:
            arr_time = arrival_time[conflict_node][i.id]
            dep_time = arr_time + i.charge_time_required[conflict_node]
            charge_time_left_list[i.id] = int(i.charge_time_required[conflict_node])
            global_time_list.append([i, "arrival", conflict_node, arr_time])
            global_time_list.append([i, "departure", conflict_node, dep_time])
    global_time_list.sort(key=lambda x: x[3])

    # print(f"global_time_list:{global_time_list}")

    cars_list_list = [[]] * len(distance_data)  # num nodes X num cars at node
    prev_event_time_list = [0] * len(distance_data)  # num nodes
    prev_charging_cars_list = [-1] * len(distance_data)  # num nodes
    cntr = 0
    while (len(global_time_list) != 0):
        cntr += 1
        event = global_time_list.pop(0)
        conflict_node = event[2]

        if (event[1] == "departure"):
            poped = False
            index_event_id = -1
            for i in range(len(cars_list_list[conflict_node])):
                if (cars_list_list[conflict_node][i][0].id == event[0].id):
                    index_event_id = i
            waiting_time = event[3] - prev_event_time_list[conflict_node]
            prev_event_time_list[conflict_node] = int(event[3])
            charge_time_left_list[prev_charging_cars_list[conflict_node]] -= waiting_time
            if (prev_charging_cars_list[conflict_node] == event[0].id):
                cars_list_list[conflict_node].pop(index_event_id)
                poped = True

            if (len(cars_list_list[conflict_node]) > 0):
                for i in range(len(cars_list_list[conflict_node])):
                    if (cars_list_list[conflict_node][i][0].id != prev_charging_cars_list[conflict_node]):
                        index_list_in_global_time_list = []
                        for idx, listn in enumerate(global_time_list):
                            if listn[0].id == cars_list_list[conflict_node][i][0].id and listn[2] == conflict_node:
                                index_list_in_global_time_list.append(idx)

                        arrival_time = cars_list_list[conflict_node][i][0].update_parameters(conflict_node,
                                                                                             waiting_time, arrival_time)
                        if index_list_in_global_time_list:
                            for index_in_global_time_list in index_list_in_global_time_list:
                                old_list = global_time_list[index_in_global_time_list]
                                arr_time = arrival_time[conflict_node][cars_list_list[conflict_node][i][0].id]
                                dep_time = arr_time + cars_list_list[conflict_node][i][0].charge_time_required[
                                    conflict_node]
                                new_list = [cars_list_list[conflict_node][i][0], "arrival", old_list[2], arr_time] if \
                                    old_list[1] == "arrival" \
                                    else [cars_list_list[conflict_node][i][0], "departure", old_list[2], dep_time]
                                global_time_list[index_in_global_time_list] = new_list
                        global_time_list.sort(key=lambda x: x[3])

            if poped and len(cars_list_list[conflict_node]) > 0:
                prev_charging_cars_list[conflict_node] = schedule(cars_list_list[conflict_node],
                                                                  prev_charging_cars_list[conflict_node],
                                                                  charge_time_left_list, conflict_node)

        else:
            index_event_id = -1
            for i in range(len(cars_list_list[conflict_node])):
                if cars_list_list[conflict_node][i][0].id == event[0].id:
                    index_event_id = i
            waiting_time = event[3] - prev_event_time_list[conflict_node]
            prev_event_time_list[conflict_node] = event[3]
            cars_list_list[conflict_node].append(event)
            charge_time_left_list[prev_charging_cars_list[conflict_node]] -= waiting_time
            if len(cars_list_list[conflict_node]) > 0:  # changing departure time
                for i in range(len(cars_list_list[conflict_node])):
                    if cars_list_list[conflict_node][i][0].id != prev_charging_cars_list[conflict_node]:
                        index_list_in_global_time_list = []
                        for idx, listn in enumerate(global_time_list):
                            if listn[0].id == cars_list_list[conflict_node][i][0].id and listn[2] == conflict_node:
                                index_list_in_global_time_list.append(idx)

                        arrival_time = cars_list_list[conflict_node][i][0].update_parameters(conflict_node,
                                                                                             waiting_time, arrival_time)
                        if index_list_in_global_time_list:
                            for index_in_global_time_list in index_list_in_global_time_list:
                                old_list = global_time_list[index_in_global_time_list]
                                arr_time = arrival_time[conflict_node][cars_list_list[conflict_node][i][0].id]
                                dep_time = arr_time + cars_list_list[conflict_node][i][0].charge_time_required[
                                    conflict_node]
                                new_list = [cars_list_list[conflict_node][i][0], "arrival", old_list[2], arr_time] if \
                                    old_list[1] == "arrival" \
                                    else [cars_list_list[conflict_node][i][0], "departure", old_list[2], dep_time]
                                global_time_list[index_in_global_time_list] = new_list
                        global_time_list.sort(key=lambda x: x[3])

            if len(cars_list_list[conflict_node]) > 0:
                prev_charging_cars_list[conflict_node] = schedule(cars_list_list[conflict_node],
                                                                  prev_charging_cars_list[conflict_node],
                                                                  charge_time_left_list, conflict_node)  # scheduling

    print("\nfinal value of all cars")
    for idx in all_cars.keys():
        print(f"Car ID:{idx}")
        print(f"Min time for Car ID {idx}:  {dict(all_cars[idx].min_time)}")

    return


if __name__ == "__main__":
    main()
