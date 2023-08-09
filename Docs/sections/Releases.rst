Releases
++++++++
.. _sec_releases:

How to cite
===========

In the academic spirit of collaboration, the source code should be appropriately acknowledged in the resulting scientific disseminations.
You may cite it as follows:

* [1], for general reference to the EnergyScope project and the EnergyScope modeling framework :cite:`Limpens2019`
* [2], for reference to the origins of the EnergyScope project or to the first online version of the calculator energyscope.ch :cite:`Girones2015`
* [3], for reference to the energyscope MILP modeling framework :cite:`Moret2016`
* [4], for reference to the current code :cite:`Limpens2021thesis`


[1] G. Limpens, S . Moret, H. Jeanmart, F. Maréchal (2019). EnergyScope TD: a novel open-source model for regional energy systems and its application to the case of Switzerland. https://doi.org/10.1016/j.apenergy.2019.113729	

[2] V. Codina Gironès, S. Moret, F. Maréchal, D. Favrat (2015). Strategic energy planning for large-scale energy systems: A modelling framework to aid decision-making. Energy, 90(PA1), 173–186. https://doi.org/10.1016/j.energy.2015.06.008   	

[3] S. Moret, M. Bierlaire, F. Maréchal (2016). Strategic Energy Planning under Uncertainty: a Mixed-Integer Linear Programming Modeling Framework for Large-Scale Energy Systems. https://doi.org/10.1016/B978-0-444-63428-3.50321-0  	

[4] G. Limpens (2021). Generating energy transition pathways: application to Belgium. PhD thesis Université Catholique de Louvain. http://hdl.handle.net/2078.1/249196


You are welcome to report any bugs related to the code or documentation to the following:
by submitting an issue on the github repository.

You can also contact us:
moret.stefano@gmail.com or gauthierLimpens@gmail.com

License
=======

Copyright (C) <2018-2021> <Ecole Polytechnique Fédérale de Lausanne (EPFL), Switzerland and Université catholique de Louvain (UCLouvain), Belgium>

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License

Codes versions
==============
- first release (v1, monthly MILP) of the EnergyScope (ES) model: https://github.com/energyscope/EnergyScope/tree/v1.0 . See :cite:t:`Moret2017PhDThesis`.
- second release (v2, hourly LP) of the EnergyScope (ES) model: https://github.com/energyscope/EnergyScope/tree/v2.0 .	See :cite:t:`Limpens2019`.
- second release with energy system improvment (v2.1 Energy system update) of EnergyScope (ES) model: https://github.com/energyscope/EnergyScope/tree/v2.1 . See :cite:t:`Limpens_belgian_2020`.
- second release with energy system improvment (v2.2 Energy system update) of EnergyScope (ES) model: https://github.com/energyscope/EnergyScope/tree/v2.2 .


Authors: 

- Stefano Moret, Ecole Polytechnique Fédérale de Lausanne (Switzerland), <moret.stefano@gmail.com> 
- Gauthier Limpens, Université catholique de Louvain (Belgium), <gauthierLimpens@gmail.com>  
- Paolo Thiran, Université catholique de Louvain (Belgium)
- Xavier Rixhon, Université catholique de Louvain (Belgium)

Model utilisation
=================

The following describes the different model versions. They are regrouped in three categories:

- the **model extensions published**

- the **model extensions unpublished**

- the **model applications** per country (scenario analaysis and robust optimisation)


Model extensions (published)
----------------------------

The EnergyScope TD models account for two published model extension:
(name in **bolt** are the active developers)


