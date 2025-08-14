Overview
++++++++
.. _label_sec_overview:

.. warning:: New and updated version of the documentation is available in this `library <https://www.energyscope.net/latest/>`_.

:Version: |version| (|release|)
:Date: |today|
:Version main developer: Gauthier Limpens (UCLouvain)
:Short summary: One cell *whole*-energy system with an hourly resolution and data for the Belgian energy system in 2035.

The EnergyScope model optimises the design and operation of all the energy sectors, with the same level of details. The energy sectors are defined as electricity, heat, mobility and non-energy demand. 


The EnergyScope model is developped through a collaboration between UCLouvain (Belgium) and EPFL (Switerland). 
It was originally created by EPFL (Switzerland) since 2011.

It is written in an algebraic language which can be compiled with an open source solver (GLPK) but also commercial one (AMPL).

Features
========

In the energy system community, several criteria are used to compare models. 
EnergyScope TD is a bottom-up energy system model and has been compared to 53 other models in :cite:`Limpens2021thesis`.

Each model is tailored for a different applications. In the following, the strengths and weaknesses of the model is presented.


Strengths of the model
----------------------


Whole energy system
^^^^^^^^^^^^^^^^^^^


The current version of the energy system represents the four energy sectors of the Belgian energy system. 
The sectors are coupled, in the sence that electricity can be used for other sectors, such as heat or mobility. 
:numref:`Figure %s <fig:bes_illustration>` shows the energy system implemented in the
model, it accounts for :

- 28 energy carriers
- 112 technologies
- 12 end use demands


.. figure:: /images/case_study_energy_system.png
   :alt: Illustrative example of a decentralised heating layer.
   :name: fig:bes_illustration
   :width: 16cm

   Application of the EnergyScope TD to the Belgian energy system: overview of the
   resources, technologies and demands implemented. Technologies (in bold) represent groups of
   technologies with different energy inputs (e.g. Boilers include gas boilers, oil boilers ...). ‘Decent.’
   represents the group of thermal storage for each decentralised heat production technology. Abbreviations:
   Atm. (atmospheric), battery electric vehicle (BEV), combined cycle gas turbine (CCGT),
   CC (carbon capture), carbon capture and storage (CCS) cogeneration of heat and power (CHP),
   district heating network (DHN), hydrogen (H2), heat pump (HP), integrated gasification combined
   cycle (IGCC), methan. (methanation), natural gas (NG), onshore (on.), offshore (off.), plug-in hybrid
   electric vehicle (PHEV), pumped hydro storage (PHS), photovoltaic (PV) and synthetic liquid fuel
   (SLF).

Optimisation of hourly operation over a year
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The formulation of the year is based on typical days, which reduces the number of time-slice accounted in the model (usually 288 hours, which represents 12 days). 
However, a reconstruction method enables to capture energy stored at different time scale. :numref:`Figure %s <fig:estd_time_scale>` illustrates the different time scales captured by the model.

.. figure:: /images/estd_different_time_scales.png
   :alt: Illustrative example of a decentralised heating layer.
   :name: fig:estd_time_scale
   :width: 16cm

   Illustration of the different time scale optimised by the model. 
   The hourly power balance is resolved on typical days (bottom), 
   while the level of charge of storage is captured at week to seasonal level (middle and top).
   This illustration is for the Swiss case study presented in [limpens2019energyScope].

The model optimises the operation and design, enabling all the differnt configuration to satisfy the imposed demand.


Open source
^^^^^^^^^^^

The model is both open source (github) and documented (this document). 
The choosen plateform foster collaboration and enable several researchers to work together.

Short computational time
^^^^^^^^^^^^^^^^^^^^^^^^

The model has a short computational time around **60 seconds** making it an ideal candidate for uncertainty quantification.


Weaknesses of the model
---------------------------

Spatial resolution: 1 cell
^^^^^^^^^^^^^^^^^^^^^^^^^^

The presented model represents a single regional area, called a *cell*. 
This area is connected to neighbouring countries, and assumptions enable 
the representation of imports/exports of electricity and molecules.

Low technico-economico resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The current implementaion has a low level of technico-economic contraints. 
Technically, the technologies can switch from off to full load in one hour (except for Nuclear). 
Economically, the operation is related to the resource purchase and the maintenance cost account for the rest. 
The latter is assumed proportional to the capacity installed.



No market equilibrium
^^^^^^^^^^^^^^^^^^^^^

The demand is described by a yearly demand and an hourly profil.
The yearly demand is exogeneous of the problem, and thus doesn't result of a offer-demand balance.
In other words, the system is forced to supply the demand even if the cost of the system soars.


Deterministic optimisation
^^^^^^^^^^^^^^^^^^^^^^^^^^

The mathematical model is written as a linear continuous problem. 
Thus, it is resolved by using linear programming solvers which are deterministic optimisation. 
All the information is known *a priori* and the solver reaches a single optimum. 

Moreover, linear programming gives chaotics solution, which can vary from white to black when slighlty changing a parameter.
As an example, one solution could be based on gas cogeneration while another is based on Combined Cycle Gas Turbines.

Uncertainty quantification techniques enable to overcome this issue by running several time the model under different configuration. 
Therefore, a short computaitonal time is required to enable many sampling.

1 year time horizon
^^^^^^^^^^^^^^^^^^^

EnergyScope TD is a snapshot model, in the sence that it represents the energy system in a target future year, without considering existing system.





