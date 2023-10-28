from ortools.linear_solver import pywraplp
from math import sin, cos
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import randint
import json

# TODO: estimate waster generated in each center
with open('./GIS_data.json', 'r') as file:
    GIS_data = json.load(file)


PI = 3.14
solver = pywraplp.Solver.CreateSolver("SAT")
J = 6  # number of collection centers candidates
K = 0 # number of transfer station candidates
F = 6 # number of treatment candidates
L = 6 # number of landfill candidates
treatment_type = ['incinerator', 'composting', 'recycling']
# treatment_type = ['incinerator', 'composting']
reduction_factor = {'incinerator': 0.1,'composting':0.2,'recycling':0.3}

# the parameters should be a statistics result in a period(day, week, month)
# the amount that limited vehicles can carry within a period
FLOW_UPPERBOUND = 2000
MINIMUM_LANDFILL_CAPACITY = 20000
# disposal capacity within a period
DISPOSAL_UPPERBOUND = 20000
# waste generated within a period
# waste_generated = [3000] * J

collection_centers = {
    j:{"waste_to_transfer":{k : solver.IntVar(0, FLOW_UPPERBOUND, f"{j}_{k}_collection_to_transfer") for k in range(K)},
       "waste_to_landfill":{l : solver.IntVar(0, FLOW_UPPERBOUND, f"{j}_{l}_collection_to_landfill") for l in range(L)},
       "waste_to_treatment":{g:{f : solver.IntVar(0, FLOW_UPPERBOUND, f"{j}_{f}_collection_to_{g}") for l in range(L) for f in range(F)} for g in treatment_type},
       "location":(randint(-90,90), randint(-180,180)), # coordinate
       "name": f'collection_center{j}',
       "waste_generated":GIS_data['collection_centers'][j]['waste_generated_year']
    } for j in range(J)
}

transfer_stations = {
    k:{"waste_from_collection":{j : collection_centers[j]['waste_to_transfer'][k] for j in range(J)},
       "waste_to_landfill":{l : solver.IntVar(0, FLOW_UPPERBOUND, f"{k}_{l}_transfer_to_landfill") for l in range(L)},
       "waste_to_treatment":{g:{f : solver.IntVar(0, FLOW_UPPERBOUND, f"{k}_{f}_transfer_to_{g}") for l in range(L) for f in range(F)} for g in treatment_type},
       "is_located" : solver.BoolVar(f"{k}_transfer_located"),
       "capacity_upperbound": 2000000,
       "location":(randint(-90,90), randint(-180,180)), # coordinate
       "name": f'transfer_center{k}'
    } for k in range(K)
}

treatment_plants = {
    f:{g:{"waste_from_collection":{j : collection_centers[j]['waste_to_treatment'][g][f] for j in range(J)},
       "waste_from_transfer":{k : transfer_stations[k]['waste_to_treatment'][g][f] for k in range(K)},
       "waste_to_landfill":{l : solver.IntVar(0, FLOW_UPPERBOUND, f"{f}_{l}_{g}_to_landfill") for l in range(L)},
       "is_located" : solver.BoolVar(f"{f}_{g}_located"),
       "location":(randint(-90,90), randint(-180,180)), # coordinate
       "name": f'treatment_plant{f}',
          "reduction_factor":reduction_factor[g],
          "capacity_upperbound": 2000000,}
        for g in treatment_type } for f in range(F)
}

sanitary_landfills = {
    l:{"waste_from_collection":{j : collection_centers[j]['waste_to_landfill'][l] for j in range(J)},
       "waste_from_transfer":{k : transfer_stations[k]['waste_to_landfill'][l] for k in range(K)},
       "waste_from_treatment":{g:{f : treatment_plants[f][g]['waste_to_landfill'][l] for f in range(F)} for g in treatment_type},
       # different from paper
       "waste_disposed": solver.IntVar(MINIMUM_LANDFILL_CAPACITY,DISPOSAL_UPPERBOUND,f"waste_disposal_{l}"),
       # "waste_disposal_upperbound":DISPOSAL_UPPERBOUND,
       "is_located" : solver.BoolVar(f"{l}_landfill_located"),
       "capacity_upperbound": 2000000,
       "location":(randint(-90,90), randint(-180,180)), # coordinate
       "name": f'landfill{l}'
    } for l in range(L)
}

# landfill count upperbound
LAND_FILL_UPPERBOUND = 1

# C1: landfill total count <= uppper bound
landfill_is_located = [sanitary_landfills[l]['is_located'] for l in range(L)]
solver.Add(sum(landfill_is_located) <= LAND_FILL_UPPERBOUND)
# landfill_count_constraint = solver.Constraint(0, LAND_FILL_UPPERBOUND)
# for l in range(L):
#     landfill_count_constraint.SetCoefficient(sanitary_landfills[l]['is_located'],1)