- **Pathway optimisation**: *EnergyScope Pathway* enables optimising the energy system from an existing year (usually 2015)
  to a future target year. :cite:t:`Limpens2021thesis` developed a model that extended EnergyScope TD into a big linear model representing 8 representative years from 2015 to 2050.
  The overall transition is optimised at once with a perfect foresight on technology performances (prices, efficiency,...), resources prices, energy demand ...
  :cite:t:`li2022dynamic` proposed a Conditional multi-stage optimisation that simulates the evolution of energy transitional pathways flexibly in case the evolution diverts from the planned posterior.
  
  **Main contributors**: **Gauthier Limpens**, Li Xiang, **Xavier Rixhon** see :cite:`Limpens2021thesis,li2022dynamic`

- **Multi-region**; *EnergyScope Multi-Cells* allows the representation of several region at once.
  The regions are resolved simultaneously with the exchanges of several energy carriers (usually electricity, molecules and wood).
  The new model was first developped by :cite:t:`thiranenergyscope` on a fictive case, then extended to the Western Europe region with a 6-cells resolution, see :cite:t:`cornet2021energy`.
  It has also been applied in other studies on different regions :cite:`thiran2021flexibility, thiran2023validation`. A European version is currently under development.
  
  **Main contributors**: **Paolo Thiran**, see :cite:`thiranenergyscope,cornet2021energy,thiran2021flexibility, thiran2023validation`

  **Other contributors**: Aurélia Hernandez, Noé Cornet, Pauline Eloy, Jeroen Dommisse, Jean-Louis Tychon.

- **Carbon flow**: Adding mass carbon balance to all technologies, splitting different types of carbon, allowing monitoring of effective emissions, carbon reuse, and sequestration.
  Two different formulation are proposed, in the present model, :cite:t:`Limpens_belgian_2020` implemented a formulation represented in :numref:`Figure %s <fig:CO2andPtGLayers>` that captures the carbon cycle for synthetic fuels.
  More exhaustively, :cite:t:`li2020decarbonization` proposed a full carbon flow capturing all the energy-related carbon flow in a national system.

  **Main contributors**: Xiang Li and **Gauthier Limpens**, see :cite:`li2020decarbonization,Limpens_belgian_2020`

- **Grid infrastructure**: Splitting and characterisation of the national grid infrastructure by different power levels (electricity, methane and hydrogen).  The problem can optimise the investment in each infrastructure, which opens the competition among small-decentralised system and large scale.
  Also it allows the possibility to compete different energy carriers grids, such as electricity versus gas.

 **Main contributors**: **Jonas Schnidrig**, see :cite:`schnidrig2023role`

Model extensions (unpublished)
------------------------------

- **Agent based**: is a framework is needed to assess decisions, uncertainties, and shocks.
  A reinforcement-learning agent interacts with the EnergyScope model, making decisions every five years from 2020 to 2050.
  Actions taken every five years impact the system for the next ten years, and intermediate solutions serve as starting points
  for subsequent decisions. By exploring different action sequences, the agent develops a robust sustainability policy,
  considering environmental parameter variations.

  **Main contributors**: **Xavier Rixhon**.

- **Multi-criteria**: Use of additional criteria such as Global Warming Potential, embodied energy, etc. :cite:t:`muyldermans2021multicriteria` initiated the work
  by collecting Life Cycle Assessment (LCA) data for most resources and technologies based on the EcoInvent database.
  Building on the collected data, :cite:t:`dumas2022energy` analysed the Belgian energy transition using the Energy Return on Investment (EROI) indicator and compared it with cost indicators.
  Schnidrig built a similar database that integrates and distinguishes Scope 1, 2, and 3 LCA emissions of resources and technologies. In their work, they used a Multi-Objective Optimization technique to analyze the case study of Switzerland (publication forthcoming).
  In ongoing work, Ghuys and Souttre are improving previous work and are developing an integrated and dynamically adaptive LCA database used in EnergyScope.

  **Main contributors**: Dumas Jonathan,  **Schnidrig Jonas**, **Mathieu Souttre**  and **Ghuys Nicolas**.

  **Other contributors**: Dubois Antoine.

