"""

1. 17IM30032 - BIMAL KUMAR SAHOO
2. 17IM10027 - VIKASH KUMAR
3. 17IM30013 - NARAYANE VANAD VIVEK
4. 17IM30012 - JITENDER SWAMI

"""


from collections import defaultdict, deque
from copy import deepcopy


class cars:
    def __init__(self, id, src, destination, battery_status, charge_rate, discharge_rate, Maxim_battery, avg_speed, adj):
        self.id = id
        self.destination = destination
        self.graph = deepcopy(adj)
        self.src = src
        self.Maxim_battery = Maxim_battery
        self.avg_speed = avg_speed
        self.path = []
        self.charge_rate = charge_rate
        self.battery_status = battery_status
        self.discharge_rate = discharge_rate
        for i in range(len(adj)):
            for j in range(len(adj)):
                if adj[i][j]!=float("inf"):
                    if (adj[i][j]/self.discharge_rate)>self.Maxim_battery:
                        self.graph[i][j]=float("inf")

        self.edges=[]
        for i in range(len(adj)):
            temp=[]
            for j in range(len(adj)):
                if self.graph[i][j]!=float('inf'):
                    temp.append(j)
            self.edges.append(temp)

    def shortest_path(self,arrival_time):
        initial = self.src
        shortest_paths = {initial: (None, 0)}
        current_node = self.src
        visited = set()

        while current_node != self.destination:
            visited.add(current_node)
            destinations = self.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = self.graph[current_node][next_node] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])


        while current_node is not None:
            self.path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        self.path = self.path[::-1]
        self.distance = defaultdict(int)
        for i in range(len(self.path)-2,-1,-1):
            self.distance[self.path[i]] = self.graph[self.path[i]][self.path[i+1]] + self.distance[self.path[i+1]]

        self.min_time = defaultdict(int)
        temp_battery_status = self.battery_status
        self.charge_time_required = defaultdict(int)
        for i in range(len(self.path)):
            if i:
                temp_battery_status -= self.graph[self.path[i-1]][self.path[i]]/self.discharge_rate
            self.min_time[self.path[i]] = self.distance[self.path[i]]/self.avg_speed
            min_charge_required = self.distance[self.path[i]]/self.discharge_rate
            self.charge_time_required[self.path[i]] = 0
            if(temp_battery_status <= min(self.Maxim_battery, min_charge_required)):
                self.charge_time_required[self.path[i]] = (min(self.Maxim_battery, min_charge_required)-temp_battery_status)/self.charge_rate
                self.min_time[self.path[i]] += self.charge_time_required[self.path[i]]

            arrival_time[self.path[i]][self.id] = 0
            if i:
                arrival_time[self.path[i]][self.id] = arrival_time[self.path[i-1]][self.id]+self.min_time[self.path[i-1]]-self.min_time[self.path[i]]

        return arrival_time

    def update_parameters(self, node, waiting_time, arrival_time):
        self.min_time[node] += waiting_time
        update = False
        for i in range(len(self.path)):
            if update:
                self.min_time[self.path[i]] += waiting_time
                arrival_time[self.path[i]][self.id] += waiting_time
            if self.path[i] == node:
                update = True
        return arrival_time


def schedule(cars_list,prev_charging_car, charge_time_left_list, conflict_node):
    car_obj_list = [w[0] for w in cars_list]
    if len(car_obj_list) == 1:
        return car_obj_list[0].id

    temp = sorted([sorted([(i, w.min_time[conflict_node] + charge_time_left_list[x.id])
                           for j, w in enumerate(car_obj_list) if j != i],
                  key=lambda y: -y[1]) for i, x in enumerate(car_obj_list)], key=lambda y: y[0][1])

    return temp[0][0][0]

