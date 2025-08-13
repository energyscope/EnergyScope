.. warning:: New and updated version of the documentation is available in this `library <https://www.energyscope.net/latest/>`_.

.. _ch_estd:

Model formulation
=================

.. role:: raw-latex(raw)
   :format: latex
..


**Model overview:**

.. figure:: /images/model_formulation/chp_estd_overview.png
   :alt: Overview of the LP modeling framework
   :name: fig:ch2_overview

   Overview of the LP modeling framework.

Overview
--------

Due to computational restrictions, energy system models rarely optimise
the 8760h of the year. As an example, running our model with 8760h time
series takes more than 19 hours; while the hereafter presented
methodology needs approximately 1 minute. A typical solution is to use a
subset of representative days called TD; this is a trade-off between
introducing an approximation error in the representation of the energy
system (especially for short-term dynamics) and computational time.

-  the first step consists in pre-processing the time series and solving
   a MILP problem to determine the adequate set of 
   (Section :ref:`sec_td_selection`).

-  the second step is the main energy model: it identifies the optimal
   design and operation of the energy system over the selected (Section
   :ref:`sec_estd`), i.e. technology selection, sizing and operation
   for a target future year.

These two steps can be computed independently. Usually, the first step
is computed once for an energy system with given weather data whereas
the second step is computed several times (once for each different
scenario). The following :numref:`Figure %s <fig:ProcessStructure>`  illustrates the overall structure of the code.

.. figure:: /images/model_formulation/meth_process_structure.png
   :alt: Overview of the EnergyScope TD framework in two-steps.
   :name: fig:ProcessStructure
   
   Overview of the EnergyScope TD framework in two-steps. **STEP 1**: 
   optimal selection of typical days (Section :ref:`sec_td_selection`). **STEP 2**: 
   Energy system model (Section :ref:`sec_estd`). The first step processes 
   only a subset of parameters, which account for the 8760h time series. 
   Abbreviations: TD, MILP, LP and GWP



This documentation is built from previous works (:cite:`Moret2017PhDThesis,Limpens2019,Limpens2021thesis`). 
For more details about the research approach, the choice of clustering method or the reconstruction method; refer to :cite:`Limpens2021thesis`.


.. _sec_td_selection:

Typical days selection
----------------------

Resorting to TDs has the main advantage of reducing the computational
time by several orders of magnitude. Usually, studies use between 6 and
20 TDs 
:cite:`Gabrielli2018,Despres2017,Nahmmacher2014,Pina2013`
sometimes even less
:cite:`Poncelet2017,Dominguez-Munoz2011`. 

Clustering methods
~~~~~~~~~~~~~~~~~~

In a previous work :cite:`Limpens2019`, it has been estimated 
that 12 typical days were appropriate for this model. 
Moreover, a comparison between different clustering algorithm shown that the method of 
:cite:`Dominguez-Munoz2011` had the best performances.

.. caution :: 
    A small mistake has been corrected on the distance used in the clustering method.
    The impact of this mistake on previous work has been assessed and the conclusion is that the impact is negligible.
    The error and explanation are detailed in the pdf Erratum_STEP_1.pdf.

Implementing seasonality with typical days
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using TDs can introduce some limitations. As an example, traditionally,
model based on TDs are not able to include inter-days or seasonal
storage due to the discontinuity between the selected days. Thus, they
assess only the capacity of production without accounting for storage
capacities. Carbon-neutral energy system will require long term storage
and thus, this limitation must be overcome. Therefore, we implemented a
method proposed by :cite:t:`Gabrielli2018` to rebuild a year
based on the typical days by defining a sequence of . This allows to
optimise the storage level of charge over the 8760h of the year.
:cite:t:`Gabrielli2018` assigned a TD to each day of the
year; all decision variables are optimised over the TDs, apart from the
amount of energy stored, which is optimised over 8760h. This methodology 
is illustrated in the follwing   :numref:`Figure %s <fig:SeasonalityImplementation>`.


.. figure:: /images/model_formulation/gabrielli.png
   :alt: Illustration of the typical days reconstruction method 
   :name: fig:SeasonalityImplementation
   :width: 14cm
   
   Illustration of the typical days reconstruction method proposed by
   :cite:`Gabrielli2018` over a week. The example is based
   on 3 TDs: TD 1 represents a cloudy weekday, applied to Monday,
   Thursday and Friday; TD 2 is a sunny weekday, applied to Tuesday and
   Wednesday; and TD 3 represents sunny weekend days. The power profile
   (above) depends solely on the typical day but the energy stored
   (below) is optimised over the 8760 hours of the year (blue curve).
   Note that the level of charge is not the same at the beginning
   (Monday 1 am) and at the end of the week (Sunday 12 pm).

The performances of this method has been quantified in a previous work :cite:`Limpens2019`.
With 12 Typical days, the key performances indicators (cost, emissions, installed capacity and primary energy used) are well captured.
The only exception are the long term storage capacities which are slightly underestimated (by maximum a factor of 2). 


.. _sec_estd:

Energy system model
-------------------


Hereafter, we present the core of the energy model. First, we introduce
the conceptual modelling framework with an illustrative example, in
order to clarify as well the nomenclature. Second, we introduce the
constraints of the energy model (data used are detailed in
the Section :doc:`/sections/Input Data`).


.. _ssec_lp_framework:

Linear programming formulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The model is mathematically formulated as a LP problem
:cite:`fourer1990modeling`. 
:numref:`Figure %s <fig:linear_programming_example>` represents - in a simple
manner - what is a LP problem and the nomenclature used. In italic
capital letters, *SETS* are collections of distinct items (as in the
mathematical definition), e.g. the *RESOURCES* set regroups all the
available resources (NG, WOOD, etc.). In italic lowercase letters,
*parameters* are known values (inputs) of the model, such as the demand
or the resource availability. In bold with first letter in uppercase,
**Variables** are unknown values of the model, such as the installed
capacity of PV. These values are determined (optimised) by the solver
within an upper and a lower bound (both being parameters). As an
example, the installed capacity of wind turbines is a decision variable;
this quantity is bounded between zero and the maximum available
potential. *Decision variables* can be split in two categories:
independent decision variables, which can be freely fixed, and dependent
decision variables, which are linked via equality constraints to the
previous ones. As an example the investment cost for wind turbines is a
variable but it directly depends on the number of wind turbines, which
is an independent decision variable. *Constraints* are inequality or
equality restrictions that must be satisfied. The problem is subject to
(*s.t.*) constraints that can enforce, for example, an upper limit for
the availability of resources, energy or mass balance, etc. Finally, an
*objective function* is a particular constraint whose value is to be
maximised (or minimised).

.. figure:: /images/model_formulation/chp_estd_lp_conceptual.png
   :alt: Conceptual illustration of a LP problem.
   :name: fig:linear_programming_example
   :width: 14cm

   Conceptual illustration of a LP problem and the nomenclature used.
   Symbol description: maximum installed size of a technology
   (*f\ max*), installed capacity of a technology (**F**) and total
   system cost (**C\ tot**). In this example, a specific technology (**F**
   [*’PV’*]) has been chosen from the set TECHNOLOGY.

.. _ssec_conceptual_modelling_framework:

Conceptual modelling framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The proposed modelling framework is a simplified representation of an
energy system accounting for the energy flows within its boundaries. Its
primary objective is to satisfy the energy balance constraints, meaning
that the demand is known and the supply has to meet it. In the energy
modelling practice, the energy demand is often expressed in terms of
FEC. According to the definition of the European commission, FEC is
defined as “*the energy which reaches the final consumer’s door*”
:cite:`EU_FEC`. In other words, the FEC is the amount of
input energy needed to satisfy the EUD in energy services. As an
example, in the case of decentralised heat production with a NG boiler,
the FEC is the amount of NG consumed by the boiler; the EUD is the
amount of heat produced by the boiler, i.e. the heating service needed
by the final user.

The input for the proposed modelling framework is the EUD in energy
services, represented as the sum of four energy-sectors: electricity,
heating, mobility and non-energy demand; this replaces the classical
economic-sector based representation of energy demand. Heat is divided
in three EUTs: high temperature heat for industry, low temperature for
space heating and low temperature for hot water. Mobility is divided in
two EUTs: passenger mobility and freight [1]_. Non-energy demand is,
based on the IEA definition, “*fuels that are used as raw materials in
the different sectors and are not consumed as a fuel or transformed into
another fuel.*” :cite:`IEA_websiteDefinition`. As examples,
the European Commission includes as non-energy the following materials:
“*chemical feed-stocks, lubricants and asphalt for road construction.*”
:cite:`EuropeanCommission2016`.

.. figure:: /images/model_formulation/chp_estd_conceptual_framework.png
   :alt: Conceptual example of an energy system.
   :name: fig:conceptual_example
   :width: 16cm

   Conceptual example of an energy system with 3 resources, 8
   technologies (of which 2 storages (in colored oval) and 1
   infrastructure (grey rectangle)) and 3 end use demands.
   Abbreviations: PHS, electrical heat pump (eHP), CHP, CNG. Some icons
   from :cite:`FlatIcon`.

