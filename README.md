Waste-Disposal-Optimization
## Introduction

### Background
Solid waste managment remains a critical challenge for urban environments worldwide. With the urban population increasing at an unprecedented rate, it is becoming increasingly urgent to effectively deal with the waste generated by the rapidly growing population. 

### Problem Statement
Shengsi island is a tourism island that faces issues that hinders the effectiveness if its solid waste management system. 66 thousand resident people and the increasing number of tourists on Shengsi Island have led to a decline in the efficiency of the waste disposal system, which has had a serious impact on the island's environment with more than 30,000 kilograms of waste to be disposed of each year. The area of Shengsi island is 8824 square kilometer.

### Objective
This study aims to address the multi-level locational planning problem of an intergrated waste management system in Shengsi island using MILP(mixed integer linear programming). The objective is to integrate various apsects of waste management, cosidering environmental, economic and logistical factors to propose a comprehensive solution.

### Literature Reivew

We categorize previous study according to the method provided by Ghiani, G[1]. 

The first category "p" corresponds to the periodicity of the problem: p=1 if there is only one cycle, and p=T if more than one cycle is considered. the second category "s" is related to the network structure, which can be subdivided into four categories:

C, if we considered the optimal location of the new collection point.

S, if we considered existing or new transfer stations.

P, if we evaluated the opening of new processing facilities or the optimization of existing processing facilities.

L, if we considered existing or new landfill, disposal or market facilities.

The third category "c" describes additional constraints and characteristics of the problem, which can refine the classification again:

"multiwaste", if we considered multiple types of waste.

"uncert", if there is uncertainty in waste generation.

The last category "o" represents the optimization objective of this problem:

TC, if it minimized transportation costs.

PC, if it consider the processing costs of the facility.

FC, if it includes fixed costs of operating existing facilities or opening new facilities.

"multiobj", if we consider multi-objective optimization.

Caruso[2] developed a solid waste management (SWM) planning system comprising three hierarchical levels. This system aimed to efficiently address the complexities of waste management by integrating processes at various stages, from collection to disposal. Through this three-tiered approach, Caruso sought to optimize resource allocation, enhance operational effectiveness, and mitigate environmental impacts associated with waste management practices.

Based on the provided classification system, this can be categorized as follows:

p: Single period.

s: No specific subfields mentioned.

c: No additional constraints or characteristics specified.

o: No specific optimization objectives mentioned.

L: Existing Landfill considered.

TC,FC: Minimized transportation costs and incorporated fixed costs related to existing facility operations or new facility openings,

Therefore, it falls under the category 1/P,L/multiwaste/TC,FC, multiobj model.

Mitropoulos[3] developed an integrated solid waste management (SWM) system operating across four hierarchical levels at the regional scale. This comprehensive system aimed to address the multifaceted challenges of waste management by incorporating strategic planning, logistical coordination, and sustainable practices at each level. By integrating collection, sorting, treatment, and disposal processes within a regional framework, Mitropoulos aimed to optimize resource utilization, minimize environmental impacts, and enhance the overall efficiency and effectiveness of solid waste management practices within the region.

Based on the provided classification system, this can be categorized as follows:

p: Single period.

s: It includes C and L, indicating consideration of optimal locations for new collection points and existing or new landfill, disposal, or market facilities.

c: No additional constraints or characteristics are mentioned.

o: No specific optimization objectives are mentioned.

S,P,L: Transfer stations, Processing plant, Landfill considered.

TC,FC: Minimized transportation costs and incorporated fixed costs related to existing facility operations or new facility openings,

Therefore, it falls under the category "1/S,P,L/–/TC,FC MIP" model.

