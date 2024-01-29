Waste-Disposal-Optimization
## Introduction
### Background
Solid waste managment remains a critical challengr for urban environments worldwid. ...
### Problem Statement
Shengsi island as as a tourism  island faces issues that hinders the effectiveness if its  solid waste management system. ... introduce data in shengsi island.  
### Objective
This study aims to address the multi-level locational planning problem of an intergrated waste management system in Shengsi island using milp(mixed integer linear programming). The objective is to integrate various apsects of waste management, cosidering environmental, economic and logistical factors to propose a comprehensive solution.
### Literature Reivew
Caruso[1] developed a a SWM planning system of 3 levels.
Mitropoulos[2] developed a  an integrated SWM system of 4 levels at the regional level. By identifying the system units needed along with the sites where these units will be constructed, this work minimized the overall SVM cost including transportation costs,  fixed
operation and maintenance costs of transfer station and treatment plants as well as the landfill costs which correspons to the enviromental effects of SVM system.
### Scope
The scope of this research encompasses the applicatioon of open sourced solver like ortools on the milp model tailored to the specific conditions of shengsi island. This study contributes to the improvement of local waste management practrices in Shengsi island. 
## Methodology
### MILP Formulation
Based on the model developed by Mitropoulos, the MIP location allocation models are as follows.  Because of the limited landspace in Shengsi island, this study didn't consider the requirements of transfer station in this model.
### Data Collection
A critical component of our methodology is the collection of accurate and comprehensive data regarding Shengsi island's geography, infrastructure and wate generation patters. To achieve this, we have emplyed the API services of Gaode, a leading provider of mapping and location-based services in china.
we use polygon serach methods provided by Gaode API to collect the data of wate generation distribution. We also used Gaode API to compute the distance matix of location candidates.
## Computational study
![image](https://github.com/Minefix049/Waste-Disposal-Optimization/assets/30038539/3faa29fe-5da4-4c4c-8072-019140689d59)# 
This study used the data of Shengsi island collected from Gaode API to optimize the location planning of process plant and landfill site. For  fast converge of the model. we introduced an artificial cuts to the model by constraining the number of landfill sites.
In case of 1 landfill, ...
In case of 2 landfill, ...
## Discusion
### Comparison with existing solutions
### Implications
Discuss the implications of this finding for policy, practive adn future research.