A simplified conceptual example of the energy system structure is
proposed in  :numref:`Figure %s <fig:conceptual_example>`. The system is
split in three parts: resources, energy conversion and demand. In this
illustrative example, resources are solar energy, electricity and NG.
The EUD are electricity, space heating and passenger mobility. The
energy system encompasses all the energy conversion technologies needed
to transform resources and supply the EUD. In this example, Solar and NG
resources cannot be directly used to supply heat. Thus, they use
technologies, such as boilers or CHP for NG, to supply the EUT layer
(e.g. the high temperature industrial heat layer). *Layers* are defined
as all the elements in the system that need to be balanced in each time
period; they include resources and EUTs. As an example, the electricity
layer must be balanced at any time, meaning that the production and
storage must equal the consumption and losses. These layers are
connected to each other by *technologies*. We define three types of
technologies: *technologies of end-use type*, *storage technologies* and
*infrastructure technologies*. A technology of end-use type can convert
the energy (e.g. a fuel resource) from one layer to an EUT layer, such
as a CHP unit that converts NG into heat and electricity. A storage
technology converts energy from a layer to the same one, such as TS that
stores heat to provide heat. In this example (
:numref:`Figure %s <fig:conceptual_example>`), there are two storage technologies:
TS for heat and PHS for electricity. An infrastructure technology
gathers the remaining technologies, including the networks, such as the
power grid and DHNs, but also technologies linking non end-use layers,
such as methane production from wood gasification or hydrogen production
from methane reforming.

As an illustrative example of the concept of *layer*, Figure
:numref:`Figure %s <fig:LayerElec>` gives a perspective of the electricity layer
which is the most complex one, since the electrification of other
sectors is foreseen as a key of the energy transition
:cite:`Sugiyama2012`. In the proposed version, 42
technologies are related to the electricity layer. 9 technologies
produce exclusively electricity, such as CCGT, PV or wind. 12
cogenerations of heat and power (CHPs) produce heat and electricity,
such as industrial waste CHP. 6 technologies are related to the
production of synthetic fuels and CCS. 1 infrastructure represents the
grid. 4 storage technologies are implemented, such as PHS, batteries or
V2G. The remains are consumers regrouped in the electrification of heat
and mobility. Electrification of the heating sector is supported by
direct electric heating but also by the more expensive but more
efficient electrical heat pumps for low temperature heat demand.
Electrification of mobility is achieved via electric public
transportation (train, trolley, metro and electrical/hybrid buses),
electric private transportation including and hydrogen cars [2]_ and
trains for freight.

.. figure:: /images/model_formulation/Layer_Elec.png
   :alt: Representation of the Electricity layer.
   :name: fig:LayerElec
   :width: 16cm

   Representation of the Electricity layer with all the technologies
   implemented in ESTD v2.1. **Bold Italic technologies** represent a group
   of different technologies. Abbreviations: atmospheric (atm.), Carbon
   capture (CC), CCGT, CHP, HP, electricity (elec.), HP, industrial
   (ind.) IGCC, PHS, synthetic methanolation (S. Methanol.), V2G, EUD.

The energy system is formulated as a LP problem. It optimises the design
by computing the installed capacity of each technology, as well as the
operation in each period, to meet the energy demand and minimize the
total annual cost of the system. In the following, we present the
complete formulation of the model in two parts. First, all the terms
used are summarised in a figure and tables:  :numref:`Figure %s <fig:sets>`
for sets, Tables :numref:`%s <tab:paramsDistributions>` and
:numref:`%s <tab:params>` for parameters, and 
:numref:`%s <tab:variablesIndependent>` and
:numref:`%s <tab:variablesdependent>` for variables. On
this basis, the equations representing the constraints and the objective
function are formulated in  :numref:`Figure %s <fig:EndUseDemand>` and
Eqs. :eq:`eq:obj_func` - :eq:`eq:efficiency`
and described in the following paragraphs.

.. _ssec_sets_params_vars:

Sets, parameters and variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:numref:`Figure %s <fig:sets>` gives a visual representation of the sets
with their relative indices used in the followings. 
:numref:`%s <tab:paramsDistributions>` and :numref:`%s <tab:params>`
list and describe the model parameters. Tables
:numref:`%s <tab:variablesIndependent>` and
:numref:`%s <tab:variablesdependent>` list and describe
the independent and dependent variables, respectively.

.. figure:: /images/model_formulation/ses_sets_v2.png
   :alt: Visual representation of the sets and indices used.
   :name: fig:sets

   Visual representation of the sets and indices used in the LP
   framework. Abbreviations: SH, HW, temperature (T), MOB, passenger
   (*Pass.*), V2G, TS.

.. container::

   .. table:: Time series parameters
      :name: tab:paramsDistributions

      +---------------------------+-----------+---------------------------+
      | **Parameter**             | **Units** | **Description**           |
      +===========================+===========+===========================+
      | :math:`\%_{elec}(h,td)`   | [-]       | Yearly time series        |
      |                           |           | (adding up to 1) of       |
      |                           |           | electricity end-uses      |
      +---------------------------+-----------+---------------------------+
      | :math:`\%_{sh}(h,td)`     | [-]       | Yearly time series        |
      |                           |           | (adding up to 1) of SH    |
      |                           |           | end-uses                  |
      +---------------------------+-----------+---------------------------+
      | :math:`\%_{elec}(h,td)`   | [-]       | Yearly time series        |
      |                           |           | (adding up to 1) of       |
      |                           |           | passenger mobility        |
      |                           |           | end-uses                  |
      +---------------------------+-----------+---------------------------+
      | :math:`\%_{fr}(h,td)`     | [-]       | Yearly time series        |
      |                           |           | (adding up to 1) of       |
      |                           |           | freight mobility end-uses |
      +---------------------------+-----------+---------------------------+
      | :math:`c_{p,t}(tech,h,td)`| [-]       | Hourly maximum capacity   |
      |                           |           | factor for each           |
      |                           |           | technology (default 1)    |
      +---------------------------+-----------+---------------------------+


.. container::

   .. table:: List of parameters (except time series).
      :name: tab:params

      +----------------------+----------------------+----------------------+
      | Parameter            | Units                | Description          |
      +======================+======================+======================+
      | :math:`\tau`\ (tech) | [-]                  | Investment cost      |
      |                      |                      | annualization factor |
      +----------------------+----------------------+----------------------+
      | :math:`i_{rate}`     | [-]                  | Real discount rate   |
      +----------------------+----------------------+----------------------+
      | :math:`endUses_      | [GWh/y] [a]_         | Annual end-uses in   |
      | {year}               |                      | energy services per  |
      | (eui,s)`             |                      | sector               |
      +----------------------+----------------------+----------------------+
      | :math:`endUsesInput  | [GWh/y] [a]_         | Total annual         |
      | (eui)`               |                      | end-uses in energy   |
      |                      |                      | services             |
      +----------------------+----------------------+----------------------+
      | :math:`re_{share}`   | [-]                  | minimum share [0;1]  |
      |                      |                      | of primary RE        |
      +----------------------+----------------------+----------------------+
      | :math:`gwp           | [ktCO\               | Higher               |
      | _{limit}`            | :math:`_{2-eq}`/y]   | CO\ :math:`_{2-eq}`  |
      |                      |                      | emissions limit      |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Lower and upper      |
      | {public,min},        |                      | limit to             |
      | \%_{public,max}`     |                      | :math:`\textbf{%}_   |
      |                      |                      | {\textbf{Public}}`   |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Lower and upper      |
      | {fr,rail,min},       |                      | limit to             |
      | \%_{fr,rail,max}`    |                      | :math:`\textbf{%}_   |
      |                      |                      | {\textbf{Fr,Rail}}`  |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Lower and upper      |
      | {fr,boat,min},       |                      | limit to             |
      | \%_{fr,boat,max}`    |                      | :math:`\textbf{%}_   |
      |                      |                      | {\textbf{Fr,Boat}}`  |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Lower and upper      |
      | {fr,truck,min},      |                      | limit to             |
      | \%_{fr,truck,max}`   |                      | :math:`\textbf{%}_   |
      |                      |                      | {\textbf{Fr,Truck}}` |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Lower and upper      |
      | {dhn,min},           |                      | limit to             |
      | \%_{dhn,max}`        |                      | :math:`\textbf{%}_   |
      |                      |                      | {\textbf{Dhn}}`      |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Share of non-energy  |
      | {ned}(EUT\_OF\_EUC(  |                      | demand per type      |
      | NON\_ENERGY))`       |                      | of feedstocks        |
      +----------------------+----------------------+----------------------+
      | :math:`t_            | [h]                  | Time period duration |
      | {op}(h,td)`          |                      | (default 1h)         |
      +----------------------+----------------------+----------------------+
      | :math:`f_{min},      | [GW] [a]_ [b]_       | Min./max. installed  |
      | f_{max}              |                      | size of the          |
      | (tech)`              |                      | technology           |
      +----------------------+----------------------+----------------------+
      | :math:`f_{min,\%},   | [-]                  | Min./max. relative   |
      | f_{max,\%}(tech)`    |                      | share of a           |
      |                      |                      | technology in a      |
      |                      |                      | layer                |
      +----------------------+----------------------+----------------------+
      | :math:`avail(res)`   | [GWh/y]              | Resource yearly      |
      |                      |                      | total availability   |
      +----------------------+----------------------+----------------------+
      | :math:`c_{op}(res)`  | [M€\                 | Specific cost of     |
      |                      | :math:`_{2015}`/GWh] | resources            |
      +----------------------+----------------------+----------------------+
      | :math:`veh_{capa}`   | [km-pass/h/veh.] [a]_| Mobility capacity    |
      |                      |                      | per vehicle (veh.).  |
      +----------------------+----------------------+----------------------+
      | :math:`\%_{          | [-]                  | Ratio peak/max.      |
      | Peak_{sh}}`          |                      | space heating demand |
      |                      |                      | in typical days      |
      +----------------------+----------------------+----------------------+
      | :math:`f(            | [GW] [c]_            | Input from (<0) or   |
      | res\cup tech         |                      | output to (>0) layers|
      | \setminus sto, l)`   |                      | . f(i,j) = 1 if j is |
      |                      |                      | main output layer for|
      |                      |                      | technology/resource  |
      |                      |                      | i.                   |
      +----------------------+----------------------+----------------------+
      | :math:`c_            | [M€\ :math:`_{2015}` | Technology specific  |
      | {inv}(tech)`         | /GW] [c]_ [b]_       | investment cost      |
      +----------------------+----------------------+----------------------+
      | :math:`c_{maint}     | [M€\ :math:`_{2015}` | Technology specific  |
      | (tech)`              | /GW/y]               | yearly maintenance   |
      |                      | [c]_ [b]_            | cost                 |
      +----------------------+----------------------+----------------------+
      | :math:`{             | [y]                  | Technology lifetime  |
      | lifetime}(tech)`     |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`gwp_{constr}  | [ktCO\               | Technology           |
      | (tech)`              | :math:`_2`-eq./GW]   | construction         |
      |                      | [a]_ [b]_            | specific GHG         |
      |                      |                      | emissions            |
      +----------------------+----------------------+----------------------+
      | :math:`gwp_          | [ktCO\               | Specific GHG         |
      | {op}(res)`           | :math:`_2`-eq./GWh]  | emissions of         |
      |                      |                      | resources            |
      +----------------------+----------------------+----------------------+
      | :math:`c_{p}(tech)`  | [-]                  | Yearly capacity      |
      |                      |                      | factor               |
      +----------------------+----------------------+----------------------+
      | :math:`\eta_{s       | [-]                  | Efficiency [0;1] of  |
      | to,in},\eta_{sto     |                      | storage input from/  |
      | ,out} (sto,l)`       |                      | output to layer. Set |
      |                      |                      | to 0 if storage not  |
      |                      |                      | related to layer     |
      +----------------------+----------------------+----------------------+
      | :math:`\%_{          | [1/h]                | Losses in storage    |
      | sto_{loss}}(sto)`    | (self discharge)     |                      |
      |                      |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`t_{sto_{in}}  | [-]                  | Time to charge       |
      | (sto)`               |                      | storage (Energy to   |
      |                      |                      | power ratio)         |
      +----------------------+----------------------+----------------------+
      | :math:`t_{sto_{out}} | [-]                  | Time to discharge    |
      | (sto)`               |                      | storage (Energy to   |
      |                      |                      | power ratio)         |
      +----------------------+----------------------+----------------------+
      | :math:`\%_           | [-]                  | Storage technology   |
      | {sto_{avail}}        |                      | availability to      |
      | (sto)`               |                      | charge/discharge     |
      +----------------------+----------------------+----------------------+
      | :math:`\%_{net_      | [-]                  | Losses coefficient   |
      | {loss}}(eut)`        |                      | :math:`[0;1]` in the |
      |                      |                      | networks (grid and   |
      |                      |                      | DHN)                 |
      +----------------------+----------------------+----------------------+
      | :math:`ev_{b         | [GWh]                | Battery size per V2G |
      | att,size}(v2g)`      |                      | car technology       |
      +----------------------+----------------------+----------------------+
      | :math:`soc_{min,ev}  | [GWh]                | Minimum state of     |
      | (v2g,h)`             |                      | charge for electric  |
      |                      |                      | vehicles             |
      +----------------------+----------------------+----------------------+
      | :math:`c_            | [M€\                 | Cost to reinforce    |
      | {grid,extra}`        | :math:`_2015`/GW]    | the grid per GW of   |
      |                      |                      | intermittent         |
      |                      |                      | renewable            |
      +----------------------+----------------------+----------------------+
      | :math:`elec_{        | [GW]                 | Maximum net transfer |
      | import,max}`         |                      | capacity             |
      +----------------------+----------------------+----------------------+
      | :math:`{solar}` _    | [km\ :math:`^2`]     | Available area for   |
      | :math:`{area}`       |                      | solar panels         |
      +----------------------+----------------------+----------------------+
      | :math:`{power}` _    | [GW/km\ :math:`^2`]  | Peak power density   |
      | :math:`density_{pv}` |                      | of PV                |
      +----------------------+----------------------+----------------------+
      | :math:`{power}` _    | [GW/km\ :math:`^2`]  | Peak power density   |
      | :math:`density_{     |                      | of solar thermal     |
      | solar,thermal}`      |                      |                      |
      +----------------------+----------------------+----------------------+