### Scope
This study refines the solid waste management system on Shengsi Island through a detailed analysis of waste generation, leveraging the actual coordinates of existing waste collection centers and sophisticated geospatial data analysis. Notably, the study employs the Google OR-Tools SAT solver to model and solve the Mixed Integer Linear Programming (MILP) problem, facilitating an innovative approach to estimating waste generation based on the distribution of residential areas.
![image](https://github.com/Minefix049/Waste-Disposal-Optimization/blob/main/case.png)

## Methodology

This study refines the solid waste management system on Shengsi Island through a detailed analysis of waste generation, leveraging the actual coordinates of existing waste collection centers and sophisticated geospatial data analysis. Notably, the study employs the Google OR-Tools SAT solver to model and solve the Mixed Integer Linear Programming (MILP) problem, facilitating an innovative approach to estimating waste generation based on the distribution of residential areas.

### Geography data collection
A critical component of our methodology is the collection of accurate and comprehensive data regarding Shengsi island's geography, infrastructure and wate generation patters. To achieve this, we have emplyed the services of Gaode, a leading provider of mapping and location-based services in china. We find out the latitude and longitude coordinates of exisitng collection centers on Gaode Map. We also define the polygons to represent operational coverage areas of each collection centers. Moreover we use polygon serach methods provided by Gaode API to collect the data of residential facilities in each operation coverage area. We also use Gaode API to compute the distance matrix of location candidates.

### Utilizating Existing Collection Centers
Our methodology is based on utilizating existing waste collection centers on Shengsi Island. We use real coordinates of these centers to accurately divide the island into sectors and mak sure that each sector is efficiently served. These sectors are delineated based on the operational coverage of each collection center, using polygon coordinates to define their geographical boundaries precisely.

### Collection and Analysis of Residential Area Data
The estimation of waste generation begins with a comprehensive collection of data on residential areas within each defined sector. Through the Gaode polygon search API, we gather detailed information on residential units, employing specific keywords to ensure a thorough identification of all relevant residential entities. This method allows for an accurate representation of the residential landscape within each sector.

### Estimating Waste Generation with Residential Count Ratios
A key innovation in our methodology is the estimation of waste generation through the ratio of residential counts in each sector. This approach allows for a proportional and realistic assessment of waste production, acknowledging the varying population densities and residential distributions across the island. By correlating the number of residential units to estimated waste output, we offer a nuanced view of waste generation that surpasses traditional, uniform estimations.

### collection of distance matrix data
A critical aspect of our study involved the acquisition of accurate and comprehensive data pertaining to Shengsi Island's geography, infrastructure, and waste generation patterns. This section outlines the methodologies employed to gather the requisite data and the tools utilized for analysis.We utilized Gaode's API to compute distance matrices between potential facility sites and waste generation centroids, employing advanced routing algorithms and geographic data. This enabled us to optimize facility placement, minimizing transportation costs and logistical challenges in designing a solid waste management system for Shengsi Island.

### MILP Modeling with Google OR-Tools SAT Solver
To support the analytical processes of this study, we employ the Google OR-Tools SAT solver for modeling and solving the MILP problems inherent in estimating waste generation and optimizing collection center operations. This powerful tool enables us to handle complex optimization problems efficiently, providing a robust framework for the strategic planning and management of the island's waste management system. The use of Google OR-Tools SAT solver underpins our methodological approach, enhancing the precision and effectiveness of our waste generation estimates and sector-based management strategies.

### Comprehensive Approach for Solid Waste Management Optimization
Integrating real-world data on collection centers with advanced modeling and analytical techniques, this study presents a comprehensive approach to optimizing solid waste management on Shengsi Island. By accurately estimating waste generation and employing sophisticated MILP modeling, we lay the groundwork for a more efficient, targeted, and sustainable waste management infrastructure that is finely tuned to the specific needs and characteristics of the island's sectors.

### Residue Rate

The reduction factor, representing the residue rate, signifies the proportion of material remaining after waste processing methods such as incineration (10%), composting (20%), and recycling (30%). It serves as a critical parameter in evaluating the efficiency of these processes and determining the extent of waste reduction achieved through them.

## Mathematical Formulation

Based on the modeling method in literature review, considering the actual requirements of shengsi island, we decided to use 1/P,L/-/TC,PC,FC MIP model to solve the locational planning of SWM system in shengsi island. Because of the limited landspace in Shengsi island, this study didn't consider the requirements of transfer station in this model. The model can be fourmulated as follow. 

### Indices and Sets
• $J$: Set of collection centers

• $K$ : Set of transfer stations (not used in this scenario)

• $F$ : Set of treatment plant candidates by the seaside

• $L$ : Set of landfill candidates

• $G$ : Set of treatment types, $G$ ={" $incinerator$"," $composting$"," $recycling$"}

### Parameters
• $d_{j, f}$: Distance from collection center $j$ to treatment plant $f$

• $d_{j,L}$: Distance from collection center $j$ to landfill $l$

• $d_{f,L}$: Distance from treatment plant $f$ to landfill $l$

• $C_T$: Transport cost per unit distance per ton of waste

• $C_{F,g}$: Fixed cost of operating treatment type $g$

• $C_{V,g}$: Variable cost of processing waste at treatment type $g$

• $C_L$: Cost of landfilling per ton of waste

• $W_j$: Waste generated at collection center $j$

• $CAP_{F,g}$: Capacity of treatment plant for treatment type $g$

• $CAP_L$: Capacity of landfill

### Decision Variables

• $x_{j,f,g}$: Tons of waste transported from collection center $j$ to treatment plant $f$ for treatment type $g$

• $y_{j,l}$: Tons of waste transported from collection center $j$ to landfill $z$

• $z_{f,l,g}$: Tons of waste transported from treatment plant $f$ to landfill $l$ after processing with treatment type $g$

• $b_{f,g}$: Binary variable indicating if treatment plant $f$ for treatment type $g$ is selected



### Objective

Minimize:
$\sum_{j\in J}\sum_{f\in F}\sum_{g\in G}C_T·d_{j,f}·x_{j,f,g}+\sum_{j\in J}\sum_{l\in L}C_T·d_{j,l}·y_{j,l}$
$+\sum_{f\in F}\sum_{l\in L}\sum_{g\in G}C_T·d_{f,l}·z_{f,l,g}$
$+\sum_{f\in F}\sum_{g\in G}(C_{F,g}·b_{f,g}+C_{V,g}·x_{j,f,g})+\sum_{j\in J}\sum_{l\in L}C_L·y_{j,l}$

### Constraints
• Waste Generation and Allocation Constraint for Each Collection Center:
$\sum_{f\in F}\sum_{g\in G}x_{j,f,g}+\sum_{l\in L}y_{j,l}=W_j\ \ \forall j\in J$

• Treatment Plant Capacity Constraint:
$\sum_{j\in J}x_{j,f,g}\leq CAP_{F,g}·b_{f,g}\ \ \forall f\in F, \forall g \in G$

• Landfill Capacity Constraint:
$\sum_{j\in J}y_{j,l}+\sum_{f \in F}\sum_{g\in G}z_{f,l,g}\leq CAP_L\ \ \forall l\in L$

• Treatment to Landfill Transport:
$z_{f,l,g}=\alpha_{g}·\sum_{j\in J}x_{j,f,g}\ \ \forall f\in F,\forall l\in L,\forall g\in G$
Where $a_g$ is the reduction factor after treatment $g$.

• Binary Treatment Plant Selection:
$b_{f,g}\in\{0,1\}\ \ \forall f\in F,\forall g\in G$

• Landfill Count Upper Bound:
Let $L_{max}$ be the maximum number of landfill sites that can be selected for use.

• Landfill Selection Upper Bound Constraint:
$\sum_{l\in L}u_l\leq L_{max}$

## Result

This paper utilizes existing waste collection centers on Shengsi Island. We use real coordinates of these centers to divide the island into sectors and mak sure that each sector is efficiently served.   By correlating the number of residential units to estimated waste output, we estimate the waster generation in each sector. The data of existing collection centers and their corresponding operational coverage areas are as follow.

### Existing collection centers and operational coverage areas

| Index | Polygon Coordinates                                       | Residential areas count | Waste generation estimation per year(ton) |
|-----|-----------------------------------------------------------|-------------------------|-----------------------------|
|  1  | 122.447,30.768 \| 122.474,30.768 \| 122.474,30.743 \| 122.447,30.743 | 25                      | 1202                        |
|  2  | 122.490,30.725 \| 122.538,30.725 \| 122.538,30.696 \| 122.490,30.696 | 26                      | 1245                        |
|  3  | 122.423,30.725 \| 122.423,30.689 \| 122.467,30.689 \| 122.467,30.725 | 254                     | 12209                       |
|  4  | 122.423,30.745 \| 122.447,30.745 \| 122.447,30.743 \| 122.467,30.743 \| 122.467,30.725 \| 122.423,30.725 | 260 | 12498                |
|  5  | 122.490,30.725 \| 122.467,30.725 \| 122.467,30.696 \| 122.490,30.696 | 87                      | 4182                        |
|  6  | 122.409,30.689 \| 122.435,30.689 \| 122.435,30.673 \| 122.409,30.673 | 0                       | 0                           |

### Process plant and landfill candidate selection
We selected several location candidates for both process plant and landfill by considering following criteria.

• Environmental Impact: Candidate locations were chosen to minimize disturbance to inland ecosystems and residential areas. 

• Land Use Efficiency: Sites were selected to avoid conflicts with residential and conservation areas, optimizing land utilization. 

• Energy and Resource Recovery: Coastal locations were preferred to utilize seawater for cooling processes and maximize energy and resource recovery opportunities. 

These criteria ensure the selected locations contribute to sustainable waste management while minimizing environmental impact and maximizing resource efficiency on Shengsi Island.

Here's the coordinate of candidate we selected.

| ID  | Coordinates       |
|-----|-------------------|
| 1   | 122.467, 30.752  |
| 2   | 122.440, 30.740  |
| 3   | 122.464, 30.729  |
| 4   | 122.442, 30.712  |
| 5   | 122.533, 30.703  |
| 6   | 122.463, 30.692  |


### Distance Matrix

We planned waste routes using Gaode API, obtaining two crucial distance matrices. We selected Strategy 13 - No Highway- to plan the route in case of considering city capacity. By inputting waste processing points' coordinates, we obtained shortest path distances, forming matrices. 

The Waste Collection Distance Matrix illustrates straight-line distances between processing points. 

The Landfill Processing Plant Distance Matrix shows distances from processing points to the landfill. 

These matrices support waste disposal planning, aiding decision-makers in strategy formulation and route optimization for enhanced efficiency and environmental sustainability.


#### Waste Collection Distance Matrix：

| Distance Matrix         | Point 1 | Point 2 | Point 3 | Point 4 | Point 5 | Point 6 |
|-------------------------|---------|---------|---------|---------|---------|---------|
| Collection Process      | 2851.0  | 2326.0  | 4095.0  | 7257.0  | 14993.0 | 10578.0 |
|                         | 15151.0 | 12210.0 | 10093.0 | 14769.0 | 2161.0  | 8792.0  |
|                         | 10110.0 | 10955.0 | 4998.0  | 6027.0  | 11685.0 | 1780.0  |
|                         | 5505.0  | 2624.0  | 1159.0  | 7555.0  | 12048.0 | 5758.0  |
|                         | 10495.0 | 6963.0  | 4366.0  | 11548.0 | 8571.0  | 2822.0  |
|                         | 14075.0 | 10543.0 | 10607.0 | 5615.0  | 16103.0 | 6088.0  |


#### Landfill Processing Plant Distance Matrix：

| Distance Matrix               | Point 1 | Point 2 | Point 3 | Point 4 | Point 5 | Point 6 |
|--------------------------------|---------|---------|---------|---------|---------|---------|
| Process to Landfill           | 2851.0  | 2326.0  | 4095.0  | 7257.0  | 14993.0 | 10578.0 |
|                                | 15151.0 | 12210.0 | 10093.0 | 14769.0 | 2161.0  | 8792.0  |
|                                | 10110.0 | 10955.0 | 4998.0  | 6027.0  | 11685.0 | 1780.0  |
|                                | 5505.0  | 2624.0  | 1159.0  | 7555.0  | 12048.0 | 5758.0  |
|                                | 10495.0 | 6963.0  | 4366.0  | 11548.0 | 8571.0  | 2822.0  |
|                                | 14075.0 | 10543.0 | 10607.0 | 5615.0  | 16103.0 | 6088.0  |

### Model Parameters
#### Cost Parameters
This sector introduces the various cost parameters and constraint parameters in the optimization models. The cost parameters can be divided into several categoris.

•  Processing Cost:  The variable treatment cost of incinerator is $350$ yuan/ton, while for composting is $250$ yuan/ton and $100$ yuan/ton for recycling plants. The variable treatment of landfill is $250$ yuan/ton.

•  Transportation Cost: The transportation cost of vehicles running between collection centers and processing plants is $7$ yuan/ton * km. The transportation cost of trucks running between processing plants and landfill sites is $30$ yuan/ton * km.

•  Fixed Cost: The fixed cost to invest an incinerator treatplant is $135000000$ yuan. Cosidering its lifecycle expanding 100 years, the fixed cost each year is $1350000$ yuan then. 

  The fixed cost to invest an composting treatplant is $200000000$ yuan. Considering its lifecycle expanding 100 years, the fixed cost each year is $12000000$ yuan then.

  The fixed cost to invest an landfill is $120000000$ yuan according to national data files. Considering its lifecycle expanding 100 years, the fixed cost each year is $1200000$ yuan then.

  The fixed cost to invest an landfill is $19500000$ yuan according to national data files. Considering its lifecycle expanding 100 years, the fixed cost each year is $195000$ yuan then.

#### Operation Constraints

This paper considers multiple constrains not only as  feasibility guarantees, but also as cutting planes. These constraints are as follow.

•  Landfill Capacity: The bounds for landfill capacity, ranging from a lower limit of 0 to an upper limit of 11,000 tons, are established based on insights from the study by Kollikkathara, Feng, and Yu[4].

•  Compost Capacity: Compost capacity is governed by lower and upper bounds of 100 tons and 600 tons per day, respectively, drawn from the research findings presented by Aleluia and Ferrão [5].

•  Incineration Capacity: The lower and upper bounds for incineration capacity, set at 100 tons and 600 tons per day, respectively, are derived from the investigations detailed in the study by Aleluia and Ferrão [6].

•  Recycing Capacity: The lower and upper bounds for incineration capacity, set at 100 tons and 600 tons per day, respectively, are derived from the investigations detailed in the study by Aleluia and Ferrão [6].

•  Landfill site count limit: This papre finds it hard to accurately measure the environment impact of solidwaste landfill so this paper constraints the count limit of landfill site to limit the impat of solidwaste landfill. The effect of landfill constraint will be discussed in computational result.

## Computational Result
In case of 1 landfill site limitation, the model finds no feasible solution because of the capacity limit of single landfill site.

In case of 2 landfill site limitation, the optimization yielded an optimal objective value of 3,363,562.866, which represents the minimum cost (in yuan) in a year associated with the solid waste management system under the given constraints. Notably, the results reveal a varied utilization of treatment technologies across the different candidate locations for treatment plants and highlight a selective approach to landfill usage.

Incinerator capacity was partially used at candidate locations 1 and 2, with 290 tons and 600 tons processed, respectively. This suggests that incineration, despite its high efficiency in volume reduction, was not the most cost-effective option across all scenarios due to either its higher operational costs or the limited waste suitable for incineration. Both Composting and Recycling technologies were maximally utilized (600 tons each) across most candidate locations, indicating a preference for these treatment methods. This could be due to lower operating costs, higher material recovery rates, or policy incentives for recycling and composting.

Two landfills were utilized, with disposal capacities of 9,986 tons and 14,591 tons, respectively. This aligns with the constraint of not exceeding two landfills, focusing on minimizing the environmental impact and costs associated with landfills. The selection of these two landfills could be justified by their proximity to waste generation sources or treatment facilities, reducing transportation costs.

In case of 3 landfill site limitation, the objective value has significantly decreased to 1,655,002.519 from 3,363,562.866 when the landfill count limit was two. This substantial reduction in cost indicates that allowing an additional landfill site enables more cost-effective waste disposal options, possibly due to reduced transportation distances for some of the waste or the utilization of landfills with lower operational costs.

In contrast to the previous results where composting, recycling, and incineration were utilized to varying degrees across different sites, this scenario shows a predominant focus on recycling, with processing occurring at only one candidate location (600 tons processed) and a smaller amount at another (110 tons). This change suggests that with more landfill options available, the model finds it more cost-effective to dispose of waste directly rather than process it through composting or incineration.
Reduced Treatment Diversity: The near-exclusive reliance on recycling in this scenario, with no waste processed through composting or incineration, reflects a strategic shift towards direct disposal in landfills, presumably because this option became more economically viable with the increased landfill availability.

With the landfill count limit increased to three, the model optimizes the use of three landfills, with disposal capacities of 9,199 tons, 8,215 tons, and 13,425 tons, respectively. This expanded utilization demonstrates the model’s flexibility in leveraging additional landfill capacity to minimize overall costs.

While increasing the number of landfills used can reduce transportation and operational costs, it also raises considerations regarding the environmental impact. More active landfills could mean a greater potential for land degradation and pollution unless managed with state-of-the-art containment and treatment technologies.

 The reduced objective value highlights a trade-off between minimizing costs and managing the environmental footprint. Allowing more landfills can lower costs but potentially at the expense of increased environmental impacts, emphasizing the need for careful policy and management decisions that balance these factors.


## Reference
[1]Ghiani, G., Laganà, D., Manni, E., Musmanno, R., & Vigo, D. (2014). Operations research in solid waste management: A survey of strategic and tactical issues. Computers & Operations Research, 44, 22-32.

[2]Caruso, C., Colorni, A., & Paruccini, M. (1993). The regional urban solid waste management system: A modelling approach. European journal of operational research, 70(1), 16-30.

[3]Mitropoulos, P., Giannikos, I., & Mitropoulos, I. (2009). Exact and heuristic approaches for the locational planning of an integrated solid waste management system. Operational Research, 9, 329-347.

[4]Kollikkathara, N., Feng, H., & Yu, D. (2010). A system dynamic modeling approach for evaluating municipal solid waste generation, landfill capacity and related cost management issues. Waste management, 30(11), 2194-2203.

[5]Aleluia, J., Ferrão, P. Assessing the costs of municipal solid waste treatment technologies in developing Asian countries. Waste Management (2017)

