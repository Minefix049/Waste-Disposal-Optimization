from ortools.linear_solver import pywraplp
from math import sin,cos
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

PI = 3.14159
class Node:
    def __init__(self, node_id, pos:tuple, service_demand:list, capacity:list, fraction:list, solver, node_num):
        self.position = pos
        self.node_id = node_id
        self.service_demand = service_demand
        self.incinerator_fraction = fraction[0]
        self.recycling_fraction = fraction[1]
        self.composting_fraction = fraction[2]

        self.incinerator_capacity = capacity[0]
        self.recycling_capacity = capacity[1]
        self.composting_capacity = capacity[2]
        self.landfill_capacity = capacity[3]

        self.solver = solver
        self.presence_incinerator = self.solver.BoolVar(f"{node_id}_presence_incinerator")
        self.presence_recycling = self.solver.BoolVar(f"{node_id}_presence_recycling")
        self.presence_composting = self.solver.BoolVar(f"{node_id}_presence_composting")
        self.presence_landfill = self.solver.BoolVar(f"{node_id}_presence_landfill")

        # amount of waste processed in this node
        self.waste_incinerator = self.solver.IntVar(0,self.incinerator_capacity,f"{node_id}_waste_incinerator")
        self.waste_recycling = self.solver.IntVar(0,self.recycling_capacity,f"{node_id}_waste_recycling")
        self.waste_composting= self.solver.IntVar(0,self.composting_capacity,f"{node_id}_waste_composting")
        self.waste_landfill = self.solver.IntVar(0,self.landfill_capacity,f"{node_id}_waste_landfill")

        # variable of outflow waste
        self.user_outflow_incinerator = {}
        self.user_outflow_recycling = {}
        self.user_outflow_composting = {}
        self.incinerator_outflow_landfill = {}
        self.recycling_outflow_landfill = {}
        self.composting_outflow_landfill = {}
        self.user_outflow_landfill = {}

        for dest_id in range(node_num):
            self.user_outflow_incinerator[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_user_outflow_incinerator")
            self.user_outflow_recycling[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_user_outflow_recycling")
            self.user_outflow_composting[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_user_outflow_composting")
            self.incinerator_outflow_landfill[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_incinerator_outflow_landfill")
            self.recycling_outflow_landfill[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_recycling_outflow_landfill")
            self.composting_outflow_landfill[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_composting_outflow_landfill")
            self.user_outflow_landfill[dest_id+1] = self.solver.IntVar(0, service_demand, f"{node_id}_{dest_id}_user_outflow_landfill")

        # variable of inflow waste
        self.user_inflow_incinerator = {}
        self.user_inflow_recycling = {}
        self.user_inflow_composting = {}
        self.incinerator_inflow_landfill = {}
        self.recycling_inflow_landfill = {}
        self.composting_inflow_landfill = {}
        self.user_inflow_landfill = {}

    def add_constraints(self):
        # outflow = service demand
        self.solver.Add(sum(self.user_outflow_incinerator.values())+sum(self.user_outflow_recycling.values())
                        +sum(self.user_outflow_composting.values())+sum(self.user_outflow_landfill.values()) == self.service_demand)
        # inflow = waste treated
        self.solver.Add(sum(self.user_inflow_composting.values()) == self.waste_composting)
        self.solver.Add(sum(self.user_inflow_recycling.values()) == self.waste_recycling)
        self.solver.Add(sum(self.user_inflow_incinerator.values()) == self.waste_incinerator)
        self.solver.Add(sum(self.user_inflow_landfill.values())+sum(self.incinerator_inflow_landfill.values())+sum(self.recycling_inflow_landfill.values())
                        + sum(self.composting_inflow_landfill.values()) == self.waste_landfill)
        # waster treated <= presence * capacity
        self.solver.Add(self.waste_incinerator <= self.landfill_capacity*self.presence_incinerator)
        self.solver.Add(self.waste_recycling <= self.recycling_capacity*self.presence_recycling)
        self.solver.Add(self.waste_composting <= self.composting_capacity*self.presence_composting)
        self.solver.Add(self.waste_landfill <= self.landfill_capacity*self.presence_landfill)

        # process inflow * fraction = process outflow
        self.solver.Add(sum(self.user_inflow_incinerator.values())*self.incinerator_fraction == sum(self.incinerator_outflow_landfill.values()))
        self.solver.Add(sum(self.user_inflow_recycling.values())*self.recycling_fraction == sum(self.recycling_outflow_landfill.values()))
        self.solver.Add(sum(self.user_inflow_composting.values())*self.recycling_fraction == sum(self.composting_outflow_landfill.values()))

        # a node can only have one process plant
        self.solver.Add(self.presence_landfill+self.presence_composting+self.presence_recycling <= 1)



if __name__ == "__main__":
    solver = pywraplp.Solver.CreateSolver("SAT")
    # parameters to be identified
    node_num = 5
    node_positions = [(1+sin(0),1+cos(0)),(1+sin(2*PI/5),1+cos(2*PI/5)),(1+sin(2*PI/5*2),1+cos(2*PI/5)*2),(1+sin(2*PI/5*3),1+cos(2*PI/5*3)),(1+sin(2*PI/5*4),1+cos(2*PI/5*4))]
    service_demand = [6000, 6000, 6000, 6000, 6000]
    capacity = [[0, 0, 0, 0],[4500,2500,0,4500],[4500,2500,0,4500],[4500,2500,0,4500],[4500,2500,0,4500]]
    fraction = [0.1, 0.25, 0]
    # economic, landfill waste, environment impact
    objective_weights = [1, 1, 0]
    # incinerator, recycling, composting, landfill
    process_plant_fixed_cost = [30, 20, 25, 1]
    process_cost = np.array([1, 3, 2.5, 1])
    # transport cost matrix
    transport_cost_matrix = np.array([[0,3,3,5,7],
                             [2,0,3,5,7],
                             [5,8,0,2,4],
                             [3,6,6,0,2],
                             [3,6,6,8,0]]) * 0.001
    network = {}
    for i in range(node_num):
        network[i+1] = Node(i+1, node_positions[i], service_demand[i], capacity[i], fraction, solver, node_num)
        # network[i+1].add_constraints()
    for i in range(node_num):
        for j in range(node_num):
            network[i+1].user_inflow_incinerator[j+1] = network[j+1].user_outflow_incinerator[i+1]
            network[i+1].user_inflow_recycling[j+1] = network[j+1].user_outflow_recycling[i+1]
            network[i+1].user_inflow_composting[j+1] = network[j+1].user_outflow_composting[i+1]
            network[i+1].incinerator_inflow_landfill[j+1] = network[j+1].incinerator_outflow_landfill[i+1]
            network[i+1].recycling_inflow_landfill[j+1] = network[j+1].recycling_outflow_landfill[i+1]
            network[i+1].composting_inflow_landfill[j+1] = network[j+1].composting_outflow_landfill[i+1]
            network[i+1].user_inflow_landfill[j+1] = network[j+1].user_outflow_landfill[i+1]
    for i in range(node_num):
        network[i+1].add_constraints()
    # add objective
    objective=solver.Objective()
    for i in range(node_num):
        # objective 2 with weights
        objective.SetCoefficient(network[i+1].waste_landfill, 1*objective_weights[1]+process_cost[3]*objective_weights[0])
        # investment(fixed cost)
        objective.SetCoefficient(network[i+1].presence_incinerator, process_plant_fixed_cost[0] * objective_weights[0])
        objective.SetCoefficient(network[i+1].presence_recycling, process_plant_fixed_cost[1] * objective_weights[0])
        objective.SetCoefficient(network[i+1].presence_composting, process_plant_fixed_cost[2] * objective_weights[0])
        objective.SetCoefficient(network[i+1].presence_landfill, process_plant_fixed_cost[3] * objective_weights[0])
        # variable cost
        objective.SetCoefficient(network[i+1].waste_incinerator, process_cost[0] * objective_weights[0])
        objective.SetCoefficient(network[i+1].waste_recycling, process_cost[1] * objective_weights[0])
        objective.SetCoefficient(network[i+1].waste_composting, process_cost[2] * objective_weights[0])
        # objective.SetCoefficient(network[i+1].waste_landfill,process_cost[3] * objective_weights[0])
        # transportation cost
        for j in range(node_num):
            objective.SetCoefficient(network[i + 1].user_outflow_incinerator[j+1], transport_cost_matrix[i][j] * objective_weights[0])
            objective.SetCoefficient(network[i + 1].user_outflow_recycling[j+1], transport_cost_matrix[i][j] * objective_weights[0])
            objective.SetCoefficient(network[i + 1].user_outflow_composting[j+1], transport_cost_matrix[i][j] * objective_weights[0])
            objective.SetCoefficient(network[i + 1].user_outflow_landfill[j+1], transport_cost_matrix[i][j] * objective_weights[0])
            objective.SetCoefficient(network[i + 1].incinerator_outflow_landfill[j + 1], transport_cost_matrix[i][j] * objective_weights[0])
            objective.SetCoefficient(network[i + 1].recycling_outflow_landfill[j + 1], transport_cost_matrix[i][j] * objective_weights[0])
            objective.SetCoefficient(network[i + 1].composting_outflow_landfill[j + 1], transport_cost_matrix[i][j] * objective_weights[0])

    objective.SetMinimization()
    # objective.SetMaximization()
    status = solver.Solve()
    G = nx.DiGraph()
    subax = plt.subplot(4, 1, (1, 4))
    pos = {}
    labels = {}
    colors = {}
    if status == pywraplp.Solver.OPTIMAL:
        print('optimal!!')
        print("Objective value =", solver.Objective().Value())

    else:
        print('The problem does not have an optimal solution.')

    print("Problem solved in %f milliseconds" % solver.wall_time())
    print("Problem solved in %d iterations" % solver.iterations())
    print("Problem solved in %d branch-and-bound nodes" % solver.nodes())
    for i in range(node_num):
        node = network[i + 1]
        G.add_node(node.node_id)
        discription = f'{node.node_id}:'
        if node.presence_landfill.solution_value() > 0:
            discription += 'land_fill'
        if node.presence_incinerator.solution_value() > 0:
            discription += '\nincinerator'
        if node.presence_recycling.solution_value() > 0:
            discription += '\nrecycling'
        if node.presence_composting.solution_value() > 0:
            discription += '\ncomposting'
        pos[node.node_id] = node.position
        labels[node.node_id] = discription
        print(f'node {i + 1} landfill waste amount: {network[i + 1].waste_landfill.solution_value()}')
        print(f'node {i + 1} incinerator waste amount: {network[i + 1].waste_incinerator.solution_value()}')
        print(f'node {i + 1} recycling waste amount: {network[i + 1].waste_recycling.solution_value()}')
        print(f'node {i + 1} composting waste amount: {network[i + 1].waste_composting.solution_value()}')
        for j in range(node_num):
            dest = network[j + 1]
            if node.user_outflow_incinerator[j + 1].solution_value() > 0:
                G.add_edge(node.node_id, dest.node_id, weight=node.user_outflow_incinerator[j + 1].solution_value(),
                           type='incinerator')
            if node.user_outflow_recycling[j + 1].solution_value() > 0:
                G.add_edge(node.node_id, dest.node_id, weight=node.user_outflow_recycling[j + 1].solution_value(),
                           type='recycling')
            if node.user_outflow_composting[j + 1].solution_value() > 0:
                G.add_edge(node.node_id, dest.node_id, weight=node.user_outflow_composting[j + 1].solution_value(),
                           type='composting')
            landfill = node.incinerator_outflow_landfill[j + 1].solution_value() + node.recycling_outflow_landfill[
                j + 1].solution_value() + \
                       node.composting_outflow_landfill[j + 1].solution_value() + node.user_outflow_landfill[
                           j + 1].solution_value()
            if landfill > 0:
                G.add_edge(node.node_id, dest.node_id, weight=landfill, type='landfill')
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos, labels=labels)
    nx.draw_networkx_edges(G, pos, edge_color='red')
    plt.show()
    print("haha")