.. [a]
   [Mpkm] (millions of passenger-km) for passenger,
   [Mtkm] (millions of ton-km) for freight mobility end-uses

.. [b]
   [GWh] if :math:`{{tech}} \in {{STO}}`

.. [c]
   [Mpkm/h] for passenger, [Mtkm/h] for freight
   mobility end-uses


.. container::

   .. table:: Independent variables. All variables are continuous and non-negative, unless otherwise indicated.
      :name: tab:variablesIndependent
   
      +---------------------------+------------+---------------------------+
      | Variable                  | Units      | Description               |
      +===========================+============+===========================+
      | :math:`\textbf{%}_{       | [-]        | Ratio :math:`[0;1]`       |
      | \textbf{Public}}`         |            | public mobility over      |
      |                           |            | total passenger mobility  |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Ratio :math:`[0;1]` rail  |
      | \textbf{Fr,Rail}}`        |            | transport over total      |
      |                           |            | freight transport         |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Ratio :math:`[0;1]` boat  |
      | \textbf{Fr,Boat}}`        |            | transport over total      |
      |                           |            | freight transport         |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Ratio :math:`[0;1]` truck |
      | \textbf{Fr,Truck}}`       |            | transport over total      |
      |                           |            | freight transport         |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Ratio :math:`[0;1]`       |
      | \textbf{Dhn}}`            |            | centralized over total    |
      |                           |            | low-temperature heat      |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{F}(tech)`  | [GW] [d]_  | Installed capacity with   |
      |                           |            | respect to main output    |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{F}_        | [GW] [d]_  | Operation in each period  |
      | {\textbf{t}}(tech         |            |                           |
      | \cup res,h,td)`           |            |                           |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{Sto}_{     | [GW]       | Input to/output from      |
      | \textbf{in}},             |            | storage units             |
      | \textbf{Sto}_{            |            |                           |
      | \textbf{out}}             |            |                           |
      | (sto, l, h, td)`          |            |                           |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{P}_{       | [GW]       | Constant load of nuclear  |
      | \textbf{Nuclear}}`        |            |                           |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{Import}_   | [GW]       | Resources imported at     |
      | \textbf{Constant}`        |            | a constant flow           |
      | (RES_IMPORT_CONSTANT)     |            |                           | 
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Constant share of         |
      | \textbf{PassMob}}(TECH\   |            | passenger mobility        |
      | OF\ EUC(PassMob))`        |            |                           |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Constant share of         |
      | \textbf{FreightMob}}      |            | freight mobility          |
      | (TECH~OF~EUC(FreightMob))`|            |                           |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{%}_{       | [-]        | Constant share of low     |
      | \textbf{HeatLowTDEC}}     |            | temperature heat          |
      | (TECH~OF~EUT(HeatLowTDec) |            | decentralised supplied    |
      | \setminus {Dec_{Solar}}   |            | by a technology plus its  |
      | )`                        |            | associated thermal solar  |
      |                           |            | and storage               |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{F}_{       | [-]        | Solar thermal installed   |
      | \textbf{sol}}             |            | capacity associated to a  |
      | (TECH~OF~EUT(HeatLowTDec) |            | decentralised heating     |
      | \setminus {Dec_{Solar}})` |            | technology                |
      +---------------------------+------------+---------------------------+
      | :math:`\textbf{F}_{       | [-]        | Solar thermal operation   |
      | \textbf{t}_{\textbf{sol}}}|            | in each period            |
      | (TECH~OF~EUT(HeatLowTDec) |            |                           |
      | \setminus {Dec_{Solar}})` |            |                           |
      +---------------------------+------------+---------------------------+



.. [d]
   [Mpkm] (millions of passenger-km) for passenger,
   [Mtkm] (millions of ton-km) for freight mobility end-uses


.. container::

   .. table:: Dependent variable. All variables are continuous and non-negative, unless otherwise indicated.
      :name: tab:variablesDependent

      +----------------------+----------------------+----------------------+
      | **Variable**         | **Units**            | **Description**      |
      +======================+======================+======================+
      | :math:`\textbf{      | [GW] [e]_            | End-uses demand. Set |
      | EndUses}(l,h,td)`    |                      | to 0 if              |
      |                      |                      | :math:`l \notin`     |
      |                      |                      | *EUT*                |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{C}_   | [M€\ :sub:`2015`/y]  | Total annual cost of |
      | {\textbf{tot}}`      |                      | the energy system    |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{C}_   | [M€\ :sub:`2015`]    | Technology total     |
      | {\textbf{inv}}(      |                      | investment cost      |
      | tech)`               |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{C}_   | [M€\ :sub:`2015`/y]  | Technology yearly    |
      | {\textbf{maint}}(    |                      | maintenance cost     |
      | tech)`               |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{C}_   | [M€\ :sub:`2015`/y]  | Total cost of        |
      | {\textbf{op}}(       |                      | resources            |
      | res)`                |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{GWP}_ | [ktCO\               | Total yearly GHG     |
      | {\textbf{tot}}`      | :math:`_2`-eq./y]    | emissions of the     |
      |                      |                      | energy system        |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{GWP}_ | [k\                  | Technology           |
      | {\textbf{constr}}(   | tCO\ :math:`_2`-eq.] | construction GHG     |
      | tech)`               |                      | emissions            |
      |                      |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{GWP}_ | [ktC\                | Total GHG emissions  |
      | {\textbf{po}}(       | O\ :math:`_2`-eq./y] | of resources         |
      | res)`                |                      |                      |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{Net}_ | [GW]                 | Losses in the        |
      | {\textbf{losses}}(   |                      | networks (grid and   |
      | eut,h,td)`           |                      | DHN)                 |
      +----------------------+----------------------+----------------------+
      | :math:`\textbf{Sto}_ | [GWh]                | Energy stored over   |
      | {\textbf{level}}(    |                      | the year             |
      | sto,t)`              |                      |                      |
      +----------------------+----------------------+----------------------+

.. [e]
   [Mpkm] (millions of passenger-km) for passenger,
   [Mtkm] (millions of ton-km) for freight mobility end-uses

.. _ssec_lp_formulation:

Energy model formulation
~~~~~~~~~~~~~~~~~~~~~~~~

In the following, the overall LP formulation is proposed through :numref:`Figure %s <fig:EndUseDemand>` and equations
 :eq:`eq:obj_func` - :eq:`eq:solarAreaLimited`
the constraints are regrouped in paragraphs. It starts with the
calculation of the EUD. Then, the cost, the GWP and the objective
functions are introduced. Then, it follows with more specific
paragraphs, such as *storage* or *vehicle-to-grid* implementations.

End-use demand
^^^^^^^^^^^^^^

Imposing the EUD instead of the FEC has two advantages. First, it
introduces a clear distinction between demand and supply. On the one
hand, the demand concerns the definition of the end-uses, i.e. the
requirements in energy services (e.g. the mobility needs). On the other
hand, the supply concerns the choice of the energy conversion
technologies to supply these services (e.g. the types of vehicles used
to satisfy the mobility needs). Based on the technology choice, the same
EUD can be satisfied with different FEC, depending on the efficiency of
the chosen energy conversion technology. Second, it facilitates the
inclusion in the model of electric technologies for heating and
transportation.

.. figure:: /images/model_formulation/EndUseDemand.png
   :alt: Hourly **EndUses** demands calculation.
   :name: fig:EndUseDemand
   :width: 16cm

   Hourly **EndUses** demands calculation starting from yearly demand
   inputs (*endUsesInput*). Adapted from
   :cite:`Moret2017PhDThesis`. Abbreviations: space heating
   (sh), district heating network (DHN), high value chemicals (HVC), hot water (HW), passenger
   (pass), freight (fr) and non-energy demand (NED).

The hourly end-use demands (**EndUses**) are computed based on the
yearly end-use demand (*endUsesInput*), distributed according to its
time series (listed in :numref:`Table %s <tab:paramsDistributions>`). 
:numref:`Figure %s <fig:EndUseDemand>` graphically presents the constraints
associated to the hourly end use demand (**EndUses**), e.g. the public
mobility demand at time :math:`t` is equal to the hourly passenger
mobility demand times the public mobility share (**%\ Public**).

Electricity end-uses result from the sum of the electricity-only demand,
assumed constant throughout the year, and the variable demand of
electricity, distributed across the periods according to *%\ elec*.
Low-temperature heat demand results from the sum of the yearly demand
for HW, evenly shared across the year, and SH, distributed across the
periods according to *%\ sh*. The percentage repartition between
centralized (DHN) and decentralized heat demand is defined by the
variable **%\ Dhn**. High temperature process heat and mobility demand
are evenly distributed across the periods. Passenger mobility demand is
expressed in passenger-kilometers (pkms), freight transportation demand
is in ton-kilometers (tkms). The variable **%\ Public** defines the
penetration of public transportation in the passenger mobility sector.
Similarly, **%\ Rail**, **%\ Boat** and **%\ Truck** define the
penetration of train, boat and trucks for freight mobility,
respectively.

Cost, emissions and objective function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::
    \text{min} \textbf{C}_{\textbf{tot}} = \sum_{j \in \text{TECH}} \Big(\textbf{$\tau$}(j) \textbf{C}_{\textbf{inv}}(j) + \textbf{C}_{\textbf{maint}} (j)\Big) + \sum_{i \in \text{RES}} \textbf{C}_{\textbf{op}}(i)
    :label: eq:obj_func

.. math::
    \text{s.t. }  \textbf{$\tau$}(j) =  \frac{i_{\text{rate}}(i_{\text{rate}}+1)^{lifetime(j)}}{(i_{\text{rate}}+1)^{lifetime(j)} - 1} ~~~~~~ \forall j \in \text{TECH}\\
    :label: eq:tau

.. math::
    \textbf{C}_{\textbf{inv}}(j) = c_{\text{inv}}(j) \textbf{F}(j) ~~~~~~ \forall j \in \text{TECH}\\
    :label: eq:c_inv

.. math::
    \textbf{C}_{\textbf{maint}}(j) = c_{\text{maint}}(j) \textbf{F}(j) ~~~~~~ \forall j \in \text{TECH}\\ 
    :label: eq:c_maint

.. math::
    \textbf{C}_{\textbf{op}}(i) = \sum_{t \in T | \{h,td\} \in T\_H\_TD(t)} c_{\text{op}}(i) \textbf{F}_{\textbf{t}}(i,h,td) t_{op} (h,td)  
    ~~~~~~ \forall i \in \text{RES}
    :label: eq:c_op

The objective, Eq. :eq:`eq:obj_func`, is the
minimisation of the total annual cost of the energy system (:math:`\textbf{C}_{\textbf{tot}}`),
defined as the sum of the annualized investment cost of the technologies
(:math:`\tau\textbf{C}_{\textbf{inv}}`), the operating and maintenance cost of the
technologies (:math:`\textbf{C}_{\textbf{maint}}`) and the operating cost of the resources
(:math:`\textbf{C}_{\textbf{op}}`). The total investment cost (:math:`\textbf{C}_{\textbf{inv}}`) of each technology
results from the multiplication of its specific investment cost
(:math:`c_{inv}`) and its installed size (**F**), the latter defined with
respect to the main end-uses output [3]_ type,
Eq. :eq:`eq:c_inv`. :math:`\textbf{C}_{\textbf{inv}}` is annualised with the
factor :math:`\tau`, calculated based on the interest rate (:math:`t_{op}`)
and the technology lifetime (*lifetime*), Eq. :eq:`eq:tau`.
The total operation and maintenance cost is calculated in the same way,
Eq. :eq:`eq:c_maint`. The total cost of the resources is
calculated as the sum of the end-use over different periods multiplied
by the period duration (:math:`t_{op}`) and the specific cost of the resource
(:math:`c_{op}`), Eq. :eq:`eq:c_op`. Note that, in
Eq. :eq:`eq:c_op`), summing over the typical days using the
set T_H_TD [4]_ is equivalent to summing over the 8760h of the year.

.. math::
    \textbf{GWP}_\textbf{tot}  = \sum_{j \in \text{TECH}} \frac{\textbf{GWP}_\textbf{constr} (j)}{lifetime(j)} +   \sum_{i \in \text{RES}} \textbf{GWP}_\textbf{op} (i) 
    :label: eq:GWP_tot
    
    \left(\text{in this version of the model} :   \textbf{GWP}_\textbf{tot}  =    \sum_{i \in \text{RES}} \textbf{GWP}_\textbf{op} (i) \right) 
    

.. math::
    \textbf{GWP}_\textbf{constr}(j) = gwp_{\text{constr}}(j) \textbf{F}(j) ~~~~~~ \forall j \in \text{TECH}
    :label: eq:GWP_constr

.. math::
    \textbf{GWP}_\textbf{op}(i) = \sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} gwp_\text{op}(i) \textbf{F}_\textbf{t}(i,h,td)  t_{op} (h,td )~~~~~~ \forall i \in \text{RES}
    :label: eq:GWP_op

The global annual GHG emissions are calculated using a LCA approach,
i.e. taking into account emissions of the technologies and resources
‘*from cradle to grave*’. For climate change, the natural choice as
indicator is the GWP, expressed in ktCO\ :math:`_2`-eq./year. In
Eq. :eq:`eq:GWP_tot`, the total yearly emissions of the
system (:math:`\textbf{GWP}_{\textbf{tot}}`) are defined as the sum of the emissions related to
the construction and end-of-life of the energy conversion technologies
:math:`\textbf{GWP}_{\textbf{constr}}`, allocated to one year based on the technology
lifetime (:math:`lifetime`), and the emissions related to resources
:math:`\textbf{GWP}_{\textbf{op}}`). Similarly to the costs, the total emissions related to
the construction of technologies are the product of the specific
emissions (:math:`gwp_{constr}` and the installed size (:math:`\textbf{F}`),
Eq. :eq:`eq:GWP_constr`. The total emissions of the
resources are the emissions associated to fuels (from cradle to
combustion) and imports of electricity (:math:`gwp_{op}`) multiplied by the
period duration (:math:`t_{op}`), Eq. :eq:`eq:GWP_op`. GWP
accounting can be conducted in different manners deepending on the scope of emission. The
European Commission and the IEA mainly uses resource-related emissions
:math:`\textbf{GWP}_{\textbf{op}}` while neglecting indirect emissions related to the
construction of technologies :math:`\textbf{GWP}_{\textbf{constr}}`. To facilitate the
comparison with their results, a similar implementation is proposed in
Eq. :eq:`eq:GWP_tot`.

System design and operation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::
    f_{\text{min}} (j) \leq \textbf{F}(j) \leq f_{\text{max}} (j) ~~~~~~ \forall j \in \text{TECH}
    :label: eq:fmin_fmax

The installed capacity of a technology (**F**) is constrained between
upper and lower bounds (*f\ max* and *f\ min*),
Eq. :eq:`eq:fmin_fmax`. This formulation allows
accounting for old technologies still existing in the target year (lower
bound), but also for the maximum deployment potential of a technology.
As an example, for offshore wind turbines, :math:`f_{min}` represents
the existing installed capacity (which will still be available in the
future), while :math:`f_{max}` represents the maximum potential.

.. math::
     \textbf{F}_\textbf{t}(i,h,td) \leq \textbf{F}_\textbf{t}(i) \cdot c_{p,t} (i,h,td) ~~~~~~ \forall i \in \text{TECH}, h \in H, td \in TD
    :label: eq:cp_t

.. math::
    \sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(j,h,td) t_{op}(h,td)  \leq   \textbf{F} (j) c_{p} (j) \sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} t_{op} (h,td)  
    :label: eq:c_p

    \forall j \in \text{TECH}

.. math::
    \sum_{t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(i,h,td) t_{op}(h,td)  \leq \text{avail} (i) ~~~~~~ \forall i \in \text{RES}
    :label: eq:res_avail



The operation of resources and technologies in each period is determined
by the decision variable :math:`\textbf{F}_{\textbf{t}}`. The capacity factor of technologies
is conceptually divided into two components: a capacity factor for each
period (:math:`c_{p,t}`) depending on resource availability (e.g. renewables)
and a yearly capacity factor (*c\ p*) accounting for technology downtime
and maintenance. For a given technology, the definition of only one of
these two is needed, the other one being fixed to the default value of
1. For example, intermittent renewables are constrained by an hourly
load factor (:math:`c_{p,t}\in[0;1]`) while CCGTs are constrained by
an annual load factor (:math:`c_{p}`, in that case 96% in 2035).
Eqs. :eq:`eq:cp_t` and :eq:`eq:c_p` link the
installed size of a technology to its actual use in each period (:math:`\textbf{F}_{\textbf{t}}`)
via the two capacity factors. The total use of resources is limited by
the yearly availability (:math:`avail`),
Eq. :eq:`eq:res_avail`.

.. math::
    \sum_{i \in \text{RES}~\cup \text{TECH} \setminus \text{STO}} f(i,l) \textbf{F}_\textbf{t}(i,h,td) + \sum_{j \in \text{STO}} \bigg(\textbf{Sto}_\textbf{out}(j,l,h,td) - \textbf{Sto}_\textbf{in}(j,l,h,td)\bigg)  
    :label: eq:layer_balance

    - \textbf{EndUses}(l,h,td) = 0
     
    \forall l \in L, \forall h \in H, \forall td \in TD
  
The matrix :math:`f` defines for all technologies and resources outputs to
(positive) and inputs (negative) layers.
Eq. :eq:`eq:layer_balance` expresses the balance
for each layer: all outputs from resources and technologies (including
storage) are used to satisfy the EUD or as inputs to other resources and
technologies.

Storage
^^^^^^^

.. math::
    \textbf{Sto}_\textbf{level} (j,t) =    \textbf{Sto}_\textbf{level} (j,t-1)\cdot\left(1 - \%_{sto_{loss}}(j) \right)  
   :label: eq:sto_level

    + t_{op} (h,td)\cdot \Big(\sum_{l \in L | \eta_{\text{sto,in} (j,l) > 0}} \textbf{Sto}_\textbf{in} 	(j,l,h,td) \eta_{\text{sto,in}} (j,l) 
    
    ~~~~~~ - \sum_{l \in L | \eta_{\text{sto,out} (j,l) > 0}} \textbf{Sto}_\textbf{out} (j,l,h,td) /  \eta_{\text{sto,out}} (j,l)\Big)
    
    \forall j \in \text{STO}, \forall t \in \text{T}| \{h,td\} \in T\_H\_TD(t)


.. math::
    \textbf{Sto}_\textbf{level} (j,t) = \textbf{F}_\textbf{t} (j,h,td) ~~~~~~ \forall j \in \text{STO DAILY},\forall t \in \text{T}| \{h,td\} \in T\_H\_TD(t)
    :label: eq:Sto_level_bound_DAILY

.. math::
    \textbf{Sto}_\textbf{level} (j,t) \leq \textbf{F} (j) ~~~~~~ \forall j \in \text{STO} \setminus \text{STO DAILY},\forall t \in \text{T}  
    :label: eq:Sto_level_bound


The storage level (:math:`\textbf{Sto}_{\textbf{level}}`) at a time step (:math:`t`) is equal
to the storage level at :math:`t-1` (accounting for the losses in
:math:`t-1`), plus the inputs to the storage, minus the output from the
storage (accounting for input/output efficiencies),
Eq. :eq:`eq:sto_level`:. In the code, for the first period of the year, 
this equation is slightly modified to set the storage level at 
the beginning of the year according to the one at the end of the year. Hence, if :math:`t=1`, 
we set :math:`t-1` to the last period of the year (8760). The storage systems which can
only be used for short-term (daily) applications are included in the
daily storage set (STO DAILY). For these units,
Eq. :eq:`eq:Sto_level_bound_DAILY`: imposes
that the storage level be the same at the end of each typical day [5]_.
Adding this constraint drastically reduces the computational time. For
the other storage technologies, which can also be used for seasonal
storage, the capacity is bounded by
Eq. :eq:`eq:Sto_level_bound`. For these units,
the storage behaviour is thus optimized over 8760h.

.. math::
    \textbf{Sto}_\textbf{in}(j,l,h,td)\cdot \Big(\lceil  \eta_{sto,in}(j,l)\rceil -1 \Big) = 0  ~~~~~~ \forall j \in \text{STO},\forall l \in \text{L}, \forall h \in \text{H}, \forall td \in \text{TD}
    :label: eq:StoInCeil

.. math::
    \textbf{Sto}_\textbf{out}(j,l,h,td)\cdot \Big(\lceil  \eta_{sto,out}(j,l)\rceil -1 \Big) = 0  ~~~~~~ \forall j \in \text{STO},\forall l \in \text{L}, \forall h \in \text{H}, \forall td \in \text{TD}
    :label: eq:StoOutCeil

.. math::
    \Big(\textbf{Sto}_\textbf{in} (j,l,h,td)t_{sto_{in}}(\text{j}) + \textbf{Sto}_\textbf{out}(j,l,h,td)t_{sto_{out}}(\text{j})\Big) \leq \textbf{F} (j)\%_{sto_{avail}}(j)
    :label: eq:LimitChargeAndDischarge

    \forall j \in STO \setminus {V2G} , \forall l \in L, \forall h \in H, \forall td \in TD


Eqs. :eq:`eq:StoInCeil` - :eq:`eq:StoOutCeil`
force the power input and output to zero if the layer is
incompatible [6]_. As an example, a PHS will only be linked to the
electricity layer (input/output efficiencies :math:`>` 0). All other
efficiencies will be equal to 0, to impede that the PHS exchanges with
incompatible layers (e.g. mobility, heat, etc).
Eq. :eq:`eq:LimitChargeAndDischarge`
limits the power input/output of a storage technology based on its
installed capacity (**F**) and three specific characteristics. First,
storage availability (:math:`\%_{sto_{avail}}`) is defined as the ratio between
the available storage capacity and the total installed capacity (default
value is 100%). This parameter is only used to realistically represent
V2G, for which we assume that only a fraction of the fleet (i.e. 20% in
these cases) can charge/discharge at the same time. Second and third,
the charging/discharging time (:math:`t_{sto_{in}}`, :math:`t_{sto_{out}}`), which are
the time to complete a full charge/discharge from empty/full
storage [7]_. As an example, a daily thermal storage needs at least 4
hours to discharge
(:math:`t_{sto_{out}}=4`\ [h]), and
another 4 hours to charge
(:math:`t_{sto_{in}}=4`\ [h]). Eq. :eq:`eq:LimitChargeAndDischarge` applies for 
all storage except electric vehicles which are limited by another constraint Eq. :eq:`eq:LimitChargeAndDischarge_ev`, presented later.

Networks
^^^^^^^^

.. math::
    \textbf{Net}_\textbf{loss}(eut,h,td) = \Big(\sum_{i \in \text{RES} \cup \text{TECH} \setminus \text{STO} | f(i,eut) > 0} f(i,eut)\textbf{F}_\textbf{t}(i,h,td) \Big) \%_{\text{net}_{loss}} (eut) 
    :label: eq:loss

    \forall eut = \text{EUT}, \forall h \in H, \forall td \in TD

.. math::
    \textbf{F} (Grid) = 1 + \frac{c_{grid,extra}}{c_{inv}(Grid)} 
    \Big(
    \textbf{F}(Wind_{onshore}) + \textbf{F}(Wind_{offshore}) + \textbf{F}(PV)
    :label: eq:mult_grid

    -\big( 
    f_{min}(Wind_{onshore}) + f_{min}(Wind_{offshore}) + f_{min}(PV)
    \big)
    \Big)

.. math::
    \textbf{F} (DHN) = \sum_{j \in \text{TECH} \setminus {STO} | f(j,\text{HeatLowTDHN}) >0} f(j,\text{HeatLowTDHN}) \cdot \textbf{F} (j) 
    :label: eq:DHNCost

Eq. :eq:`eq:loss` calculates network losses as a share
(:math:`%_{net_{loss}}`) of the total energy transferred through the network. As
an example, losses in the electricity grid are estimated to be 4.5\% of
the energy transferred in 2015 [8]_.
Eqs. :eq:`eq:mult_grid` - :eq:`eq:DHNCost`
define the extra investment for networks. Integration of intermittent RE
implies additional investment costs for the electricity grid
(:math:`c_{grid,ewtra}`). As an example, the reinforcement of the electricity
grid is estimated to be 358 millions €\ :sub:`2015` per Gigawatt of
intermittent renewable capacity installed (see 
`Data for the grid <#ssec:app1_grid:>`__ for details).
Eq. :eq:`eq:DHNCost` links the size of DHN to the total
size of the installed centralized energy conversion technologies.

Additional Constraints
^^^^^^^^^^^^^^^^^^^^^^

.. math::
    \textbf{F}_\textbf{t} (Nuclear,h,td) = \textbf{P}_\textbf{Nuclear}  ~~~~~~ \forall h \in H, \forall td \in TD
    :label: eq:CstNuke

Nuclear power plants are assumed to have no power variation over the
year, Eq. :eq:`eq:CstNuke`. If needed, this equation can
be replicated for all other technologies for which a constant operation
over the year is desired.

.. math::
    \textbf{F}_\textbf{t} (j,h,td) = \textbf{%}_\textbf{PassMob} (j)   \sum_{l \in EUT\_of\_EUC(PassMob)} \textbf{EndUses}(l,h,td) 
    :label: eq:mob_share_fix

    \forall j \in TECH\_OF\_EUC(PassMob) , \forall h \in H, \forall td \in TD

.. math::
    \textbf{F}_\textbf{t} (j,h,td) = \textbf{%}_\textbf{FreightMob} (j)   \sum_{l \in EUT\_of\_EUC(FreightMob)} \textbf{EndUses}(l,h,td) 
    :label: eq:freight_share_fix

    \forall j \in TECH\_OF\_EUC(FreightMob) , \forall h \in H, \forall td \in TD

.. math::
    \textbf{%}_\textbf{Fr,Rail} + \textbf{%}_\textbf{Fr,Train} + \textbf{%}_\textbf{Fr,Boat} = 1
    :label: eq:freight_share_constant


Eqs. :eq:`eq:mob_share_fix` - :eq:`eq:freight_share_fix`
impose that the share of the different technologies for mobility
(:math:`\textbf{%}_{\textbf{PassMob}}`) and (:math:`\textbf{%}_{\textbf{Freight}}`) be the same at each time
step [9]_. In other words, if 20% of the mobility is supplied by train,
this share remains constant in the morning or the afternoon.
Eq. :eq:`eq:freight_share_constant`
verifies that the freight technologies supply the overall freight demand
(this constraint is related to :numref:`Figure %s <fig:EndUseDemand>`).

Decentralised heat production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. math::
    \textbf{F} (Dec_{Solar}) = \sum_{j \in \text{TECH OF EUT} (\text{HeatLowTDec}) \setminus \{ 'Dec_{Solar}' \}} \textbf{F}_\textbf{sol} (j)  
    :label: eq:de_strategy_dec_total_ST

.. math::
    \textbf{F}_{\textbf{t}_\textbf{sol}} (j,h,td) \leq  \textbf{F}_\textbf{sol} (j)  c_{p,t}('Dec_{Solar}',h,td)
    :label: eq:op_strategy_dec_total_ST

    \forall j \in \text{TECH OF EUT} (\text{HeatLowTDec}) \setminus \{ 'Dec_{Solar}' \}, \forall h\in H, \forall td \in TD


\endgroup  
Thermal solar is implemented as a decentralized technology. It is always
installed together with another decentralized technology, which serves
as backup to compensate for the intermittency of solar thermal. Thus, we
define the total installed capacity of solar thermal
**F**\ ('':math:`Dec_{solar}`'') as the sum of **F\ sol**\ (:math:`j`),
Eq. :eq:`eq:de_strategy_dec_total_ST`,
where :math:`\textbf{F}_{\textbf{sol}}(j)` is the solar thermal
capacity associated to the backup technology :math:`j`.
Eq. :eq:`eq:op_strategy_dec_total_ST`
links the installed size of each solar thermal capacity
:math:`\textbf{F}_{\textbf{sol}}(j)` to its actual production
::math:`\textbf{F}_{\textbf{t}_\textbf{sol}}(j,h,td))` via the
solar capacity factor (:math:`c_{p,t}('Dec_{solar}')`).

.. math::
    \textbf{F}_\textbf{t} (j,h,td) + \textbf{F}_{\textbf{t}_\textbf{sol}} (j,h,td)  
    :label: eq:heat_decen_share

    + \sum_{l \in \text{L}}\Big( \textbf{Sto}_\textbf{out} (i,l,h,td) - \textbf{Sto}_\textbf{in} (i,l,h,td) \Big)

    = \textbf{%}_\textbf{HeatDec}(\text{j}) \textbf{EndUses}(HeatLowT,h,td) 

    \forall j \in \text{TECH OF EUT} (\text{HeatLowTDec}) \setminus \{ 'Dec_{Solar}' \}, 

    i \in \text{TS OF DEC TECH}(j)  , \forall h\in H, \forall td \in TD


.. figure:: /images/model_formulation/ts_and_Fsolv2.png
   :alt: Illustrative example of a decentralised heating layer.
   :name: fig:FsolAndTSImplementation
   :width: 12cm

   Illustrative example of a decentralised heating layer with thermal
   storage, solar thermal and two conventional production technologies,
   gas boilers and electrical HP. In this case,
   Eq. :eq:`eq:heat_decen_share` applied to the
   electrical HPs becomes the equality between the two following terms:
   left term is the heat produced by: the eHPs
   (:math:`\textbf{F}_{\textbf{t}}('eHPs',h,td)`), the solar panel
   associated to the eHPs
   (:math:`\textbf{F}_{\textbf{t}_\textbf{sol}}('eHPs',h,td)`) and
   the storage associated to the eHPs; right term is the product between
   the share of decentralised heat supplied by eHPs
   (:math:`\textbf{%}_{\textbf{HeatDec}}('eHPs')`) and heat low temperature decentralised
   demand (:math:`\textbf{EndUses}(HeatLowT,h,td)`).

A thermal storage :math:`i` is defined for each decentralised heating
technology :math:`j`, to which it is related via the set *TS OF DEC TECH*,
i.e. :math:`i`\ =\ *TS OF DEC TECH(j)*. Each thermal storage :math:`i` can store
heat from its technology :math:`j` and the associated thermal solar
:math:`\textbf{F}_{\textbf{sol}}` (:math:`j`). Similarly to the passenger mobility,
Eq. :eq:`eq:heat_decen_share` makes the model
more realistic by defining the operating strategy for decentralized
heating. In fact, in the model we represent decentralized heat in an
aggregated form; however, in a real case, residential heat cannot be
aggregated. A house heated by a decentralised gas boiler and solar
thermal panels should not be able to be heated by the electrical heat
pump and thermal storage of the neighbours, and vice-versa. Hence,
Eq. :eq:`eq:heat_decen_share` imposes that the
use of each technology (:math:`\textbf{F}_{\textbf{t}}(j,h,td)`),
plus its associated thermal solar
(:math:`\textbf{F}_{\textbf{t}_\textbf{sol}}(j,h,td)`) plus
its associated storage outputs
(:math:`\textbf{Sto}_{\textbf{out}}(i,l,h,td)`) minus its associated
storage inputs (:math:`\textbf{Sto}_{\textbf{in}}(i,l,h,td)`) should
be a constant share (:math:`\textbf{%}_{\textbf{HeatDec}}(j)`) of the decentralised heat
demand :math:`(\textbf{EndUses}(HeatLowT,h,td)`). :numref:`Figure %s <fig:FsolAndTSImplementation>` shows, through an example with
two technologies (a gas boiler and a HP), how decentralised thermal
storage and thermal solar are implemented.