# C2: collection center outflow = waster generated
for key,value in collection_centers.items():
    solver.Add(sum(value['waste_to_transfer'].values())+sum(value['waste_to_landfill'].values())+sum(value['waste_to_treatment']['incinerator'].values())
    +sum(value['waste_to_treatment']['composting'].values())+sum(value['waste_to_treatment']['recycling'].values()) == value['waste_generated'])

# C3: transfer station inflow = outflow
for key,value in transfer_stations.items():
    solver.Add(sum(value['waste_from_collection'].values()) == sum(value['waste_to_landfill'].values())+sum(value['waste_to_treatment']['incinerator'].values())
    +sum(value['waste_to_treatment']['composting'].values())+sum(value['waste_to_treatment']['recycling'].values()))
    solver.Add(sum(value['waste_from_collection'].values())<=value['is_located']*value['capacity_upperbound'])

# C4: treatment plant inflow = outflow
for key,value in treatment_plants.items():
    for type, type_value in value.items():
        solver.Add((sum(type_value['waste_from_collection'].values()) + sum(type_value['waste_from_transfer'].values()))*type_value['reduction_factor']
                   ==sum(type_value['waste_to_landfill'].values()))
        solver.Add(sum(type_value['waste_from_collection'].values())+sum(type_value['waste_from_transfer'].values()) <=
                   type_value['capacity_upperbound']*type_value['is_located'])

# C5：landfill inflow = waste landfill
for key, value in sanitary_landfills.items():
    solver.Add(sum(value['waste_from_transfer'].values()) + sum(value['waste_from_collection'].values()) + sum(value['waste_from_treatment']['incinerator'].values())
               + sum(value['waste_from_treatment']['composting'].values()) + sum(value['waste_from_treatment']['recycling'].values()) <= value['is_located']*value['capacity_upperbound'])
    solver.Add(value['waste_disposed'] ==  sum(value['waste_from_transfer'].values()) + sum(value['waste_from_collection'].values()) + sum(value['waste_from_treatment']['incinerator'].values())
               + sum(value['waste_from_treatment']['composting'].values()) + sum(value['waste_from_treatment']['recycling'].values()))

# TODO: estimate transport cost per distance unit
transport_cost_vehicle = 20
# distance_center_transfer = np.random.rand(J,K)

objective=solver.Objective()
# for j in range(J):
#     for k in range(K):
#         objective.SetCoefficient(collection_centers[j]['waste_to_transfer'][k], transport_cost_vehicle * distance_center_transfer[j][k])

distance_center_plant = np.random.rand(J, F)
for j in range(J):
    for f in range(F):
        for type in treatment_type:
            objective.SetCoefficient(collection_centers[j]['waste_to_treatment'][type][f], transport_cost_vehicle * distance_center_plant[j][f])

disntance_center_landfill = np.random.rand(J, L)
for j in range(J):
    for l in range(L):
        objective.SetCoefficient(collection_centers[j]['waste_to_landfill'][l], transport_cost_vehicle * disntance_center_landfill[j][l])

transfer_cost_truck = 30
disntance_transfer_plant = np.random.rand(K,F)
for k in range(K):
    for f in range(F):
        for type in treatment_type:
            objective.SetCoefficient(transfer_stations[k]['waste_to_treatment'][type][f], transfer_cost_truck*disntance_transfer_plant[k][f])

disntance_transfer_landfill = np.random.rand(K,L)
for k in range(K):
    for l in range(L):
        objective.SetCoefficient(transfer_stations[k]['waste_to_landfill'][l],  transfer_cost_truck * disntance_transfer_landfill[k][l])

disntance_plant_landfill = np.random.rand(F,L)
for f in range(F):
    for l in range(L):
        for type in treatment_type:
            objective.SetCoefficient(treatment_plants[f][type]['waste_to_landfill'][l], transfer_cost_truck*disntance_plant_landfill[f][l])

# fixed cost
# transfer_station_fixed_cost = 20000
# for k in range(K):
#     objective.SetCoefficient(transfer_stations[k]['is_located'], transfer_station_fixed_cost)

# TODO: estimate fixed cost of treatment cost
fixed_cost_treatment_cost = {type: np.random.rand(F) for type in treatment_type}

for f in range(F):
    for type in treatment_type:
        objective.SetCoefficient(treatment_plants[f][type]['is_located'], fixed_cost_treatment_cost[type][f])

# TODO: estimate fixed and virable cost of landfill
variable_cost_landfill = 20
fixed_cost_landfill = 20000
for l in range(L):
    objective.SetCoefficient(sanitary_landfills[l]['waste_disposed'], 20)
    objective.SetCoefficient(sanitary_landfills[l]['is_located'], fixed_cost_landfill)
print("haha")