- **Soft coupling with Dispatch model** (`DispaSET <dispaset.eu>`_): this approach was initially introduced in the work of :cite:t:`coates2020energy`, and later extended in the research by :cite:t:`pavivcevic2022bi`.
  The soft coupling involves an automatic interaction between EnergyScope and DispaSET. EnergyScope optimizes the system design, while DispaSET verifies the operability. This automatic feedback loop enhances the sizing accuracy in EnergyScope to account a stable dispatch, and vice versa.

  **Main contributors**: Matija Pavicevic and Thiran Paolo

- **Soft coupling with Macro-economic model** (`GEMMES <https://www.afd.fr/en/ressources/modelling-small-open-developing-economies-financialized-world-stock-flow-consistent-prototype-growth-model>`_):
  GEMMES (General Monetary and Multisectoral Macrodynamics for the Ecological Shift) is a macro-economic tool that estimates the impact of public decisions on the economy of a given country. Coupling the models will allow to assess how the energy
  transition affects the economic environment in which it takes place and vice versa. As an example, deploying additional renewable energies, such as solar and wind, might affect the country's balance of payments, with consequences on the
  exchange rate and thus possibly on inflation and on the interest rate taken as input by EnergyScope.

  **Main contributors**: Pierre Jacques, see :cite:`godin2020modelling`

- **Soft coupling with district energy models** (REHO): The integration of REHO into the system allows for enhanced accuracy at the building level by effectively capturing the energy demand of buildings. Additionally, REHO facilitates the reconciliation between national estimations of energy hubs (such as district heating networks and energy communities) and their actual implementation.
  This work is under development, see :cite:`chuat2023impact`

  **Main contributors**: Schnidrig Jonas and Chuat Arthur

- **Soft coupling with industry model**: The integration of industry into the system involves the incorporation of industrial prosumer configurations based
  on the results of the AIDRES project. This approach entails replacing the energy demands of the industry with the production capacity offered by the industry.
  In simpler terms, it means that the terawatt-hours (TWh) of heat or electricity traditionally consumed by the industry will be replaced by kilo-tons of materials required for production.

  **Main contributors**: Schnidrig Jonas

Model Applications
------------------

The model has been applied to the following countries:

- Switzerland:
  
    * *Robust optimisation design*: Moret developed a framework to integrate uncertainties in energy models. The framework accounts for uncertainty characterisation, sensitivity analysis and robust optimisation. See :cite:t:`Moret2017PhDThesis`.
    * *Scenario analysis and storage needs*: see for the main study :cite:t:`Limpens2019` and :cite:t:`Limpens_role_2019` for a specific study on the storage.
    * *Role of the grid infrastructure in the transition*: see :cite:t:`schnidrig2023role`.
    * *Carbon flow of an independent and carbon neutral Switzerland*: see :cite:t:`li2020decarbonization`.
    * *Dynamic optimisation of the transition*: see :cite:t:`li2020decarbonization`.

- Belgium:
  
    * *Scenarios analysis*: see :cite:t:`Limpens_belgian_2020` who analysed different scenarios to reduce greenhouse gases emissions.
    * *Uncertainty*: see :cite:t:`limpens2020impact` for the elaboration of the methodology to the Belgium case (using a novel methodology), see :cite:t:`rixhon2021role` for a specific study on electro-fuels and see :cite:t:`limpens2020impact,Limpens2021thesis` for an updated study on the Belgian case.

- Italy:
  
    * *Scenarios analysis*: see :cite:t:`borasio2022deep` for an exhaustive analysis (per regions and with uncertainty) to reduce the energy system at the horizon of 2050.
    * *Multi-region analysis*: see :cite:t:`thiran2021flexibility` for an application of the Multi-cell model to a three region case.

- Spain:
  
    * *Scenario analysis*: see :cite:t:`rosello2021study` for different scenarios of transition in Spain.

- Other countries:
  
    * *European Union countries* see :cite:t:`dommissemodelling` for a data collection and results for 26 european countries.
  