Vehicle-to-grid
^^^^^^^^^^^^^^^

.. figure:: /images/model_formulation/v2gAndBatteries.png
   :alt: Illustrative example of a V2G implementation.
   :name: fig:V2GAndBatteries
   :width: 7cm

   Illustrative example of a V2G implementation. The battery can
   interact with the electricity layer. 
   The size of the battery is directly related to the number of cars (see Eq. :eq:`eq:SizeOfBEV`). 
   The V2G takes the electricity from the battery to provide a constant share (:math:`\textbf{%}_{\textbf{PassMob}}`) of the
   passenger mobility layer (*Mob. Pass.*). Thus, it imposes the amount of electricity that electric car must deserve (see Eq. :eq:`eq:BtoBEV`).
   The remaining capacity of battery available can be used to provide V2G services (see :eq:`eq:LimitChargeAndDischarge_ev`). 
   

.. math::
    \textbf{F} (i) = \frac{\textbf{F} (j)}{ veh_{capa} (j)} ev_{batt,size} (j)  ~~~~~~ \forall  j \in  V2G, i \in \text{EVs_BATT OF V2G}(j)
    :label: eq:SizeOfBEV

Vehicle-to-grid dynamics are included in the model via the *V2G* set.
For each vehicle :math:`j \in V2G`, a battery :math:`i` (:math:`i`
:math:`\in` *EVs_BATT*) is associated using the set EVs_BATT_OF_V2G
(:math:`i \in \text{EVs_BATT_OF_V2G}(j)`). Each type :math:`j`
of *V2G* has a different size of battery per car
(:math:`ev_{batt,size}(j)`), e.g. the first generation battery of the
Nissan Leaf (ZE0) has a capacity of 24 kWh [10]_. The number of vehicles
of a given technology is calculated with the installed capacity (**F**)
in [km-pass/h] and its capacity per vehicles (:math:`veh_{capa}` in
[km-pass/h/veh.]). Thus, the energy that can be stored in batteries
**F**\ (:math:`i`) of *V2G*\ (:math:`j`) is the ratio of the installed capacity of
vehicle by its specific capacity per vehicles times the size of battery
per car (:math:`ev_{batt,size}(j)`), Eq. 
:eq:`eq:SizeOfBEV`. As an example, if this technology
of cars covers 10 Mpass-km/h, and the capacity per vehicle is 50.4
pass-km/car/h (which represents an average speed of 40km/h and occupancy
of 1.26 passenger per car); thus, the amount of BEV cars are 0.198
million cars. And if a BEV has a 24kWh of battery, such as the Nissan
Leaf (ZE0), thus, the equivalent battery has a capacity of 4.76 GWh.


