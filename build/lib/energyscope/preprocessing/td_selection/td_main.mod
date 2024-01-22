# -------------------------------------------------------------------------------------------------------------------------													
#	EnergyScope TD is an open-source energy model suitable for country scale analysis. It is a simplified representation of an urban or national energy system accounting for the energy flows												
#	within its boundaries. Based on a hourly resolution, it optimises the design and operation of the energy system while minimizing the cost of the system.												
#													
#	Copyright (C) <2018-2019> <Ecole Polytechnique Fédérale de Lausanne (EPFL), Switzerland and Université catholique de Louvain (UCLouvain), Belgium>
#													
#	Licensed under the Apache License, Version 2.0 (the "License");												
#	you may not use this file except in compliance with the License.												
#	You may obtain a copy of the License at												
#													
#		http://www.apache.org/licenses/LICENSE-2.0												
#													
#	Unless required by applicable law or agreed to in writing, software												
#	distributed under the License is distributed on an "AS IS" BASIS,												
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.												
#	See the License for the specific language governing permissions and												
#	limitations under the License.												
#													
#	Description and complete License: see LICENSE file.												
# -------------------------------------------------------------------------------------------------------------------------																								

#----------------------------------------------------------------------------------
# TYPICAL DAY SELECTION
# from F. Dominguez-Munoz et al., Selection of typical demand days for CHP optimization, 2011
#----------------------------------------------------------------------------------

############################
###  MILP formulation    ###
############################
set DIMENSIONS ;		# Number of input data per day (24h x nbr of time series)
set DAYS := 1 .. 365;			# Number of days 

### parameters
param Nbr_TD default 12; 				#Number of TD days
param Ndata{DAYS,DIMENSIONS}; 			#Input data (already normalized)
param Distance{i in DAYS,j in DAYS} := sum{k in DIMENSIONS}((Ndata[i,k]-Ndata[j,k])*(Ndata[i,k]-Ndata[j,k])) ; # Distance matrix.

### Variables
var Selected_TD {DAYS} 				binary;# default 0; #which are the typical days 
var Cluster_matrix {DAYS,DAYS} 		binary;# default 0; #which day corresponds to which typical day

### Constraints 
# Allocate one cluster centre (i) to each day (j) 
subject to allocate_1TD_per_day{j in DAYS}:
	sum{i in DAYS} Cluster_matrix[i,j] = 1;

# If cluster not allocated, it needs to be null 
subject to other_TD_null {i in DAYS,j in DAYS}:
	Cluster_matrix[i,j] <= Selected_TD[i]; 

# Limit the number of TD
subject to limit_number_of_TD:
	sum{i in DAYS} Selected_TD[i] = Nbr_TD;

#-Objective
minimize Euclidean_distance: 
	sum{i in DAYS,j in DAYS} Distance[i,j]*Cluster_matrix[i,j];

 