.. math::
    \textbf{Sto}_\textbf{out} (j,Elec,h,td) \geq - f(i,Elec) \textbf{F}_\textbf{t} (i,h,td) 
    :label: eq:BtoBEV

    \forall i \in V2G , \forall j \in \text{EVs_BATT OF V2G}(j), \forall h \in H, td \in TD 




Eq. :eq:`eq:BtoBEV` forces batteries of electric vehicles
to supply, at least, the energy required by each associated electric
vehicle technology. This lower bound is not an equality; in fact,
according to the V2G concept, batteries can also be used to support the
grid. :numref:`Figure %s <fig:V2GAndBatteries>` shows through an example
with only BEVs how Eq. :eq:`eq:BtoBEV` simplifies the
implementation of V2G. In this illustration, a battery technology is
associated to a BEV. The battery can either supply the BEV needs or
sends electricity back to the grid.

.. math::
    \textbf{Sto}_\textbf{in} (j,l,h,td)t_{sto_{in}}(\text{j}) + \Big(\textbf{Sto}_\textbf{out}(j,l,h,td) + f(i,Elec) \textbf{F}_\textbf{t} (i,h,td) \Big) \cdot t_{sto_{out}}(\text{j})
    :label: eq:LimitChargeAndDischarge_ev

    \leq \Big( \textbf{F} (j) - \frac{\textbf{F} (j)}{ veh_{capa} (j)} ev_{batt,size} (j) \Big) \cdot \%_{sto_{avail}}(j)

    \forall i \in V2G , \forall j \in \text{EVs_BATT OF V2G}(j) , \forall l \in L, \forall h \in H, \forall td \in TD

Eq. :eq:`eq:LimitChargeAndDischarge_ev` limits the availability of batteries to the number of vehicle connected to the grid.
This equation is similar to the one for other type of storage (see Eq. :eq:`eq:LimitChargeAndDischarge`); 
except that a part of the batteries are not accounted, i.e. the one running (see Eq. :eq:`eq:BtoBEV`). 
Therefore, the available output is corrected by removing the electricity powering the running car (here, :math:`f(i,Elec) \leq 0`) 
and the available batteries is corrected by removing the numbers of electric cars running (:math:`\frac{\textbf{F} (j)}{ veh_{capa} (j)} ev_{batt,size} (j)`).

.. math::
    \textbf{Sto}_\textbf{level} (j,t) \geq \textbf{F}[i] soc_{ev}(i,h)
    :label: eq:EV_min_state_of_charge

    \forall i \in V2G , \forall j \in \text{EVs_BATT OF V2G}(j) , \forall t \in T| \{h,td\} \in T\_H\_TD

For each electric vehicle (:math:`ev`), a minimum state of charge is imposed for each hour of the day \big(:math:`soc_{ev}(i,h)`\big). 
As an example, we can impose that the state of charge of EV is 60% in the morning, to ensure that cars can be used to go for work. 
Eq. :eq:`eq:EV_min_state_of_charge` imposes, for each type of `V2G`, 
that the level of charge of the EV batteries is greater than the minimum state of charge times the storage capacity.


Peak demand
^^^^^^^^^^^

.. math::
    \textbf{F} (j) 
    \geq
    \%_{Peak_{sh}}\max_{h\in H,td\in TD}\left\{\textbf{F}_\textbf{t}(j,h,td)\right\}
    :label: eq:dec_peak

    \forall j \in \text{TECH OF  EUT} (HeatLowTDEC)   \setminus \{ 'Dec_{Solar}'\}

.. math::
    \sum_{\hspace{3cm}j \in \text{TECH OF EUT} (HeatLowTDHN), i \in \text{STO OF EUT}(HeatLowTDHN)}
    :label: eq:dhn_peak
    
    \Big( \textbf{F} (j)+
    \textbf{F} (i)/t_{sto_{out}}(i,HeatLowTDHN)  \Big)
    
    \geq
    \%_{Peak_{sh}} \max_{h\in H,td\in TD}  \big\{ \textbf{EndUses}(HeatLowTDHN,h,td) \big\}
  
Finally,
Eqs. :eq:`eq:dec_peak` - :eq:`eq:dhn_peak`
constrain the installed capacity of low temperature heat supply. Based
on the selected TDs, the ratio between the yearly peak demand and the
TDs peak demand is defined for space heating (:math:`\%_{Peak_{sh}}`).
Eq. :eq:`eq:dec_peak` imposes that the installed
capacity for decentralised technologies covers the real peak over the
year. Similarly, Eq. :eq:`eq:dhn_peak` forces the
centralised heating system to have a supply capacity (production plus
storage) higher than the peak demand. These equations force the
installed capacity to meet the peak heating demand, i.e. which
represents, somehow, the network adequacy  [11]_.

.. _sssec_lp_adaptation_case_study:

Adaptations for the case study
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Additional constraints are required to implement scenarios. Scenarios
require six additional constraints
(Eqs. :eq:`eq:LimitGWP` - :eq:`eq:solarAreaLimited`)
to impose a limit on the GWP emissions, the minimum share of RE primary
energy, the relative shares of technologies, such as gasoline cars in
the private mobility, the cost of energy efficiency measures, the
electricity import power capacity and the available surface area for
solar technologies.


.. math::
    \textbf{GWP}_\textbf{tot} \leq gwp_{limit}  
    :label: eq:LimitGWP

.. math::
    \sum_{j \in  \text{RES}_\text{re},t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(j,h,td)  \cdot  t_{op} (h,td)   
    :label: eq:LimitRE
    
    \geq 
    re_{share} \sum_{j \in \text{RES} ,t \in T| \{h,td\} \in T\_H\_TD(t)} \textbf{F}_\textbf{t}(j,h,td) \cdot  t_{op} (h,td)
    

To force the Belgian energy system to decrease its emissions, two lever
can constraint the annual emissions:
Eq. :eq:`eq:LimitGWP` imposes a maximum yearly
emissions threshold on the GWP (:math:`gwp_{limit}`); and
Eq. :eq:`eq:LimitRE` fixes the minimum renewable primary
energy share.

.. math::
    f_{\text{min,\%}}(j) \sum_{j' \in \text{TECH OF EUT} (eut),t \in T|\{h,td\} \in T\_H\_TD(t)}    \textbf{F}_\textbf{t}(j',h,td)\cdot t_{op}(h,td)  
    :label: eq:fmin_max_perc
    
    \leq 
 	\sum_{t \in T|\{h,td\} \in T\_H\_TD(t)}  \textbf{F}_\textbf{t} (j,h,td)\cdot t_{op}(h,td) 
    
    \leq 
    f_{\text{max,\%}}(j) \sum_{j'' \in \text{TECH OF EUT} (eut),t \in T|\{h,td\} \in T\_H\_TD(t)}    \textbf{F}_\textbf{t}(j'',h,td)\cdot t_{op}(h,td) 
    
    \forall eut \in EUT, \forall j \in \text{TECH OF EUT} (eut) 


To represent the Belgian energy system in 2015,
Eq. :eq:`eq:fmin_max_perc` imposes the relative
share of a technology in its sector.
Eq. :eq:`eq:fmin_max_perc` is complementary to
Eq. :eq:`eq:fmin_fmax`, as it expresses the minimum
(:math:`f_{min,\%}`) and maximum (:math:`f_{max,\%}`) yearly output shares of each
technology for each type of EUD. In fact, for a given technology,
assigning a relative share (e.g. boilers providing at least a given
percentage of the total heat demand) is more intuitive and close to the
energy planning practice than limiting its installed size. :math:`f_{min,\%}`
and :math:`f_{max,\%}` are fixed to 0 and 1, respectively, unless otherwise
indicated.

.. math::
    \textbf{F}(Efficiency) =  \frac{1}{1+i_{rate}} 
    :label: eq:efficiency

To account for efficiency measures from today to the target year,
Eq. :eq:`eq:efficiency` imposes their cost. The EUD
is based on a scenario detailed in 
`Data for end use demand <#sec:app1_end_uses>`__ and has a lower energy demand
than the “business as usual” scenario, which has the highest energy
demand. Hence, the energy efficiency cost accounts for all the
investment required to decrease the demand from the “business as usual”
scenario and the implemented one. As the reduced demand is imposed over
the year, the required investments must be completed before this year.
Therefore, the annualisation cost has to be deducted from one year. This
mathematically implies to define the capacity of efficiency measures
deployed to :math:`1/ (1+i_{rate})` rather than 1. The investment is
already expressed in €\ :sub:`2015`.

.. math::
    \textbf{F}_{\textbf{t}}(Electricity,h,td) \leq  elec_{import,max} ~~~~~~ \forall h \in H, \forall td \in TD
    :label: eq:elecImpLimited

.. math::
    \textbf{F}_{\textbf{t}}(i,h,td) \cdot t_{op} (h,td) =  \textbf{Import}_{\textbf{constant}}(i) ~~~~~~ \forall i \in \text{RES_IMPORT_CONSTANT}, h \in H, \forall td \in TD
    :label: eq:import_resources_constant



Eq. :eq:`eq:elecImpLimited` limits the power grid
import capacity from neighbouring countries based on a net transfer
capacity (:math:`elec_{import,max}`). Eq. :eq:`eq:import_resources_constant` imposes that some resources are imported at a constant power. 
As an example, gas and hydrogen are supposed imported at a constant flow during the year. 
In addition to offering a more realistic representation, this implementation makes it possible to visualise the level of storage within the region (i.e. gas, petrol ...).

.. caution::
    Adding too many ressource to Eq. :eq:`eq:import_resources_constant` increase drastically the computational time. 
    In this implementation, only resources expensive to store have been accounted: hydrogen and gas. 
    Other resources, such as diesel or ammonia, can be stored at a cheap price with small losses.
    By limiting to two types of resources (hydrogen and gas), the computation time is below a minute.
    By adding all resources, the computation time is above 6 minutes.


.. math::
    \textbf{F}(PV)/power\_density_{pv} 
    :label: eq:solarAreaLimited

    + \big( \textbf{F}(Dec_{Solar}) + \textbf{F}(DHN_{Solar}) \big)/power\_density_{solar~thermal}  \leq solar_{area}

In this model version, the upper limit for solar based technologies is
calculated based on the available land area (*solar\ area*) and power
densities of both PV (:math:`power\_density_{pv}`) and solar thermal
(:math:`power\_density_{solar~thermal}`),
Eq. :eq:`eq:solarAreaLimited`. The equivalence
between an install capacity (in watt peaks Wp) and the land use (in
:math:`km^2`) is calculated based on the power peak density
(in [Wp/m\ :math:`^2`]). In other words, it represents the peak power of a
one square meter of solar panel. We evaluate that PV and solar thermal
have a power peak density of :math:`power\_density_{pv}` =0.2367 and
:math:`power\_density_{solar~thermal}` =0.2857 [GW/km\ :math:`^2`] [12]_. Thus,
the land use of PV is the installed power (:math:`\textbf{F}(PV)` in [GW])
divided by the power peak density (in [GW/km\ :math:`^2`]). This area is
a lower bound of the real installation used. Indeed, here, the
calculated area correspond to the installed PV. However, in utility
plants, panels are oriented perpendicular to the sunlight. As a
consequence, a space is required to avoid shadow between rows of panels.
In the literature, the *ground cover ratio* is defined as the total
spatial requirements of large scale solar PV relative to the area of the
solar panels. This ratio is estimated around five
:cite:`dupont2020global`, which means that for each square
meter of PV panel installed, four additional square meters are needed.

.. _ssec_estd_implementation:

Implementation
--------------

The formulation of the MILP and LP problems has been implemented using
an algebraic modeling language. The latter allows the representation of
large LP and MILP problems. Its syntax is similar to AMPL, which is -
according to the NEOS-statistics [13]_ - the most popular format for
representing mathematical programming problems. The formulation enable
the use of different solvers as open sources ones, such as GLPK, or
commercial ones, such as CPLEX or Gurobi. In the code, each of the
equations defined above is found as it is with the corresponding
numbering. SETS, Variables and parameters have the same names (unless
explicitly stated in the definition of the term). :numref:`Figure %s <fig:ch2_LP_formulation_implementation_colored>` illustrates -
for the balance constraint :eq:`eq:layer_balance` - the mathematical
formulation presented in this work and its implementation in the code.
Colors highlight the same elements. In the implementation, each
constraint has a comment (starting with #) and has a name (colored in
black), in this case *layer_balance*. In addition, most of the SETS,
Variables and parameters are more explicitly named, as a first example
the set layers is named *L* in the paper and *LAYERS* in the
implementation; or as another example, the input efficiency who is named
*f* in the paper and *layers_in_out* in the implementation.

.. figure:: /images/model_formulation/eqs_color.png
   :alt: Comparison of equation formulation and code. This is the equation
 
.. figure:: /images/model_formulation/ch_estd_code_screenshot.png
   :alt: Comparison of equation formulation and code.
   :name: fig:ch2_LP_formulation_implementation_colored

   Comparison of equation formulation (upper equation) and code
   implementation (lower figure). Example based on Eq.
   :eq:`eq:layer_balance`.

The entire implementation is available on the directory
:cite:`ESTD_v2_1_repo` and its architecture is illustrated
in :numref:`Figure %s <fig:ch2_estd_repo_structure>`. Four folders compose
the repository and contain the documentation (``Documentation``), the
data used (``Data_management``), the MILP implementation
(``STEP_1_TD_selection``) and the LP implementation
(``STEP_2_Energy_Model``). For each of the models, the definition of the
terms (SETS, Variables and Parameters) as well as the domains of the
variables, the formulation of the constraints and the objective function
are included in the model file (with the extension ``.mod``). The
numerical values of the parameters are contained in separate files (with
the extension ``.dat``). Finally, the output data of the model are saved
in a file (wit the extension ``.out``) or a folder (``\outputs``). An
interface - via excel - allows to visualise the data (``DATA.xlsx``) and
to generate the data files (``STEP_1_in.xlsx``, ``STEP_1_out.xlsx`` and
``STEP_2_in.xlsx``). Finally, a user guide manual is available in the
documentation to support the modeler in her/his first steps.

.. figure:: /images/model_formulation/ch_estd_repo_structure.png
   :alt: EnergyScope TD repository structure.
   :name: fig:ch2_estd_repo_structure

   EnergyScope TD repository structure available at
   :cite:`ESTD_v2_1_repo`.

.. [1]
    Passenger transport activity from aviation is accounted in passenger mobility (excluding international extra EU travels).

.. [2]
    Hydrogen can be produced based on many feed-stocks, among them electricity used for electrolysers.

.. [3]
   Indeed, some technologies have several outputs, such as a CHP. Thus,
   the installed size must be defined with respect to one of these
   outputs. As an example, CHP are defined based on the thermal output
   rather than the electrical one.

.. [4]
   To simplify the reading, the formulation
   :math:`t \in T| \{h,td\} \in T\_H\_TD(t)` is used. However, this
   cannot be directly implemented in the code and it requires two
   additional sets : :math:`HOUR\_OF\_PERIOD(t)` and
   :math:`TYPICAL\_DAY\_OF\_PERIOD(t)`. Hence, we have:
   :math:`t \in T| \{h,td\} \in T\_H\_TD(t)`, which is equivalent in the
   code to
   :math:`t \in T| h \in HOUR\_OF\_PERIOD(t), td \in TYPICAL\_DAY\_OF\_PERIOD(t)`.

.. [5]
   In most cases, the activation of the constraint stated in
   Eq. :eq:`eq:sto_level` will have as a consequence
   that the level of storage be the same at the beginning and at the end
   of each day — hence the use of the terminology ‘*daily storage*’.
   Note, however, that such daily storage behaviour is not always
   guaranteed by this constraint and thus, depending on the typical days
   sequence, a daily storage behaviour might need to be explicitly
   enforced.

.. [6]
   In the code, these equations are implemented with a *if-then*
   statement.

.. [7]
   In this linear formulation, storage technologies can charge and
   discharge at the same time. On the one hand, this avoids the need of
   integer variables; on the other hand, it has no physical meaning.
   However, in a cost minimization problem, the cheapest solution
   identified by the solver will always choose to either charge or
   discharge at any given :math:`t`, as long as cost and efficiencies
   are defined. Hence, we recommend to always verify numerically the
   fact that only storage inputs or outputs are activated at each
   :math:`t`, as we do in all our implementations.

.. [8]
   This is the ratio between the losses in the grid and the total annual
   electricity production in Belgium in 2015
   :cite:`Eurostat2017`.

.. [9]
   [foot:nonLinear]All equations expressed in a compact non-linear form
   in this section Eqs. :eq:`eq:mob_share_fix`, :eq:`eq:freight_share_fix`, 
   :eq:`eq:heat_decen_share` and :eq:`eq:dhn_peak` can be linearised. For these
   cases, the **EndUses** is defined with parameters and a variable
   representing a constant share over the year (e.g.  :math:`\textbf{%}_\textbf{public}`). As
   an example, **EndUses** in
   Eq. :eq:`eq:mob_share_fix` is equal to
   :math:`\textbf{EndUsesInput}(PassMb) \cdot %pass (h, td) / t_op (h, td)`.
   The term :math:`\textbf{%}_{\textbf{public}}`, is missing in the equation, but is implicitly
   implemented in :math:`\textbf{%}_{\textbf{PassMob}}`.

.. [10]
   This generation (ZE0) was marketed from 2010 to 2017 with a battery
   capacity of 24 kWh. The new generation (ZE1) accounts for an improved
   capacity and reaches 40 kWh per battery. Data from
   https://en.wikipedia.org/wiki/Nissan_Leaf, consulted on 08-02-2021

.. [11]
   The model resolution of the dispatch is not accurate enough to verify
   the adequacy. As one model cannot address all the issues, another
   approach has been preferred: couple the model to a dispatch one, and
   iterate between them. Percy and Coates
   :cite:`percy_coates_coupling_2020` demonstrated the
   feasibility of coupling a design model (ESTD) with a dispatch one
   (Dispa-SET :cite:`Quoilin2017`). Based on a feedback
   loop, they iterated on the design to verify the power grid adequacy
   and the strategic reserves. Results show that the backup capacities
   and storage needed to be slightly increased compared to the results
   of the design model alone.

.. [12]
   The calculation is based on the annual capacity factor, the
   conversion efficiency and the average yearly irradiation. As an
   example, for PV, the efficiency in 2035 is estimated at
   23% :cite:`DanishEnergyAgency2019` with an average daily
   irradiation - similar to historical values - of
   2820 Wh/m\ \ :math:`^2` in
   Belgium :cite:`IRM_Atlas_Irradiation`. The capacity
   factor of solar is around 11.4%, hence specific area for 1 kilowatt
   peak (:math:`kW_p`) is
   :math:`2820/24\cdot0.23/0.114\approx236.7`\ \ [:math:`MW_p`/km\ \ :math:`^2`]=\ \ :math:`0.2367`
   [:math:`GW_p`/km\ \ :math:`^2`].

.. [13]
   NEOS Server is an Internet-based client-server application that
   provides free access to a library of optimization solvers, statistics
   are available at: https://neos-server.org/neos/report.html, consulted
   the 27/01/2021.


