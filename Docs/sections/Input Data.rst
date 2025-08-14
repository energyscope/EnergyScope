.. _app:bestd_data:

Input Data
++++++++++

.. warning:: New and updated version of the documentation is available in this `library <https://www.energyscope.net/latest/>`_.

**Belgian energy system data in 2035**

..
   .. caution ::
      This section is still under construction.
      It is built from Limpens PhD thesis (2021) available at http://dx.doi.org/10.13140/RG.2.2.25755.18724 


.. role:: raw-latex(raw)
   :format: latex
..



Overview This appendix reports the input data for the application of the
LP modeling framework to the case study of Belgium between 2015 and
2050. Data are detailed for the year 2035 and 2015, the latter used for
model verification. Trends to extrapolated these data for the other
years are given. This appendix is an improved version previously
presented in :cite:`Limpens2019,Limpens_belgian_2020`

The data can be grouped into three parts: resources (Section `Resources <#app:sec:BESTD_resources>`__), demand (Section
`Demand <#sec:app1_end_uses>`__) and technologies (Section
`Technologies <#app:BESTD_data_technologies>`__.. For resources, the work of the JRC
:cite:`simoes2013jrc`, Biomass atlas
:cite:`elbersen2012atlas` and
:cite:t:`H2coalition2020shipping` have been used to
complement and confirm or correct the prices already reported in previous works
:cite:`Moret2017PhDThesis,Limpens2019,limpens2020impact`.
For energy demand, the annual demand is calculated from the work of the
European Commission’s projections up to 2050
:cite:`EuropeanCommission2016`. As a complement, the time
series are all calculated on the basis of the year 2015. For
technologies, they are characterised by the following characteristics:
energy balances, cost (investment and maintenance), and environmental
impact (global warming potential (GWP)). For weather dependent technologies (wind, solar, etc.), real
production for the year 2015 was collected from the TSO.

For GWP and GHG emissions, LCA data are taken from the Ecoinvent
database v3.2 [1]_ :cite:`weidema_ecoinvent_2013` using the
“allocation at the point of substitution” method. GWP is assessed with
the “GWP100a - IPCC2013” indicator. For technologies, the GWP impact
accounts for the technology construction; for resources, it accounts for
extraction, transportation and combustion. In addition, data for fuel
combustion are taken from :cite:t:`Quaschning2015`.

For the cost, the reported data are the nominal values for Belgium in
the year 2035 All costs are expressed in *real*\  [2]_ Euros for the
year 2015 (€\ :sub:`2015`). If not specified, € refers to
€\ :sub:`2015`. All cost data used in the model originally expressed in
other currencies or referring to another year are converted to
€\ :sub:`2015` to offer a coherent comparison. Most of the data come
from a previous work :cite:`Moret2017PhDThesis,Limpens2019`,
and were expressed in CHF\ :sub:`2015` (Based on the average annual
exchange rate value from ECB https://www.ecb.europa.eu, the annual rate
was 1€\ :sub:`2015` = 1.0679CHF\ :sub:`2015`). The method used for the
year conversion is illustrated by Eq. :eq:`eqn:currency_conv`.

.. math::
    c_{inv} [\text{€}_{2015}] = c_{inv} [C_y] \cdot  \frac{\text{USD}_y}{C_y}  \cdot \frac{\text{CEPCI}_{2015} \ [\text{USD}_{2015}]}{\text{CEPCI}_y \ [\text{USD}_y]} \cdot \frac{\text{€}_{2015}}{\text{USD}_{2015}} 
    :label: eqn:currency_conv

Where :math:`C` and :math:`y` are the currency and the year in which the
original cost data are expressed, respectively, USD is the symbol of
American Dollars and the CEPCI
:cite:`chemical_engineering_chemical_2016` is an index
taking into account the evolution of the equipment cost (values reported
in :numref:`Table %s <tbl:cepci>`). As an example, if the cost data are
originally in EUR\ :sub:`2010`, they are first converted to
USD\ :sub:`2010`, then brought to USD\ :sub:`2015` taking into account
the evolution of the equipment cost (by using the CEPCI), and finally
converted to €\ :sub:`2015`. The intermediate conversion to USD is
motivated by the fact that the CEPCI is expressed in *nominal* USD.
Although this conversion method is originally defined for
technology-related costs, in this paper as a simplification it used also
for the cost of resources.


.. container::

   .. table:: CEPCI values :cite:`chemical_engineering_chemical_2016`
      :name: tbl:cepci

      ======== =========
      **Year** **CEPCI**
      ======== =========
      1982     285.8
      1990     357.6
      1991     362.3
      1992     367.0
      1993     371.7
      1994     376.4
      1995     381.1
      1996     381.7
      1997     386.5
      1998     389.5
      1999     390.6
      2000     394.1
      2001     394.3
      2002     395.6
      2003     402.0
      2004     444.2
      2005     468.2
      2006     499.6
      2007     525.4
      2008     575.4
      2009     521.9
      2010     550.8
      2011     585.7
      2012     584.6
      2013     567.3
      2014     576.1
      2015     556.3
      ======== =========


.. The current appendix is built in three parts. At first, data are given
   for the year 2035 for resources (Section
   `Resources <#app:sec:BESTD_resources>`__), demand (Section
   `Demand <#sec:app1_end_uses>`__) and technologies (Section
   `Technologies <#app:BESTD_data_technologies>`__. Then, the year 2015 is discussed
   as real data have been collected for this case. And finally, the
   extension of the data from year 2035 to other years are detailed.

.. _app:sec:BESTD_resources:

Resources
=========

Resources can be regrouped in two categories: endogenous and exogenous.
In the case of Belgium, endogenous resources are exclusively renewables.
They account for solar, biomass, wind and hydro. The only endogenous
resource which is non renewable is waste. In addition, energy can be
imported from abroad (exogenous). These resources are characterised by
an import price and a maximum potential. Exogenous resources account for
the import of hydrocarbons, electricity or other fuels.

The availability of all resources, except for biomass, and non-RE waste,
is set to a value high enough to allow unlimited use in the model. 
:numref:`Table %s <tbl:prices_resources>` details the prices of
resources (:math:`c_{op}`), the GHG emissions (:math:`gwp_{op}`) associated to their
production, transportation and combustion; and endogenous availability
of resources. Export of electricity are possible, but they are
associated to a zero selling price. Two kinds of emissions are proposed:
one accounting for the impact associated to production, transport and
combustion (based on GWP100a -
IPCC2013 :cite:`Moret2017PhDThesis`); the other accounting
only for combustion (based on :cite:t:`Quaschning2015`).
Total emissions are used to assess energy system emissions. Combustion
only is used to calculate the direct CO2 emissions that can be captured
and used through a carbon capture technology (latter presented).

Local renewable resources
-------------------------

The majors renewable potentials are: solar, biomass and wind.
Additionnaly, Belgium has hydro and perhaps affordable geothermal. Wind,
solar, hydro and geothermal are limited by the number of technologies
deployable, while biomass is limited by the amount of resources
available.

Wind, solar, hydro and geothermal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The energy transition relies on renewable energies, which makes their
deployment potential a critical parameter. In 2015, 6% of the primary
energy consumed in Belgium was renewable, mainly biomass, solar and
wind. In the following, we summarise the potential for the different
resources: in terms of available potential for biomass and waste (:numref:`Table %s <tab:renewableResourcesPotentialIn2035>`);
or in terms of capacity for solar, wind, geothermal and hydro (:numref:`Table %s <tab:renewableTechPotentialIn2035>`).
These data are put into perspective with the real data for 2015.

.. container::

   .. csv-table:: Comparison of installed capacity of renewable energies (RE) based technologies in 2015 and their potentials in the model. Abbreviations: centralised (cen.), decentralised (dec.), maximum (max.).
      :header: **Technology**, **2015**\  [aa]_ , **max. potential** , **Units**
      :widths: 15 15 15 15
      :name: tab:renewableResourcesPotentialIn2035
   
      photovoltaic , 3.85 , :math:`\approx`\ 60 [bb]_ , [GW]
      onshore wind , 1.18 , 10 [cc]_ , [GW]
      offshore wind , 0.69 , 3.5 , [GW]
      hydro river , 0.11 [dd]_ , 0.120 , [GW]
      geothermal , 0 , :math:`\approx`\ 0 [ee]_ , [GW]
      geothermal , :math:`\approx`\ 0 , :math:`\approx`\ 0 , [GW]
      cen. solar th. , 0 , :math:`\approx` 70 , [GW]
      dec. solar th. , 0 , :math:`\approx` 70 , [GW]


   .. [aa]
      Data from :cite:`Limpens_belgian_2020` consistent with Eurostat :cite:`EurostatEnergyBalanceSheets2015`.

   .. [bb]
      Due to land availability, the solar potentials
      are limited to around 1% of total Belgian lands
      (250km\ \ :math:`^2`). This is equivalent to :math:`\approx`\ \ 60 GW
      of PV or :math:`\approx`\ \ 70 GW of solar thermal.

   .. [cc]
      From :cite:`limpens2018electricity`.
      In line with :cite:`EliaSystemOperator2017` which
      estimated 9 GW for onshore and 8 GW for offshore.

   .. [dd]
      In 2015, the production was
      360 GWh :cite:`EuropeanCommission2016` with an installed
      capacity of around 110 MW :cite:`Devogelaer2013`. No
      important development is
      foreseen :cite:`Devogelaer2013,EliaSystemOperator2017`.

   .. [ee]
      A prototype (Balmatt project) started in 2019 and should produce
      4-5 MW :cite:`VITO_Website`.

.. container::

   .. csv-table:: Renewable resources in 2015 and their potential.
      :header: **Resources** , **2015** , **max. potential** , **Units**
      :widths: 15 15 15 15
      :name: tab:renewableTechPotentialIn2035

		bioethanol , 0.48 [ff]_ , 0 , [TWh]
		biodiesel , 2.89 , 0 , [TWh]
		SNG , 0 , 0 , [TWh]
		H2 , 0 , 0 , [TWh]
		woody [gg]_ , 13.9 , 23.4 , [TWh]
		wet , 11.6 [hh]_ , 38.9 , [TWh]
		waste (non-RE), 7.87 , 17.8 , [TWh]
      
   .. [ff]
      Bioethanol also accounts for other bio-fuels
      except biodiesel. In 2015, 0.21 TWh of bioethanol have been imported,
      the rest of the biofuels have been produced locally from crops
      :raw-latex:`\cite{EurostatEnergyBalanceSheets2015}`. In the model,
      the crops available to produce sustainable biomass are accounted for,
      and can produce wet or woody biomass.

   .. [gg]
      Endogenous potential. See following section.

   .. [hh]
      Belgium production of bioethanol, biomethanol, biogas and biodiesel
      is accounted for as wet biomass.

Wind, solar and biomass are foreseen to be the main resources. The land
availability for PV is highly speculative, we propose a simple approach
to estimate an order of magnitude of this limit. Assuming that it exists
today 250 km\ :math:`^2` of available well oriented
roof [9]_ :cite:`Devogelaer2013` and that the efficiency in
2035 will be 23% :cite:`DanishEnergyAgency2019` with an
average daily total irradiation - similar to historical values - of
2820 Wh/m\ :math:`^2` in
Belgium :cite:`IRM_Atlas_Irradiation`. The upper limit
becomes 59.2 GW of installed capacity [10]_. This limit is in line with
a study performed by the Belgian TSO which proposes arbitrarily
40 GW :cite:`EliaSystemOperator2017`. The hydro potential is
very limited and almost fully exploited. Even if geothermal heat is used
for heating through DHN since 1986 at Saint
Ghislain :cite:`Delmer1997`, research about the geothermal
potential in Belgium are at their early stages. In 2015, a new project
started (the Balmatt project). Nowadays, the installation produces
1.5 MW of electricity (in 2019). The project is expected to scale up to
5 MW of electricity :cite:`VITO_Website`. However, there is
no large facility yet and the potential is not accurately estimated. A
study performed by the VITO evaluates the potential in Flanders to
3.1 GWe and they extend it to 4 GWe for the whole Belgian
potential :cite:`Devogelaer2013`. However, because of a lack
of reliable sources about geothermal potential, we consider the
potential as null in the reference scenario.

The wind potential is estimated to 10 GW onshore and 3.5 GW offshore
:cite:`limpens2018electricity`. At the time of collecting
the data (2011-2020), several potentials can be collected through
various sources. As an example, the study from
:cite:t:`Devogelaer2013` proposes to use 9 GW and 8 GW for
onshore and offshore, respectively. As another example,
:cite:t:`Dupont2017` estimates the wind potential based on
its energy return on invested energy, in other words, its profitability.
This study concluded that Belgium has a potential between 7 660 and
24 500 MW for onshore and between 613 and 774 MW for offshore [11]_. At
the time of writing, the wind energy is in the spotlight with collapsing
investment costs and a rising potential. Indeed, Europe has one of the
best potential worldwide and has a leading wind power industry. As an
illustration of recent improvements the following argument motivates the
increase of the Belgian wind potential: taller and taller wind turbines
enable the use of faster and more constant wind. As a consequence, the
offshore potential might be underestimated. On the other hand, the
onshore potential might be overestimated as developers see their project
often blocked by citizens. In a nutshell, the wind potential allowed is
relevant, but perhaps slightly underestimated. As motivated in the
results, due to its limited potential, wind will remain a small
contributor of the energy mix with a maximum of :math:`\approx`\ 10%.



Biomass and non-RE waste
~~~~~~~~~~~~~~~~~~~~~~~~


In the literature, waste and biomass are often merged, as it is the case
in the European commission report
:cite:`EuropeanCommission2016`. In this thesis, a
distinction is made between *biomass* and *waste*. Waste accounts for
all the fossil waste, such as plastics, whereas biomass is organic and
assumed renewable. Biomass is split into two categories: one that can be
digested by bacteria (*wet biomass*), such as apple peel; and one that
cannot (*woody biomass*), such as wood. Hence, the organic waste
generated by the municipalities is accounted for in *woody or wet
biomass* and not as fossil waste.

In the literature, biomass potential highly varies based on the
assumptions made, such as the area available to produce biomass, or the
definition of sustainable biomass.
In an European study, :cite:t:`elbersen2012atlas` drew the
biomass atlas of EU countries for different scenarios in terms of prices
and potentials. According to a conservative approach, the sustainable
scenario estimations are selected. In their work, biomass is declined in
a larger variety of form. To adapt these data to our work, these
varieties are aggregated into three types: woody biomass, wet biomass
and non-RE waste. Waste accounts for common sludges, MSW landfill, MSW
not landfill (composting, recycling) and paper cardboard. The overall
potential is estimated to 17.8 TWh/y with an approximate price of
10.0 €/MWh. The price is estimated as a weighted sum between the
different variety and their specific price (given in the document). Wet
biomass accounts for all the digestible biomass, which are verge gras,
perennials (grassy), prunings, total manure, grass cuttings abandoned
grassland, animal waste and forrage maize (biogas). The overall
potential is estimated to 38.9 TWh/y with an approximate price of
2.5 €/MWh. Woody biomass accounts for all the non-digestible biomass,
which are roundwood (including additional harvestable roundwood), black
liquor, landscape care wood, other industrial wood residues, perennials
(woody), post consumer wood, saw-dust, sawmill by-products (excluding
sawdust) and primary forestry residues. The overall potential is
estimated to 23.4 TWh/y with an approximate price of 14.3 €/MWh.

Oleaginous (0.395 TWh/y) and sugary (0 TWh/y) potentials are two order
of magnitude below the previous categories and thus neglected.

However, these costs do not account for treatment and transportation.
Based on a local expert (from Coopeos), a MWh of wood ready to use for
small wood boilers is negotiated around 28 €/MWh today, twice much than
estimated prices. This order of magnitude is in line with the Joint
Research Center price estimation in 2030
:cite:`simoes2013jrc`. Thus, the price proposed in
:cite:`elbersen2012atlas` are doubled. It results in prices
for woody biomass, wet biomass and waste of 28.5, 5.0 and 20.0  €/MWh in
2015, respectively. The price for biomass is expected to increase by
27.7% up to 2050 :cite:`simoes2013jrc`. By adapting these
value to 2035, the prices are for 32.8 €/MWh woody biomass, 5.8 €/MWh
for wet biomass and for 23.1 €/MWh for waste.

Imported resources
------------------


Dominating fossil fuels are implemented in the model and detailed in
Section
`[ssec:case_study_imported_res] <#ssec:case_study_imported_res>`__. They
can be regrouped in hydrocabons (gasoline, diesel, LFO and NG), coal and
uranium. Data is summarised in :numref:`Table %s <tbl:prices_resources>` and are compared to
other sources, such as estimations from the JRC of prices for oil, gas
and coal :cite:`simoes2013jrc`. They base their work on a
communication of the European Commission
:cite:`eu2011roadmap`.


There are a long list of candidate to become renewable fuels. Historically, biomass has been converted into bio-fuels. 
Two types of these fuels are accounted: bio-diesel and bio-ethanol. They can substitute diesel and gasoline, respectively. 
More recently, a new type of renewable fuel is proposed and can be labeled electro-fuels. Indeed, these fuels are produced from electricity. 
We consider that the energy content of these fuels is renewable (i.e. from renewable electricity). 
Four type of fuels were considered: hydrogen, ammonia, methanol and methane. 
To avoid ambiguity between renewable fuels and their fossil equivalent, it is specified if the imported resources is renewable or fossil. 


.. caution::
   to be updated + explain where data comes from.

The only difference being 
Thus, we have gas and gas_re, or h2 and h2_re. Gas refers to what is usually called 'natural gas', while gas_re refers to methane from biogas, methanation of renewable hydrogen,...
Since, a specific study for the Belgian case has been conducted by a consortium of industries, :cite:t:`H2coalition2020shipping`, which estimate new prices for the imports.
:numref:`Table %s <tbl:prices_resources>` summarises all the input data for the resources.


.. container::

   .. table:: Price, GHG emissions and availability of resources, in 2035. Abbreviations: Liquid Fuel Oil (LFO), Natural Gas (NG) and Synthetic Natural Gas (SNG).
      :name: tbl:prices_resources

      +-------------+-------------+-------------+-------------+-------------+
      | **Res\      | :math:`c_   | :math:`gwp_ | :math:`{CO}_| *avail*     |
      | ources**    | {op}`       | {op}`       | {2direct}`  |             |
      |             |             |             | [26]_       |             |
      +-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :sub:`2\| [kgCO\      | [kgCO\      | [GWh]       |
      |             | 015`/MWh\   | :sub:`2-eq.`| :sub:`2-eq.`|             |
      |             | :sub:`fuel`]| /MWh\       | /MWh\       |             |
      |             |             | :sub:`fuel`]| :sub:`fuel`]|             |
      +-------------+-------------+-------------+-------------+-------------+
      | Electricity | 84.3 [27]_  | 206.4 [28]_ | 0           | 27.5        |
      | Import      |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Gasoline    | 82.4 [29]_  | 345 [28]_   | 250         | infinity    |
      |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Diesel      | 79.7 [30]_  | 315 [28]_   | 270         | infinity    |
      |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | LFO         | 60.1 [31]_  | 311.5 [28]_ | 260         | infinity    |
      |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Fossil      | 44.3 [32]_  | 267 [28]_   | 200         | infinity    |
      | Gas         |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Woody       | 32.8        | 11.8 [28]_  | 390         | 23.4        |
      | biomass     |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Wet-biomass | 5.8         | 11.8 [28]_  | 390         | 38.9        |
      +-------------+-------------+-------------+-------------+-------------+
      | non-RE      | 23.1        | 150  [28]_  | 260 [33]_   | 17.8        |
      | waste       |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Coal        | 17.6        | 401         | 360         | 33.3 [37]_  |
      |             |             | :cite:`\    |             |             |
      |             |             | we\         |             |             |
      |             |             | idema_ecoin\|             |             |
      |             |             | vent_2013`  |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Uranium     | 3.9 [34]_   | 3.9         | 0           | infinity    |
      |             |             | :cite:`\    |             |             |
      |             |             | we\         |             |             |
      |             |             | idema_ecoin\|             |             |
      |             |             | vent_2013`  |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Bio-diesel  | 120.0       | 0 [36]_     | 270         | infinity    |
      |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | B\          | 111.3 [35]_ | 0 [36]_     | 250         | infinity    |
      | io-gasoline |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Renew. gas  | 118.3       | 0 [36]_     | 200         | infinity    |
      |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Fossil  H2  | 87.5        | 364         | 0           | infinity    |
      | [25]_       |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Renew. H2   | 119.4       | 0 [36]_     | 0           | infinity    |
      |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Fossil      | 76          | 285         | 0           | infinity    |
      | Ammonia     |             |             |             |             |
      | [25]_       |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Renew.      | 81.8        | 0 [36]_     | 0           | infinity    |
      | Ammonia     |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Fossil      | 82.0        | 350         | 246         | infinity    |
      | Methanol    |             |             |             |             |
      | [25]_       |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+
      | Renew.      | 111.3       | 0 [36]_     | 246         | infinity    |
      | Methanol    |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+


.. [25]
   Own calculation for fossil hydrogen, ammonia and methanol. 
   Price and emissions are calculated based on fossil gas and based on conversion efficiencies.

.. [26]
   Direct emissions related to
   combustion:cite:`Quaschning2015`.

.. [27]
   Based on average market price in the year 2010 (50
   EUR\ \ :sub:`2010`/MWh, from
   :cite:`epex_spot_swissix_????`). Projected from 2010 to
   2035 using a multiplication factor of 1.36
   :cite:`prognos_ag_energieperspektiven_2012`. For security
   of supply reason, the availability is limited to 30% of yearly
   electricity EUD (See Section
   `[ssec:be_policies] <#ssec:be_policies>`__).

.. [28]
   GWP100a-IPCC2013 metric: impact associated to
   production, transport and combustion, see
   :cite:`Moret2017PhDThesis`

.. [29]
   Based on 1.49 CHF\ \ :sub:`2015`/L (average price in 2015 for
   gasoline 95 in Switzerland)
   :cite:`swiss_federal_office_of_statistics_sfos_ipc_2016`.
   Taxes (0.86 CHF\ \ :sub:`2015`/L,
   :cite:`beuret_evolution_2016`) are removed and the
   difference is projected from 2015 to 2035 using a multiplication
   factor of 1.24 :cite:`european_commission_energy_2011`.
   In line with :cite:`simoes2013jrc`.

.. [30]
   Based on 1.55 CHF\ \ :sub:`2015`/L (average price in 2015)
   :cite:`swiss_federal_office_of_statistics_sfos_ipc_2016`.
   Taxes (0.87 CHF\ \ :sub:`2015`/L,
   :cite:`beuret_evolution_2016`) are removed and the
   difference is projected from 2015 to 2035 using a multiplication
   factor of 1.24 :cite:`european_commission_energy_2011`.
   In line with :cite:`simoes2013jrc`.

.. [31]
   Based on 0.705 CHF\ \ :sub:`2015`/L (average price in 2015 for
   consumptions above 20000 L/y)
   :cite:`swiss_federal_office_of_statistics_sfos_indice_2016-1`.
   Taxes (0.22 CHF\ \ :sub:`2015`/L,
   :cite:`beuret_evolution_2016`) are removed and the
   difference is projected from 2015 to 2035 using a multiplication
   factor of 1.24 :cite:`european_commission_energy_2011`.
   In line with :cite:`simoes2013jrc`.

.. [32]
   Based on the EUC estimated cost of resources in
   2030, see Table 5 from :cite:`simoes2013jrc`.

.. [33]
   Assuming that the energy content can be assimilated to plastics and
   extended to LFO.

.. [34]
   Average of the data points for 2035 in
   :cite:`f._ess_kosten_2011`, accounting for the efficiency
   of nuclear power plants (:numref:`Table %s <tbl:nonrenew_elec>`).

.. [35]
   Data extrapolated from
   :cite:`brynolf2018electrofuels`


.. [36]
   Emissions related to electro-fuels
   and bio-fuels production are neglected.
   
.. [37]
   Belgium is phasing out coal. Coal is still used in industrial processes.
   In 2015, 33.3 TWh of coal were used. Thus, the amount available should be lower than this value.


.. _sec:app1_end_uses:

Energy demand and political framework
=====================================

The EUD for heating, electricity and mobility in 2035 is calculated from
the forecast done by the EUC in 2035 for Belgium (see Appendix 2 in
:cite:`EuropeanCommission2016`). However, in
:cite:`EuropeanCommission2016`, the FEC is given for heating
and electricity. The difference between FEC and EUD is detailed in
Section
`[ssec:conceptual_modelling_framework] <#ssec:conceptual_modelling_framework>`__
and can be summarised as follows: the FEC is the amount of input energy
needed to satisfy the EUD in energy services. Except for HP, the FEC is
greater than EUD. We applied a conservative approach by assuming that
the EUD equal to the FEC for electricity and heating demand.

.. _ssec:app1_electricity_end_uses:

Electricity
-----------

The values in table `1.3 <#tbl:elec_demand>`__ list the electricity
demand that is not related to heating for the three sectors in 2035. The
overall electricity EUD is given in
:cite:`EuropeanCommission2016`. However, only the FEC is
given by sectors. In order to compute the share of electricity by
sector, we assume that the electricity to heat ratio for the residential
and services remain constant between 2015 and 2035. This ratio can be
calculated from :cite:t:`EuropeanCommission-Eurostat.2018`,
these ratio of electricity consumed are 24.9% and 58.2% for residential
and services, respectively. As a consequence, the industrial electricity
demand is equal to the difference between the overall electricity demand
and the two other sectors.

A part of the electricity is assumed to be a fixed demand, such as
fridges in households and services, or industrial processes. The other
part is varying, such as the lighting demand. The ratio between varying
electricity and fixed demand are calculated in order to fit the real curve 
in 2015 (data provided by ENTSO-E
https://www.entsoe.eu/). It results in a share of 32.5% of varying electricity demand  
and 67.5% of baseload electricity demand.
demand of electricity is shared over the year according to *%\ elec*,
which is represented in  :numref:`Figure %s <fig:TS_elec>`. We use the real
2015 Belgian electricity demand (data provided by ENTSO-E
https://www.entsoe.eu/). *%\ elec* time series is the normalised value
of the difference between the real time series and its minimum value.

.. container::

   .. table:: Yearly electricity demand not related to heating by sector, in 2035.
      :name: tbl:elec_demand

      ========== =========== ============
      \          **Varying** **Constant**
      \          [TWh]       [TWh]
      Households 7.7         14.3
      Industry   11.1        33.7
      Services   11.0        14.1
      ========== =========== ============

.. figure:: /images/belgian_data/ts_elec_Belgium.png
   :alt: Normalised electricity time series over the year.
   :name: fig:TS_elec

   Normalised electricity time series over the year.


.. _ssec:app1_heating_end_uses:

Heating
-------

We applied the same methodology as in previous paragraph to compute the
residential, service heat yearly demand. The industrial heat processes
demand is assumed to be the overall industrial energy demand where
electricity and non energy use have been removed. Yearly EUD per sector
is reported in table `1.4 <#tbl:heat_demand>`__.

A part of the heat is assumed to be a fixed demand, such as hot water in
households and services, or industrial processes. The other part
represents the space heating demand and is varying. Similarly to the
electricity, the ratio between varying electricity and fixed demand are
the one of Switzerland, presented in
:cite:`Limpens2019,Moret2017PhDThesis` which are based on
:cite:`prognos_ag_energieperspektiven_2012`. The varying
demand of heat is shared over the year according to :math:`%_{sh}`. This time
series is based on our own calculation. The methodology is the
following: based on the temperature time series of Uccle 2015 (data from
IRM :cite:`Reyniers2012`); the HDH are calculated; and then
the time series. The HDH is a similar approach than the more commonly
used HDD. According to Wikipedia, HDD is defined as follows: “*HDD is a
measurement designed to quantify the demand for energy needed to heat a
building. HDD is derived from measurements of outside air temperature.
The heating requirements for a given building at a specific location are
considered to be directly proportional to the number of HDD at that
location. [...] Heating degree days are defined relative to a base
temperature*”. According to the European Environment Agency [37b]_, the
base temperature is 15.5\ :math:`^o`\ C, we took 16\ :math:`^o`\ C. HDH
are computed as the difference between ambient temperature and the
reference temperature at each hour of the year. If the ambient
temperature is above the reference temperature, no heating is needed.
:numref:`Figure %s <fig:HDD_BE_2015>` compares the result of our methodology
with real value collected by Eurostat [38]_. The annual HDD was 2633,
where we find 2507.

By normalising the HDH, we find :math:`%_{sh}`, which is represented in 

.. figure:: /images/belgian_data/belgium_HDD_2015.png
   :alt: Comparison of HDD between Eurostat and our own calculation.
   :name: fig:HDD_BE_2015

   Comparison of HDD between Eurostat and our own calculation.

.. figure:: /images/belgian_data/ts_sh_Belgium.png
   :alt: Normalised space heating time series over the year.
   :name: fig:TS_heat

   Normalised space heating time series over the year.

.. container::

   .. table:: Yearly heat end use demand per sector, in 2035.
      :name: tbl:heat_demand

      ========== ================= ============= ========================
      \          **Space heating** **Hot water** **Process heat**\  [39]_
      \          [TWh]             [TWh]         [TWh]
      Households 70.2              18.0          0
      Industry   13.1              3.4           50.4
      Services   34.8              7.8           0
      ========== ================= ============= ========================

   .. [39]
      We define process heat as the high temperature heat required in the
      industrial processes. This heat cannot be supplied by technologies
      such as heat pumps or thermal solar.

.. _ssec:app1_demand_mobility:

Mobility
--------

The annual passenger transport demand in Belgium for 2035 is expected
to be 194 billions :cite:`EuropeanCommission2016`.
Passenger transport demand is divided between public and private
transport. The lower (:math:`%_{public,min}`) and upper bounds
(:math:`%_{public,max}`) for the use of public transport are 19.9% [40]_ and
50% of the annual passenger transport demand, respectively. The
passenger mobility demand is shared over the day according to
:math:`%_{pass}`. We assume a constant passenger mobility demand for every
day of the year. This latter is represented in Figure
:numref:`Figure %s <fig:TS_mobPass>` (data from Figure 12 of
:cite:`USTransportation`).
The annual freight transport demand in Belgium for 2035 is expected to
be 98e09 tons kilometers :cite:`EuropeanCommission2016`.
The freight can be supplied by trucks, trains or boats. The lower
(:math:`%_{fr,rail,min}`) and upper bounds (:math:`%_{fr,rail,max}`) for the use of
freight trains are 10.9% and 25% of the annual freight transport
demand, respectively. The lower (:math:`%_{fr,boat,min}`) and upper bounds
(:math:`%_{fr,boat,max}`) for the use of freight inland boats are 15.6% and
30% of the annual freight transport demand, respectively. The lower
(:math:`%_{fr,trucks,min}`) and upper bounds (:math:`%_{fr,trucks,max}`) for the use
of freight trucks are 0% and 100% of the annual freight transport
demand, respectively. The bounds and technologies information are
latter summarised in Table
`1.15 <#tbl:freight_vehicles_efficiency>`__.

.. figure:: /images/belgian_data/ts_mob.png
   :alt: Normalised passenger mobility time series over a day. We assume a similar passenger mobility demand over the days of the year.  
   :name: fig:TS_mobPass
   :width: 6cm
   :height: 4cm

   Normalised passenger mobility time series over a day. We assume a
   similar passenger mobility demand over the days of the year.

.. _app:discount_and_interest_rates:

Discount rate and interest rate
-------------------------------

To compute their profitability, companies apply a discount rate to the
investment they make. A discount rate is used for both cost of finance
and for risk perception and opportunity cost. The cost of finance is to
be compared with concepts like ‘hurdle rate’ or ‘rate of return’ usually
calculated in accordance to an annual return on investment. Each
individual investment physically occurring in year k, results in a
stream of payments towards the amortization of this investment spread
over several years in the future. The higher the cost of finance (or
hurdle rate), the higher the annual payments spread over the lifetime of
an investment and thus the higher the total cost. The hurdle rate
affects only the investment costs so the impact is bigger for capital
intensive technologies. We consider differentiated hurdle discount rates
for different groups of energy supply and demand technologies,
representing the different risk perception of industry versus
individuals.

According with :cite:t:`Meinke-Hubeny2017` who based their
work on the JRC EU TIMES model :cite:`simoes2013jrc` in line
with the PRIMES model :cite:`EuropeanCommission2016`, the
discount rate is around 7.5 up to 12% depending on the technologies.
Discount rate cannot be directly converted into interest rate as the
first is fixed by the market and the second is fixed by the central
banks. As the evidence presented in Figure
:numref:`Figure %s <fig:path_be_irate_discountrate>` indicates, while these two
interest rates tend to move together, they also may follow different
paths from time to time.


.. figure:: /images/belgian_data/path_be_i_rate_and_discount_rate.png
   :alt: Comparison of Belgian interest rate and discount rate. The following rate was chosen to represent the discount rate: floating loans rate over a 1M€ (other than bank overdraft) and up to 1 year initial rate fixation.
   :name: fig:path_be_irate_discountrate

   Comparison of Belgian interest rate and discount rate. The following
   rate was chosen to represent the discount rate: floating loans rate
   over a 1M€ (other than bank overdraft) and up to 1 year initial rate
   fixation.

For the different studies, the real discount rate for the public
investor :math:`i_{rate}` is fixed to 1.5%, which is similar to the floating
loan rate over a million euros (other than bank overdraft) and greater
than the central bank interest rate.

.. _app:BESTD_data_technologies:

Technologies
============

The technologies are regrouped by their main output types.

Electricity production
----------------------

The following technologies are regrouped into two categories depending
on the resources used: renewable or not.

.. _ssec:app1_renewables:

Renewables
~~~~~~~~~~

.. container::

   .. table:: Renewable electricity production technologies, in 2035. Abbreviations: onshore (on.), offshore (off.).
      :name: tbl:renew_elec

      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      |             | :math:`c_   | :math:`c_   | :math:`gwp_ | :math:`li   | :math:`c_   | :math:`f_   | :math:`f_|
      |             | {inv}`      | {maint}`    | {constr}`   | fetime`     | {p}`        | {min}`      | {max}`   |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      |             | [€          | [€          | [kgCO       | [y]         | [%]         | [GW]        |[GW]      |
      |             | :sub:`2015` | :sub:`2015` | :sub:`2-eq.`|             |             |             |          |
      |             | /kW         | /kW         | /kW         |             |             |             |          |
      |             | :sub:`e`]   | :sub:`e`/y] | :sub:`e`]   |             |             |             |          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      |    Solar    |    870      |    18.8     |    2081     |    25 [57]_ |    11.9     |    0        |    59.2  |
      |    PV       |    [57]_    |    [57]_    |    :cite:`\ |    :cite:`\ |    [58]_    |             |    [59]_ |
      |             |             |             |    weidema_\|    eur\     |             |             |          |
      |             |             |             |    ecoinven\|    opean\   |             |             |          |
      |             |             |             |    t_2013`  |    _phot\   |             |             |          |
      |             |             |             |             |    ovolt\   |             |             |          |
      |             |             |             |             |    aic_t\   |             |             |          |
      |             |             |             |             |    echno\   |             |             |          |
      |             |             |             |             |    logy_\   |             |             |          |
      |             |             |             |             |    platf\   |             |             |          |
      |             |             |             |             |    orm_s\   |             |             |          |
      |             |             |             |             |    trate\   |             |             |          |
      |             |             |             |             |    gic_2\   |             |             |          |
      |             |             |             |             |    011`     |             |             |          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      |    On.      |    1040     |    12.1     |    622.9    |    30 [60]_ |    24.3     |    0        |    10    |
      |    Wind     |    [60]_    |    [60]_    |    :cite:`\ |    :cite:`\ |    [58]_    |             |    [61]_ |
      |    Turbine  |             |             |    weidema_\|    a\       |             |             |          |
      |             |             |             |    ecoinven\|    ssoci\   |             |             |          |
      |             |             |             |    t_2013`  |    ation\   |             |             |          |
      |             |             |             |             |    _des_\   |             |             |          |
      |             |             |             |             |    entre\   |             |             |          |
      |             |             |             |             |    prise\   |             |             |          |
      |             |             |             |             |    s_ele\   |             |             |          |
      |             |             |             |             |    ctriq\   |             |             |          |
      |             |             |             |             |    ues_s\   |             |             |          |
      |             |             |             |             |    uisse\   |             |             |          |
      |             |             |             |             |    s_aes\   |             |             |          |
      |             |             |             |             |    _ener\   |             |             |          |
      |             |             |             |             |    gie_2\   |             |             |          |
      |             |             |             |             |    013`     |             |             |          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      |    Off.     |    4975     |    34.6     |    622.9    |    30 [60]_ |    41.2     |    0        |    6     |
      |    Wind     |    [60]_    |    [60]_    |    :cite:`\ |    :cite:`\ |    [58]_    |             |    [61]_ |
      |    Turbine  |             |             |    weidema_\|    a\       |             |             |          |
      |             |             |             |    ecoinven\|    ssoci\   |             |             |          |
      |             |             |             |    t_2013`  |    ation\   |             |             |          |
      |             |             |             |             |    _des_\   |             |             |          |
      |             |             |             |             |    entre\   |             |             |          |
      |             |             |             |             |    prise\   |             |             |          |
      |             |             |             |             |    s_ele\   |             |             |          |
      |             |             |             |             |    ctriq\   |             |             |          |
      |             |             |             |             |    ues_s\   |             |             |          |
      |             |             |             |             |    uisse\   |             |             |          |
      |             |             |             |             |    s_aes\   |             |             |          |
      |             |             |             |             |    _ener\   |             |             |          |
      |             |             |             |             |    gie_2\   |             |             |          |
      |             |             |             |             |    013`     |             |             |          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      |    Hydro    |    5045     |    50.44    |    1263     |    40       |    48.4     |    0.38     | 0.38     |
      |    River    |    :cite:`\ |    :cite:`\ |    :cite:`\ |    :cite:`\ |             |    :cite:`\ | :cite:`\ |
      |             |    assoc\   |    assoc\   |    weid\    |    assoc\   |             |    swis\    | swis\    |
      |             |    iatio\   |    iatio\   |    ema_e\   |    iatio\   |             |    s_fed\   | s_fed\   |
      |             |    n_des\   |    n_des\   |    coinv\   |    n_des\   |             |    eral_of\ | eral_of\ |
      |             |    _entr\   |    _entr\   |    ent_2\   |    _entr\   |             |    fic\     | fic\     |
      |             |    epris\   |    epris\   |    013`     |    epris\   |             |    e_of_en\ | e_of_en\ |
      |             |    es_el\   |    es_el\   |             |    es_el\   |             |    erg\     | erg\     |
      |             |    ectri\   |    ectri\   |             |    ectri\   |             |    y_sfo\   | y_sfo\   |
      |             |    ques_\   |    ques_\   |             |    ques_\   |             |    e_sta\   | e_sta\   |
      |             |    suiss\   |    suiss\   |             |    suiss\   |             |    tisti\   | tisti\   |
      |             |    es_ae\   |    es_ae\   |             |    es_ae\   |             |    que_2\   | que_2\   |
      |             |    s_gra\   |    s_gra\   |             |    s_gra\   |             |    013`     | 013`     |
      |             |    nde_2\   |    nde_2\   |             |    nde_2\   |             |             |          |
      |             |    014`     |    014`     |             |    014`     |             |             |          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+
      | Geothermal  |    7488     |    142      |    24.9     |    30       |    86       |    0        |    0     |
      | [63]_       |    [63]_    |    [63]_    |    :cite:`\ |             |    :cite:`\ |             |    [64]_ |
      |             |             |             |    weid\    |             |    assoc\   |             |          |
      |             |             |             |    ema_e\   |             |    iatio\   |             |          |
      |             |             |             |    coinv\   |             |    n_des\   |             |          |
      |             |             |             |    ent_2\   |             |    _entr\   |             |          |
      |             |             |             |    013`     |             |    epris\   |             |          |
      |             |             |             |             |             |    es_el\   |             |          |
      |             |             |             |             |             |    ectri\   |             |          |
      |             |             |             |             |             |    ques_\   |             |          |
      |             |             |             |             |             |    suiss\   |             |          |
      |             |             |             |             |             |    es_ae\   |             |          |
      |             |             |             |             |             |    s_ele\   |             |          |
      |             |             |             |             |             |    ctric\   |             |          |
      |             |             |             |             |             |    ite_2\   |             |          |
      |             |             |             |             |             |    012`     |             |          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+----------+

.. [57]
   Investment cost based on
   :cite:`DanishEnergyAgency2019`. OM cost scaled
   proportionally based on IEA data.

.. [58]
   Based on the real data of 2015 (data
   provided by ELIA, the Belgian TSO, which monitored 2952MW of PV,
   onshore and offshore in 2015 (Source: \url{https://www.elia.be/}, consulted the 06/12/2019.})).

.. [59]
   Assuming that 250 km\ \ :math:`^2` of available roof well oriented
   exist today :cite:`Devogelaer2013` and that the
   efficiency in 2035 will be 23%
   :cite:`DanishEnergyAgency2019` with an average
   irradiation - similar to historical values - of 2820
   Wh/m\ \ :math:`^2` in Belgium,
   :cite:`IRM_Atlas_Irradiation`. The upper limit becomes
   59.2 GW of installed capacity.

.. [60]
   Onshore and offshore wind turbines in 2030
   :cite:`DanishEnergyAgency2019`. 
   For Offshore, a correction factor of
   2.58 is applied to have an LCOE of 79€/MWh in 2020, in line with
   recently published offer:
   https://www.enerdata.net/publications/daily-energy-news/belgium-agrees-79mwh-lcoe-three-offshore-wind-parks.html,
   visited on the 12-06-2020.

.. [61]
   From previous study
   :cite:`limpens2018electricity` 
   with a correction on Offshore wind. The government announced a plan to build 6 GW of offshore wind, see `Belgian offshore plateform <https://www.belgianoffshoreplatform.be/fr/>`_.
   

.. [64]
   A prototype (Balmatt project) started in 2019 and produces 4-5
   MW :cite:`VITO_Website`. However, the potential is not
   accurately known.


.. [63]
   ORC cycle at 6 km depth for electricity
   production. Based on Table 17 of :cite:`Carlsson2014`. We
   took the reference case in 2030.



Data for the considered renewable electricity production technologies
are listed in :numref:`Table %s <tbl:renew_elec>`, including
the yearly capacity factor (:math:`c_p`). As described in the Section
`[ssec:lp_formulation] <#ssec:lp_formulation>`__, for seasonal
renewables the capacity factor :math:`c_{p,t}` is defined for each
time period. These capacity factors are represented in Figure
:numref:`Figure %s <fig:TS_Renewables>`. For these technologies,
:math:`c_p` is the average of :math:`c_{p,t}`. For all the other
electricity supply technologies (renewable and non-renewable),
:math:`c_{p,t}` is equal to the default value of 1. As the power
delivered by the hydro river is almost negligible, we take the time
series of hydro river from Switzerland
:cite:`Limpens2019`.
 

.. figure:: /images/belgian_data/c_p_t_renewables.png
   :alt: Capacity factor for the different renewable energy sources over the year.
   :name: fig:TS_Renewables

   Capacity factor for the different renewable energy sources over the year.



.. _ssec:app1_non-renewable:

Non-renewable
~~~~~~~~~~~~~

Data for the considered fossil electricity production technologies are
listed in :numref:`Table %s <tbl:nonrenew_elec>`. The
maximum installed capacity (:math:`f_{max}`) is set to a value high enough
(100 000 TW\ :sub:`e`) for each technology to potentially cover the
entire demand.


.. container::

   .. table:: Non-renewable electricity supply technologies, in 2035. Abbreviations: Combined Cycles Gas Turbine (CCGT), Ultra-Supecritical (U-S), Integrated Gasification Combined Cycles (IGCC).
      :name: tbl:nonrenew_elec

      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`gwp_ | :math:`li   | :math:`c_   | :math:`\eta | :math:`C    |
      |             | {inv}`      | {maint}`    | {constr}`   | fetime`     | {p}`        | _e`         | O_{2,       |
      |             |             |             |             |             |             |             | direct}`    |
      |             |             |             |             |             |             |             | [81]_       |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€          | [€          | [kgCO       | [y]         | [%]         | [%]         | [tCO2/      |
      |             | :sub:`2015` | :sub:`2015` | :sub:`2-eq.`|             |             |             | MWh         |
      |             | /kW         | /kW         | /kW         |             |             |             | :sub:`e`    |
      |             | :sub:`e`]   | :sub:`e`/y] | :sub:`e`]   |             |             |             | ] [81]_     |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Nuclear     | 4846 [82]_  | 103         | 707.9       | 60          | 84.9        | 37          | 0           |
      |             |             | :cite:`\    | \           | :cite:`\    | [83]_       |             |             |
      |             |             | i\          | :cite:`\    | as\         |             |             |             |
      |             |             | ea_-_\      | weid\       | socia\      |             |             |             |
      |             |             | inter\      | ema_e\      | tion_\      |             |             |             |
      |             |             | natio\      | coinv\      | des_e\      |             |             |             |
      |             |             | nal_e\      | ent_2\      | nterp\      |             |             |             |
      |             |             | nergy\      | 013`\       | rises\      |             |             |             |
      |             |             | _agen\      |             | _elec\      |             |             |             |
      |             |             | cy_ie\      |             | triqu\      |             |             |             |
      |             |             | a_201\      |             | es_su\      |             |             |             |
      |             |             | 4-1`\       |             | isses\      |             |             |             |
      |             |             |             |             | _ener\      |             |             |             |
      |             |             |             |             | gie_2\      |             |             |             |
      |             |             |             |             | 014`        |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | CCGT        | 772         | 20          | 183.8       | 25          | 85.0        | 63 [84]_    | 0.317       |
      |             | :cite:`\    | :cite:`\    | \           | :cite:`\    |             |             |             |
      |             | i\          | i\          | :cite:`\    | b\          |             |             |             |
      |             | ea_-_\      | ea_-_\      | weid\       | auer_\      |             |             |             |
      |             | inter\      | inter\      | ema_e\      | new_2\      |             |             |             |
      |             | natio\      | natio\      | coinv\      | 008`        |             |             |             |
      |             | nal_e\      | nal_e\      | ent_2\      |             |             |             |             |
      |             | nergy\      | nergy\      | 013`\       |             |             |             |             |
      |             | _agen\      | _agen\      |             |             |             |             |             |
      |             | cy_ie\      | cy_ie\      |             |             |             |             |             |
      |             | a_201\      | a_201\      |             |             |             |             |             |
      |             | 4-1`        | 4-1`        |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | CCGT\       | 772         | 20          | 183.8       | 25          | 85.0        | 50          | 0           |
      | :sub:`AMMO\ |             |             | :cite:`\    |             |             |             |             |
      | NIA` [89]_  |             |             | weid\       |             |             |             |             |
      |             |             |             | ema_e\      |             |             |             |             |
      |             |             |             | coinv\      |             |             |             |             |
      |             |             |             | ent_2\      |             |             |             |             |
      |             |             |             | 013`\       |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Coal        | 2517        | 30          | 331.6       | 35          | 86.8        | 49          | 0.735       |
      |             | [85]_       | [85]_       | :cite:`\    | \           | \           | [86]_       |             |
      |             |             |             | weid\       | :cite:`\    | :cite:`\    |             |             |
      |             |             |             | ema_e\      | b\          | b\          |             |             |
      |             |             |             | coinv\      | auer_\      | auer_\      |             |             |
      |             |             |             | ent_2\      | new_2\      | new_2\      |             |             |
      |             |             |             | 013`\       | 008`        | 008`        |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | IGCC        | 3246        | 49          | 331.6       | 35          | 85.6        | 54          | 0.667       |
      |             | [87]_       | [87]_       | :cite:`\    | \           | \           | [88]_       |             |
      |             |             |             | weid\       | :cite:`\    | :cite:`\    |             |             |
      |             |             |             | ema_e\      | b\          | b\          |             |             |
      |             |             |             | coinv\      | auer_\      | auer_\      |             |             |
      |             |             |             | ent_2\      | new_2\      | new_2\      |             |             |
      |             |             |             | 013`\       | 008`        | 008`        |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+

.. [81]
   Direct emissions due to combustion. Expressed
   in ton CO2 per MWh of electricity produced. Emissions computed based
   on resource used and specific emissions given in :numref:`Table %s <tbl:prices_resources>`.

.. [82]
   Investment cost: 3431 €\ \ :sub:`2015`/kW\ \ :math:`_{\text{e}}`
   :cite:`iea_-_international_energy_agency_iea_2014-1` +
   dismantling cost in Switzerland: 1415
   €\ \ :sub:`2015`/kW\ \ :math:`_{\text{e}}`
   :cite:`swissnuclear_financement_????`.

.. [83]
   Data for the year 2012
   :cite:`swiss_federal_office_of_energy_sfoe_swiss_2014`

.. [84]
   0.4-0.5 GW\ \ :math:`_{e}` CCGT in 2035 (realistic optimistic
   scenario) :cite:`bauer_new_2008`.

.. [85]
   1.3 GW\ \ :math:`_{e}` advanced pulverized coal power
   plant
   :cite:`u.s._eia_-_energy_information_administration_updated_2013`.
   *c\ maint* is fixed cost (29.2 €\ \ :sub:`2015`/kW\ \ :sub:`e`/y) +
   variable cost (0.51 €\ \ :sub:`2015`/kW\ \ :sub:`e`/y assuming 7600
   h/y).

.. [86]
   Pulverized coal in 2025 (realistic optimistic scenario)
   :cite:`bauer_new_2008`.

.. [87]
   1.2 GW\ \ :math:`_{\text{e}}` IGCC power plant
   :cite:`u.s._eia_-_energy_information_administration_updated_2013`.
   *c\ maint* is fixed cost (48.1 €\ \ :sub:`2015`/kW\ \ :sub:`e`/y) +
   variable cost (0.82 €\ \ :sub:`2015`/kW\ \ :sub:`e`/y assuming 7500
   h/y).

.. [88]
   IGCC in 2025 (realistic optimistic scenario)
   :cite:`bauer_new_2008`.

.. [89]
   Use of Ammonia in CCGT is at its early stage. Mitsubishi is developping 
   a 40 MW turbine and promises similar efficiency as gas CCGT :cite:`nose2021development`. 
   However, the high emissions of NOx requires a removal equipment which will reduce the 
   power plant efficiency. As gas and ammonia CCGT will be similar, we expect a similar cost and lifetime. 
   The only exception is the efficiency, which is assumed at 50% instead of 63% for a gas CCGT :cite:`ikaheimo2018power`.



Heating and cogeneration
------------------------

Tables :numref:`%s <tbl:ind_cogen_boiler>`,
:numref:`%s <tbl:dhn_cogen_boiler>` and
:numref:`%s <tbl:dec_cogen_boiler>` detail the data for
the considered industrial, centralized and decentralised CHP
technologies, respectively. In some cases, it is assumed that
industrial (:numref:`Table %s <tbl:ind_cogen_boiler>`)
and centralized (:numref:` Table %s <tbl:dhn_cogen_boiler>`) technologies are
the same.
:math:`f_{min}` and :math:`f_{max}` for
heating and CHP technologies are 0 and 100 TW\ :sub:`th`,
respectively. The latter value is high enough for each technology to
supply the entire heat demand in its layer. the maximum
(:math:`f_{max,\%}`) and minimum
(:math:`f_{min,\%}`) shares are imposed to 0 and 100%
respectively, i.e. they are not constraining the model.


.. container::

   .. table:: Industrial heating and cogeneration technologies, in 2035. Abbreviations: Combined Heat and Power (CHP), electricity (Elec.), Natural Gas (NG).
      :name: tbl:ind_cogen_boiler
   
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      |              | :math:`c_    | :math:`c_    | :math:`gwp_  | :math:`li    | :math:`c_    | :math:`\eta  | :math:`\eta  | :math:`C     |
      |              | {inv}`       | {maint}`     | {constr}`    | fetime`      | {p}`         | _e`          | _{th}`       | O_{2,        |
      |              |              |              |              |              |              |              |              | direct}`     |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      |              | [€           | [€           | [kgCO        | [y]          | [%]          | [%]          | [%]          | [tCO2/       |
      |              | :sub:`2015`  | :sub:`2015`  | :sub:`2-eq.` |              |              |              |              | MWh          |
      |              | /kW          | /kW          | /kW          |              |              |              |              | :sub:`th`    |
      |              | :sub:`th`]   | :sub:`th`/y] | :sub:`th`]   |              |              |              |              | ] [115]_     |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | CHP NG       | 1408         | 92.6         | 1024         | 20           | 85           | 44           | 46           | 0.435        |
      |              | [116]_       | [117]_       | \            | \            |              | [118]_       | [118]_       |              |
      |              |              |              | :cite:`\     | :cite:`\     |              |              |              |              |
      |              |              |              | weidem\      | baue\        |              |              |              |              |
      |              |              |              | a_ecoi\      | r_new_\      |              |              |              |              |
      |              |              |              | nvent_2013`  | 2008`        |              |              |              |              |
      |              |              |              |              |              |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | CHP          | 1080         | 40.5         | 165.3        | 25           | 85           | 18           | 53           | 0.735        |
      | Wood         | \            | \            | \            | \            |              | \            | \            |              |
      | [119]_       | \            | \            | \            | \            |              | \            | \            |              |
      |              | :cite:`\     | :cite:`\     | :cite:`\     | :cite:`\     |              | :cite:`\     | :cite:`\     |              |
      |              | iea_\        | iea_\        | weidem\      | ove\         |              | iea_\        | iea_\        |              |
      |              | -_inte\      | -_inte\      | a_ecoi\      | _arup_\      |              | -_inte\      | -_inte\      |              |
      |              | rnatio\      | rnatio\      | nvent_2013`  | and_pa\      |              | rnatio\      | rnatio\      |              |
      |              | nal_en\      | nal_en\      |              | rtners\      |              | nal_en\      | nal_en\      |              |
      |              | ergy_a\      | ergy_a\      |              | _ltd_r\      |              | ergy_a\      | ergy_a\      |              |
      |              | gency_\      | gency_\      |              | eview_\      |              | gency_\      | gency_\      |              |
      |              | iea_20\      | iea_20\      |              | 2011`        |              | iea_20\      | iea_20\      |              |
      |              | 14-1`        | 14-1`        |              |              |              | 14-1`        | 14-1`        |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | CHP          | 2928         | 111.3        | 647.8        | 25           | 85           | 20           | 45           | 0.578        |
      | Waste        | [120]_       | [120]_       | [121]_       | \            |              | \            | \            |              |
      |              |              |              |              | :cite:`\     |              | :cite:`\     | :cite:`\     |              |
      |              |              |              |              | ove\         |              | ove\         | ove\         |              |
      |              |              |              |              | _arup_\      |              | _arup_\      | _arup_\      |              |
      |              |              |              |              | and_pa\      |              | and_pa\      | and_pa\      |              |
      |              |              |              |              | rtners\      |              | rtners\      | rtners\      |              |
      |              |              |              |              | _ltd_r\      |              | _ltd_r\      | _ltd_r\      |              |
      |              |              |              |              | eview_\      |              | eview_\      | eview_\      |              |
      |              |              |              |              | 2011`        |              | 2011`        | 2011`        |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | Boiler       | 58.9         | 1.2          | 12.3         | 17           | 95           | 0            | 92.7         | 0.216        |
      | NG           | :cite:`\     | :cite:`\     | [122]_       | \            |              |              | \            |              |
      |              | \            | \            |              | \            |              |              | :cite:`\     |              |
      |              | Mo\          | Mo\          |              | :cite:`\     |              |              | Mo\          |              |
      |              | ret201\      | ret201\      |              | eur\         |              |              | ret201\      |              |
      |              | 7PhDTh\      | 7PhDTh\      |              | opean_\      |              |              | 7PhDTh\      |              |
      |              | esis`        | esis`        |              | commis\      |              |              | esis`        |              |
      |              |              |              |              | sion_e\      |              |              |              |              |
      |              |              |              |              | nergy_\      |              |              |              |              |
      |              |              |              |              | 2008`        |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | Boiler       | 115          | 2.3          | 28.9         | 17           | 90           | 0            | 86.4         | 0.451        |
      | Wood         | \            | \            | \            | \            |              |              | \            |              |
      |              | :cite:`\     | :cite:`\     | \            | \            |              |              | :cite:`\     |              |
      |              | Mo\          | Mo\          | :cite:`\     | :cite:`\     |              |              | Mo\          |              |
      |              | ret201\      | ret201\      | weidem\      | eur\         |              |              | ret201\      |              |
      |              | 7PhDTh\      | 7PhDTh\      | a_ecoi\      | opean_\      |              |              | 7PhDTh\      |              |
      |              | esis`        | esis`        | nvent_2013`  | commis\      |              |              | esis`        |              |
      |              |              |              |              | sion_e\      |              |              |              |              |
      |              |              |              |              | nergy_\      |              |              |              |              |
      |              |              |              |              | 2008`        |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | Boiler       | 54.9         | 1.2          | 12.3         | 17           | 95           | 0            | 87.3         | 0.309        |
      | Oil          | [123]_       | [124]_       | \            | \            |              |              | \            |              |
      |              |              |              | \            | \            |              |              | :cite:`\     |              |
      |              |              |              | :cite:`\     | :cite:`\     |              |              | Mo\          |              |
      |              |              |              | weidem\      | eur\         |              |              | ret201\      |              |
      |              |              |              | a_ecoi\      | opean_\      |              |              | 7PhDTh\      |              |
      |              |              |              | nvent_2013`  | commis\      |              |              | esis`        |              |
      |              |              |              |              | sion_e\      |              |              |              |              |
      |              |              |              |              | nergy_\      |              |              |              |              |
      |              |              |              |              | 2008`        |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | Boiler       | 115          | 2.3          | 48.2         | 17           | 90           | 0            | 82           | 0.439        |
      | Coal         | [125]_       | [125]_       | \            | \            |              |              |              |              |
      |              |              |              | \            | \            |              |              |              |              |
      |              |              |              | :cite:`\     | :cite:`\     |              |              |              |              |
      |              |              |              | weidem\      | eur\         |              |              |              |              |
      |              |              |              | a_ecoi\      | opean_\      |              |              |              |              |
      |              |              |              | nvent_2013`  | commis\      |              |              |              |              |
      |              |              |              |              | sion_e\      |              |              |              |              |
      |              |              |              |              | nergy_\      |              |              |              |              |
      |              |              |              |              | 2008`        |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | Boiler       | 115          | 2.3          | 28.9         | 17           | 90           | 0            | 82           | 0.317        |
      | Waste        | [125]_       | [125]_       | [126]_       | \            |              |              |              |              |
      |              |              |              |              | \            |              |              |              |              |
      |              |              |              |              | :cite:`\     |              |              |              |              |
      |              |              |              |              | eur\         |              |              |              |              |
      |              |              |              |              | opean_\      |              |              |              |              |
      |              |              |              |              | commis\      |              |              |              |              |
      |              |              |              |              | sion_e\      |              |              |              |              |
      |              |              |              |              | nergy_\      |              |              |              |              |
      |              |              |              |              | 2008`        |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+
      | Direct       | 332          | 1.5          | 1.47         | 15           | 95           | 0            | 100          | 0            |
      | Elec.        | [127]_       | [127]_       | \            |              |              |              |              |              |
      |              |              |              | \            |              |              |              |              |              |
      |              |              |              | :cite:`\     |              |              |              |              |              |
      |              |              |              | weidem\      |              |              |              |              |              |
      |              |              |              | a_ecoi\      |              |              |              |              |              |
      |              |              |              | nvent_2013`  |              |              |              |              |              |
      +--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+--------------+


.. [115]
   Direct emissions due to combustion. Expressed
   in ton CO2 per MWh of heat produced. Emissions computed based on
   resource used and specific emissions given in :numref:`Table %s <tbl:prices_resources>`.

.. [116]
   Calculated as the average of investment costs for 50 kW\ \ :sub:`e`
   and 100 kW\ \ :sub:`e` internal combustion engine cogeneration
   systems :cite:`prognos_ag_energieperspektiven_2012`.

.. [117]
   Calculated as the average of investment costs for 50 kW\ \ :sub:`e`
   and 100 kW\ \ :sub:`e` internal combustion engine cogeneration
   systems :cite:`rits_energieperspektiven_2007`.

.. [118]
   200 kW\ \ :sub:`e` internal combustion engine cogeneration
   NG system, very optimistic scenario in 2035
   :cite:`bauer_new_2008`.

.. [119]
   Biomass cogeneration plant (medium size) in 2030-2035.

.. [120]
   Biomass-waste-incineration CHP, 450 scenario in 2035
   :cite:`iea_-_international_energy_agency_iea_2014-1`.

.. [121]
   Impact of MSW incinerator in :cite:`Moret2017PhDThesis`,
   using efficiencies reported in the table.

.. [122]
   Assuming same impact as industrial oil boiler.

.. [123]
   925 kW\ \ :sub:`th` oil boiler (GTU 530)
   :cite:`walter_meier_ag_listes_2011`

.. [124]
   Assumed to be equivalent to a NG boiler.

.. [125]
   Assumed to be equivalent to a wood boiler.

.. [126]
   Assuming same impact as industrial wood boiler.

.. [127]
   Commercial/public small direct electric heating
   :cite:`nera_economic_consulting_uk_2009`.


.. container::

   .. table:: District heating technologies, in 2035. Abbreviations: biomass (bio.), CHP, digestion (dig.), hydrolysis (hydro.).
      :name: tbl:dhn_cogen_boiler


      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      |            | :math:`c_  | :math:`c_  | :math:`gwp_| :math:`li  | :math:`c_  | :math:`\eta| :math:`\eta| :math:`C   |
      |            | {inv}`     | {maint}`   | {constr}`  | fetime`    | {p}`       | _e`        | _{th}`     | O_{2,      |
      |            |            |            |            |            |            |            |            | direct}`   |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      |            | [€         | [€         | [kgCO      | [y]        | [%]        | [%]        | [%]        | [tCO2/     |
      |            | :sub:`2015`| :sub:`2015`| :sub:`2    |            |            |            |            | MWh        |
      |            | /kW        | /kW        | -eq.`/kW   |            |            |            |            | :sub:`th`  |
      |            | :sub:`th`] | :sub:`th`  | :sub:`th`] |            |            |            |            | ] [154]_   |
      |            |            | /y]        |            |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | HP         | 345        | 12.0       | 174.8      | 25         | 95         | 0          | 400        | 0          |
      |            | [155]_     | [156]_     | \          |            |            |            |            |            |
      |            |            |            | :cite:`\   |            |            |            |            |            |
      |            |            |            | wei\       |            |            |            |            |            |
      |            |            |            | dema_ec\   |            |            |            |            |            |
      |            |            |            | oinvent\   |            |            |            |            |            |
      |            |            |            | _2013`     |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP NG     | 1254       | 37.5       | 490.9      | 25         | 85         | 50         | 40         | 0.500      |
      |            | [157]_     | [157]_     | [158]_     | \          |            | [159]_     | [159]_     |            |
      |            |            |            |            | :cite:`\   |            |            |            |            |
      |            |            |            |            | ba\        |            |            |            |            |
      |            |            |            |            | uer_new\   |            |            |            |            |
      |            |            |            |            | _2008`     |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP        | 1081       | 40.5       | 165.3      | 25         | 85         | 18         | 53         | 0.736      |
      | Wood [160]_| :cite:`\   |            |            | :cite:`\   |            | :cite:`\   | :cite:`\   |            |
      |            | iea_\      |            |            | ove_\      |            | iea_\      | iea_\      |            |
      |            | -_inter\   |            |            | arup_an\   |            | -_inter\   | -_inter\   |            |
      |            | nationa\   |            |            | d_partn\   |            | nationa\   | nationa\   |            |
      |            | l_energ\   |            |            | ers_ltd\   |            | l_energ\   | l_energ\   |            |
      |            | y_agenc\   |            |            | _review\   |            | y_agenc\   | y_agenc\   |            |
      |            | y_iea_2\   |            |            | _2011`     |            | y_iea_2\   | y_iea_2\   |            |
      |            | 014-1`     |            |            |            |            | 014-1`     | 014-1`     |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP        | 2928       | 111        | 647.8      | 25         | 85         | 20         | 45         | 0.578      |
      | Waste      |            |            |            | :cite:`\   |            | :cite:`\   | :cite:`\   |            |
      | [160]_     |            |            |            | ove_\      |            | ove_\      | ove_\      |            |
      |            |            |            |            | arup_an\   |            | arup_an\   | arup_an\   |            |
      |            |            |            |            | d_partn\   |            | d_partn\   | d_partn\   |            |
      |            |            |            |            | ers_ltd\   |            | ers_ltd\   | ers_ltd\   |            |
      |            |            |            |            | _review\   |            | _review\   | _review\   |            |
      |            |            |            |            | _2011`     |            | _2011`     | _2011`     |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP        | 1374       | 147.9      | 647.8      | 25         | 85         | 13         | 16         | 2.488      |
      | bio.       | [161]_     | [161]_     | [162]_     |            | [161]_     | [161]_     | [161]_     |            |
      | dig.       |            |            |            |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP        | 4537       | 227        | 647.8      | 15         | 85         | 25.4       | 33.5       | 1.164      |
      | bio.       | [163]_     |            | [162]_     |            |            |            |            |            |
      | hydro.     |            |            |            |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | Boiler     | 58.9       | 1.2        | 12.3       | 17         | 95         | 0          | 92.7       | 0.216      |
      | NG         | :cite:`\   |            |            | :cite:`\   |            |            | :cite:`\   |            |
      |            | Moret2\    |            |            | \          |            |            | Moret2\    |            |
      |            | 017PhDT\   |            |            | europ\     |            |            | 017PhDT\   |            |
      |            | hesis`     |            |            | ean_com\   |            |            | hesis`     |            |
      |            |            |            |            | mission\   |            |            |            |            |
      |            |            |            |            | _energy\   |            |            |            |            |
      |            |            |            |            | _2008`     |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | Boiler     | 115        | 2.3        | 28.9       | 17         | 90         | 0          | 86.4       | 0.451      |
      | Wood       | :cite:`\   | :cite:`\   |            | :cite:`\   |            |            | :cite:`\   |            |
      |            | Moret2\    | Moret2\    |            | \          |            |            | Moret2\    |            |
      |            | 017PhDT\   | 017PhDT\   |            | europ\     |            |            | 017PhDT\   |            |
      |            | hesis`     | hesis`     |            | ean_com\   |            |            | hesis`     |            |
      |            |            |            |            | mission\   |            |            |            |            |
      |            |            |            |            | _energy\   |            |            |            |            |
      |            |            |            |            | _2008`     |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | Boiler     | 54.9       | 1.2        | 12.3       | 17         | 95         | 0          | 87.3       | 0.309      |
      | Oil        |            |            |            | :cite:`\   |            |            | :cite:`\   |            |
      |            |            |            |            | \          |            |            | Moret2\    |            |
      |            |            |            |            | europ\     |            |            | 017PhDT\   |            |
      |            |            |            |            | ean_com\   |            |            | hesis`     |            |
      |            |            |            |            | mission\   |            |            |            |            |
      |            |            |            |            | _energy\   |            |            |            |            |
      |            |            |            |            | _2008`     |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | Geo        | 1500       | 57.0       | 808.8      | 30         | 85         | 0          | 100        | 0          |
      | thermal    | [165]_     | [165]_     | \          | [165]_     |            |            |            |            |
      | [165]_     |            |            | :cite:`\   |            |            |            |            |            |
      |            |            |            | wei\       |            |            |            |            |            |
      |            |            |            | dema_ec\   |            |            |            |            |            |
      |            |            |            | oinvent\   |            |            |            |            |            |
      |            |            |            | _2013`     |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+
      | Solar      | 362        | 0.43       | 221.8      | 30         | 10         | 0          | 100        | 0          |
      | thermal    | [166]_     | [166]_     | \          | [166]_     |            |            |            |            |
      | [166]_     |            |            | :cite:`\   |            |            |            |            |            |
      |            |            |            | wei\       |            |            |            |            |            |
      |            |            |            | dema_ec\   |            |            |            |            |            |
      |            |            |            | oinvent\   |            |            |            |            |            |
      |            |            |            | _2013`     |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+------------+


.. [154]
   Direct emissions due to combustion. Expressed
   in ton CO2 per MWh of heat produced. Emissions computed based on
   resource used and specific emissions given in :numref:` Table %s <tbl:prices_resources>`.

.. [155]
   Calculated with the equation: *c\ inv* [EUR\ \ :sub:`2011`] =
   :math:`3737.6 * E^{0.9}`, where :math:`E` is the electric power
   (kW\ \ :sub:`e`) of the compressor, assumed to be 2150
   kW\ \ :sub:`e`. Equation from
   :cite:`becker_methodology_2012`, taking only the cost of
   the technology (without installation factor).

.. [156]
   Ground-water heat pump with 25 years lifetime
   :cite:`iea_-_international_energy_agency_renewables_2007`.

.. [157]
   CCGT with cogeneration
   :cite:`iea_-_international_energy_agency_iea_2014-1`.

.. [158]
   Impact of NG CHP in from :cite:`Moret2017PhDThesis`,
   using efficiencies reported in the table.

.. [159]
   :math:`\eta`\ \ \ :sub:`e` and :math:`\eta`\ \ \ :sub:`th`
   at thermal peak load of a 200-250 MW\ \ :sub:`e` CCGT plant,
   realistic optimistic scenario in
   2035 :cite:`bauer_new_2008`.

.. [160]
   Assumed same technology as for industrial heat and CHP
   (:numref:`Table %s <tbl:ind_cogen_boiler>`)

.. [161]
   Cost estimations from
   :cite:`ro2007catalytic` and efficiencies from
   :cite:`poschl2010evaluation`. Data in line with IEA:
   :cite:`ETSAP2010_BiomassForHeatAndPower`

.. [162]
   Construction emissions is assimilated to an industrial CHP waste
   technology.

.. [163]
   Own calculation

.. [165]
   Geothermal heat-only plant with steam driven
   absorption heat pump 70/17\ \ :math:`^o`\ \ C at 2.3 km depth (from
   :cite:`DanishEnergyAgency2019`).

.. [166]
   Total system excluding thermal storage (from
   :cite:`DanishEnergyAgency2019`).



.. container::

   .. table:: Decentralised heating and cogeneration technologies, in 2035. Abbreviations: Combined Heat and Power (CHP), electricity (Elec.), Fuel Cell (FC), Heat Pump (HP), Natural Gas (NG) and thermal (th.).
      :name: tbl:dec_cogen_boiler


      +------------+------------+------------+------------+------------+------------+------------+------------+
      |            | :math:`c_  | :math:`c_  | :math:`gwp_| :math:`li  | :math:`c_  | :math:`\eta| :math:`\eta|
      |            | {inv}`     | {maint}`   | {constr}`  | fetime`    | {p}`       | _e`        | _{th}`     |
      |            |            |            |            |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      |            | [€         | [€         | [kgCO      | [y]        | [%]        | [%]        | [%]        |
      |            | :sub:`2015`| :sub:`2015`| :sub:`2    |            |            |            |            |
      |            | /kW        | /kW        | -eq.`/kW   |            |            |            |            |
      |            | :sub:`e`]  | :sub:`e`/y]| :sub:`e`]  |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | HP         | 492        | 21 [209]_  | 164.9      | 18         | 100        | 0          | 300        |
      |            | [207]_     |            | \          | [209]_     |            |            |            |
      |            | [208]_     |            | \          |            |            |            |            |
      |            |            |            | \          |            |            |            |            |
      |            |            |            | :cite:`\   |            |            |            |            |
      |            |            |            | weid\      |            |            |            |            |
      |            |            |            | ema_e\     |            |            |            |            |
      |            |            |            | coinv\     |            |            |            |            |
      |            |            |            | ent_2\     |            |            |            |            |
      |            |            |            | 013`       |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | Thermal    | 316 [210]_ | 9.5 [211]_ | 381.9      | 20         | 100        | 0          | 150        |
      | HP         | [208]_     |            | \          |            |            |            |            |
      |            |            |            | \          |            |            |            |            |
      |            |            |            | \          |            |            |            |            |
      |            |            |            | :cite:`\   |            |            |            |            |
      |            |            |            | weid\      |            |            |            |            |
      |            |            |            | ema_e\     |            |            |            |            |
      |            |            |            | coinv\     |            |            |            |            |
      |            |            |            | ent_2\     |            |            |            |            |
      |            |            |            | 013`       |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP        | 1408       | 92.6       | 1024       | 20         | 100        | 44         | 46         |
      | NG [212]_  |            |            |            | \          |            |            |            |
      |            |            |            |            | :cite:`\   |            |            |            |
      |            |            |            |            | b\         |            |            |            |
      |            |            |            |            | auer_\     |            |            |            |
      |            |            |            |            | new_2\     |            |            |            |
      |            |            |            |            | 008`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | CHP        | 1          | 82.0       | 1          | 20         | 100        | 39 [215]_  | 43 [215]_  |
      | Oil        | 306 [213]_ | [213]_     | 024 [214]_ |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | FC NG      | 7 242      | 144.8      | 2193       | 20         | 100        | 58 [218]_  | 22 [218]_  |
      |            | [216]_     | [217]_     | \          | \          |            |            |            |
      |            |            |            | \          | \          |            |            |            |
      |            |            |            | \          | \          |            |            |            |
      |            |            |            | :cite:`\   | :cite:`\   |            |            |            |
      |            |            |            | weid\      | gerbo\     |            |            |            |
      |            |            |            | ema_e\     | ni_fi\     |            |            |            |
      |            |            |            | coinv\     | nal_2\     |            |            |            |
      |            |            |            | ent_2\     | 008`\      |            |            |            |
      |            |            |            | 013`       |            |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | FC H\      | 7242       | 144.8      | 2193       | 20         | 100        | 58         | 22         |
      | :sub:`2`   |            |            |            | \          |            |            |            |
      | [219]_     |            |            |            | \          |            |            |            |
      |            |            |            |            | \          |            |            |            |
      |            |            |            |            | :cite:`\   |            |            |            |
      |            |            |            |            | gerbo\     |            |            |            |
      |            |            |            |            | ni_fi\     |            |            |            |
      |            |            |            |            | nal_2\     |            |            |            |
      |            |            |            |            | 008`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | Boiler     | 159        | 5.08       | 4.8        | 17         | 100        | 0          | 90         |
      | NG         | \          | \          | \          | \          |            |            | \          |
      |            | \          | \          | \          | \          |            |            | \          |
      |            | \          | \          | \          | \          |            |            | :cite:`\   |
      |            | :cite:`\   | :cite:`\   | :cite:`\   | :cite:`\   |            |            | Moret\     |
      |            | Moret\     | Moret\     | Moret\     | eur\       |            |            | 2017P\     |
      |            | 2017P\     | 2017P\     | 2017P\     | opean\     |            |            | hDThe\     |
      |            | hDThe\     | hDThe\     | hDThe\     | _comm\     |            |            | sis`       |
      |            | sis`       | sis`       | sis`       | issio\     |            |            |            |
      |            |            |            |            | n_ene\     |            |            |            |
      |            |            |            |            | rgy_2\     |            |            |            |
      |            |            |            |            | 008`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | Boiler     | 462        | 16         | 2          | 17         | 100        | 0          | 85         |
      | Wood       | \          | \          | 1.1 [220]_ | \          |            |            | \          |
      |            | \          | \          |            | \          |            |            | \          |
      |            | \          | \          |            | \          |            |            | \          |
      |            | :cite:`\   | :cite:`\   |            | :cite:`\   |            |            | :cite:`\   |
      |            | pant\      | pant\      |            | eur\       |            |            | pant\      |
      |            | aleo_in\   | aleo_in\   |            | opean\     |            |            | aleo_in\   |
      |            | teg\       | teg\       |            | _comm\     |            |            | teg\       |
      |            | ratio\     | ratio\     |            | issio\     |            |            | ratio\     |
      |            | n_201\     | n_201\     |            | n_ene\     |            |            | n_201\     |
      |            | 4-1`       | 4-1`       |            | rgy_2\     |            |            | 4-1`       |
      |            |            |            |            | 008`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | Boiler     | 142        | 8.5 [221]_ | 21.1\      | 17         | 100        | 0          | 85         |
      | Oil        | \          |            | \          | \          |            |            | \          |
      |            | \          |            | \          | \          |            |            | \          |
      |            | \          |            | \          | \          |            |            | :cite:`\   |
      |            | :cite:`\   |            | :cite:`\   | :cite:`\   |            |            | Moret\     |
      |            | walt\      |            | Moret\     | eur\       |            |            | 2017P\     |
      |            | er_me\     |            | 2017P\     | opean\     |            |            | hDThe\     |
      |            | ier_a\     |            | hDThe\     | _comm\     |            |            | sis`       |
      |            | g_lis\     |            | sis`       | issio\     |            |            |            |
      |            | tes_2\     |            |            | n_ene\     |            |            |            |
      |            | 011`       |            |            | rgy_2\     |            |            |            |
      |            |            |            |            | 008`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | Solar      | 719 [222]_ | 8.1 [223]_ | 221.2      | 20         | 11.3\      | 0          | NA         |
      | Th.        |            |            | \          | \          | [224]_     |            |            |
      |            |            |            | \          | \          |            |            |            |
      |            |            |            | \          | \          |            |            |            |
      |            |            |            | :cite:`\   | :cite:`\   |            |            |            |
      |            |            |            | weid\      | nera\      |            |            |            |
      |            |            |            | ema_e\     | _econ\     |            |            |            |
      |            |            |            | coinv\     | omic_co\   |            |            |            |
      |            |            |            | ent_2\     | nsu\       |            |            |            |
      |            |            |            | 013`       | lting\     |            |            |            |
      |            |            |            |            | _uk_2\     |            |            |            |
      |            |            |            |            | 009`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+
      | Direct     | 40 [225]_  | 0          | 1.47       | 15         | 100        | 0          | 100        |
      | Elec.      |            | .18 [226]_ | \          | \          |            |            |            |
      |            |            |            | \          | \          |            |            |            |
      |            |            |            | \          | \          |            |            |            |
      |            |            |            | :cite:`\   | :cite:`\   |            |            |            |
      |            |            |            | weid\      | nera\      |            |            |            |
      |            |            |            | ema_e\     | _econ\     |            |            |            |
      |            |            |            | coinv\     | omic_co\   |            |            |            |
      |            |            |            | ent_2\     | nsu\       |            |            |            |
      |            |            |            | 013`       | lting\     |            |            |            |
      |            |            |            |            | _uk_2\     |            |            |            |
      |            |            |            |            | 009`       |            |            |            |
      +------------+------------+------------+------------+------------+------------+------------+------------+

.. [207]
   10.9 kW\ \ :sub:`th` Belaria compact IR heat pump
   :cite:`hoval_sa_catalogue_2016`.

.. [208]
   Catalog data divided by 2.89. 2.89 is the ratio between
   Swiss catalog prices and prices found in the literature. Calculated
   by dividing the average price of a decentralised NG boiler (489
   CHF\ \ :sub:`2015`/kW\ \ :sub:`th`) in Swiss catalogs
   :cite:`viessman_viessman_2016` by the price for the
   equivalent technology found in literature (169
   CHF\ \ :sub:`2015`/kW\ \ :sub:`th`, from
   :cite:`Moret2017PhDThesis`).

.. [209]
   6 kW\ \ :sub:`th` air-water heat pump
   :cite:`nera_economic_consulting_uk_2009`.

.. [210]
   Specific investment cost for a 15.1 kW\ \ :sub:`th` absorption heat
   pump (Vitosorp 200-F) :cite:`viessman_viessman_2016`

.. [211]
   3% of *c\ inv* (assumption).

.. [212]
   Assumed same technology as for industrial CHP NG
   (:numref:`Table %s <tbl:ind_cogen_boiler>`)

.. [213]
   Assumed to be equivalent to a 100 kW\ \ :sub:`e`
   internal combustion engine cogeneration NG system
   :cite:`rits_energieperspektiven_2007,prognos_ag_energieperspektiven_2012`.

.. [214]
   Assuming same impact as decentralised NG CHP.

.. [215]
   Efficiency data for a 200 kW\ \ :sub:`e` diesel
   engine :cite:`weidema_ecoinvent_2013`

.. [216]
   System cost (including markup) for a 5 kW\ \ :sub:`e` solid-oxide FC
   system, assuming an annual production of 50000 units
   :cite:`battelle_manufacturing_2014`.

.. [217]
   2% of the investment
   cost :cite:`iea_-_international_energy_agency_iea_2014-1`.

.. [218]
   Solid-oxide FC coupled with a NG turbine, values for very
   optimistic scenario in 2025 :cite:`gerboni_final_2008`.

.. [219]
   Assumed to be equivalent to FC NG.

.. [220]
   Assuming same impact as NG and oil decentralised boilers.

.. [221]
   6% of *c\ inv*, based on ratio between investment and OM cost of
   boiler of similar size
   in :cite:`european_commission_energy_2008`.

.. [222]
   504 CHF\ \ :sub:`2015`/m\ \ :math:`^2` for the UltraSol Vertical 1V
   Hoval system :cite:`hoval_sa_catalogue_2016`. For
   conversion from €\ \ :sub:`2015`/m\ \ :math:`^2` to
   €\ \ :sub:`2015`/kW\ \ :sub:`th`, it is assumed an annual heat
   capacity factor of 6.5% based on Uccles data.

.. [223]
   1.1% of the investment cost, based on ratio investment-to-OM cost
   in :cite:`nera_economic_consulting_uk_2009`.

.. [224]
   The calculation of the capacity factor for solar thermal is based on
   the IRM model :cite:`IRM_Atlas_Irradiation` with
   radiation data from the city of Uccles, Belgium.

.. [225]
   Resistance heaters with fan assisted air circulation
   in :cite:`european_commission_energy_2008`.

.. [226]
   In the lack of specific data, same investment-to-OM ratio as for
   direct electric heating in the industry sector
   (:numref:`Table %s <tbl:ind_cogen_boiler>`).


:numref:`Figure %s <fig:TS_solar_th>` represents the capacity factor
(:math:`c_{p,t}`) of solar thermal panels. The time series is the
direct irradiation in Uccles in 2015, based on measurements of IRM.
For all the other heat supply technologies (renewable and
non-renewable) :math:`c_{p,t}` is equal to the default value of 1.

.. figure:: /images/belgian_data/TS_solar_th.png
   :alt: Capacity factor of thermal solar panels over the year.
   :name: fig:TS_solar_th

   Capacity factor of thermal solar panels over the year.

.. _sec:app1_vehicles_mobility:

Transport
---------

Passenger mobility
~~~~~~~~~~~~~~~~~~

The vehicles available for passenger mobility are regrouped in two
categories: public and private. Private accounts for all the cars owned
(or rented) by the user, such as a gasoline car, a diesel car... In
opposition to private, public mobility accounts for the shared vehicles.
It accounts for buses, coaches, trains, trams, metro and trolleys. From
the literature, data about mobility is not directly transposable to the
model. Data about mobility are usually given per vehicles, such as a
vehicle cost or an average occupancy per vehicle. These data are
summarised in :numref:`Table %s <tbl:mob_specific_costs_calculation>`.



.. container::

   .. table:: Specific investment cost calculation based on vehicle investment data, in 2035. Abbreviations: average (av.), Fuel Cell (FC), Hybrid Electric Vehicle (HEV), Natural Gas (NG), Plug-in Hybrid Electric Vehicle (PHEV), public (pub.).
      :name: tbl:mob_specific_costs_calculation

      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | **Vehicle | :math:`Ve | :math:`Ma | :math:`Oc | :math:`Av.| :math:`Av.| :math:`li | :math:`gw |
      | type**    | h.~Cost`  | intenance`| cupancy`  | ~distance`| ~speed`   | fetime`   | p_{       |
      |           |           | [241]_    |           |           |           | [242]_    | constr}`  |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      |           |           | [k€\      | [k€\      | [         | [1000     | [         | [         |
      |           |           | :math:`_\ | :math:`_\ | pass/     | km/y]     | km/h]     | years]    |
      |           |           | 2015`     | 2015`     | veh.]     |           |           |           |
      |           |           | /veh.]    | /veh./y]  |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Gasoline  | 21 [243]_ | 1.2       | 1.26      | 18 [245]_ | 40        | 10        | 17.2      |
      | car       |           |           | [244]_    |           |           |           |           |
      |           |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Diesel    | 22 [243]_ | 1.2       | 1.26      | 18 [245]_ | 40        | 10        | 17.4      |
      | car       |           |           | [244]_    |           |           |           |           |
      |           |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | NG        | 22 [243]_ | 1.2       | 1.26      | 18 [245]_ | 40        | 10        | 17.2      |
      | car       |           |           | [244]_    |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | HEV       | 22 [243]_ | 1.74      | 1.26      | 18 [245]_ | 40        | 10        | 26.2      |
      | car       |           |           | [244]_    |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | PHEV      | 23 [243]_ | 1.82      | 1.26      | 18 [245]_ | 40        | 10        | 26.2      |
      | car       |           |           | [244]_    |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | BEV       | 23 [243]_ | 0.5       | 1.26      | 18 [245]_ | 40        | 10        | 19.4      |
      | [246]_    |           |           | [244]_    |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | FC        | 22 [243]_ | 0.5       | 1.26      | 18 [245]_ | 40        | 10        | 39.6      |
      | car       |           |           | [244]_    |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Tram      | 2500      | 50.0      | 200       | 60        | 20        | 30        | 0         |
      | and       |           |           |           |           |           |           | [247]_    |
      | metro     |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Diesel    | 220       | 11.0      | 24        | 39        | 15        | 15        | 0 [247]_  |
      | bus       |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Diesel    | 300       | 12.0      | 24        | 39        | 15        | 15        | 0 [247]_  |
      | HEV       |           |           |           |           |           |           |           |
      | bus       |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | NG        | 220       | 11.0      | 24        | 39        | 15        | 15        | 0 [247]_  |
      | bus       |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | FC        | 375       | 11.3      | 24        | 39        | 15        | 15        | 0 [247]_  |
      | bus       |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Train     | 10000     | 200.0     | 80        | 200       | 83        | 40        | 0 [247]_  |
      | pub.      |           |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+


.. [241]
   own calculation. The maintenance cost
   was assumed proportional to the investment cost and depending the
   type of powertrain. the average speed of private cars is calculated
   assuming that it is used 5% of the time (i.e. 1h12). Knowing the
   annual distance, the value is approximately 40 km/h.

.. [242]
   In 2016, the average age of private cars was 8.9 years with a
   difference between regions :cite:`kwanten2016kilometres`.

.. [243]
   Costs are from mid-range vehicles estimation
   and projections of :cite:`national2013transitions`.

.. [244]
   The federal bureau office estimates
   a decreasing average occupancy for cars down to 1.26
   passenger/vehicle in 2030
   :cite:`BureaufederalduPlan2012`).

.. [245]
   In 2016, averaged yearly distance for
   private cars were between 9 500 and 21 100 kms depending on the type
   of powertrains, but in average around 18 000 kms.

.. [246]
   Low range BEV have been implemented. Otherwise the investment cost is
   more than twice.

.. [247]
   No data found.



In Belgium, the car occupancy rate is less than 1.3 passengers per car:
1.3 in 2015 and estimated at 1.26 in
:cite:`BureaufederalduPlan2012`. The annual distance of a
car depends on its type of motorization: from 9 500 km/year for a city
gasoline car, to 21 100 km/year for a CNG one. On average, the distance
is 18 000 km/year. The average age of a car is 8.9 years in 2016, with a
variation between regions: in Brussels it is 10 years. On average, the
distance is 18 000 km/year. The average age of a car is 8.9 years in
2016, with a rather strong variation between regions: in Brussels it is
10 years. Finally, a car drives on average a slightly more than one hour
a day (1h12). Although private car usage habits may change, we
extrapolate these data from today to future years. Certain trends, such
as the mutualisation of a car, could lead to an increase in the annual
distance travelled by a car. But other trends, such as autonomous cars,
could lead to a further decrease in the car occupancy rate, to values
below 1. These change may influence in both direction the specific price
of a kilometer passenger provided by a car.

For public transportation, the data were collected from various report
:cite:`taszka2018analyse,moawad2013light,james2012mass`.
These data have been adapted based on discussion with experts in the
field. They are reported in :numref:`Table %s <tbl:mob_specific_costs_calculation>`.

Surprisingly, in 2035, vehicles cost are similar regardless the
power-train.  :numref:`Figure %s <fig:car_cost_over_transition>` shows how
the vehicle cost vary over the transition, data from
:cite:`national2013transitions`. Today, we verify a strong
price difference between the different technologies, this difference
will diminish with the development of new technologies. The price
difference between two technologies will become small as early as 2035
(:math:`\leq`\ 10%). In their work,
:cite:t:`national2013transitions` estimates the cost of
promising technologies in 2015 lower than the real market price. This is
the case for BEV and FC vehicles, where the price ranges today around
60 k€\ :sub:`2015` . These differences can be justified by three facts:
these vehicles are usually more luxurious than others; The selling price
do not represent the manufacturing cost for prototypes; the study is
from 2013 and may have overestimated the production in 2015 and 2020.


.. figure:: /images/belgian_data/app_bestd_car_cost_transition.png
   :alt: Mid-range vehicle costs evolution during the transition. Reference (**1.0 (ref)**) is at 19.7 k€\ :sub:`2015`. Abbreviations: Carbon capture (CC), LFO, methanation (methan.), methanolation (methanol.), Natural Gas (NG), Synthetic Natural Gas (SNG), storage (sto.) and synthetic (syn.).
   :name: fig:car_cost_over_transition
   :width: 14cm

   Mid-range vehicle costs evolution during the transition. Reference
   (**1.0 (ref)**) is at 19.7 k€\ :sub:`2015`. Abbreviations: Carbon
   capture (CC), LFO, methanation (methan.), methanolation (methanol.),
   Natural Gas (NG), Synthetic Natural Gas (SNG), storage (sto.) and synthetic (syn.).

.. math::
   c_{inv} (i) = \frac{vehicle~cost (i)}{occupancy (i)\cdot average~speed (i)} ~~~~~~ \forall i \in \text{TECH OF EUT} (PassMob)
   :label: eq:c_inv_for_mob_pass_calculation
    
.. math::
   c_p = \frac{average~distance(i)}{average~speed(i)\cdot 8760} ~~~~~~ \forall i \in \text{TECH OF EUT} (PassMob)
   :label: eq:c_p_for_mob_pass_calculation
    
.. math::
   veh._{capa} (i) = occupancy (i)\cdot average~speed ~~~~~~ \forall i \in \text{TECH OF EUT} (PassMob)
   :label: eq:veh_capa_for_mob


From data of :numref:`Table %s <tbl:mob_specific_costs_calculation>`,
specific parameters for the model are deduced. The specific investment
cost (:math:`c_{inv}`) is calculated from the vehicle cost, its average speed
and occupancy, Eq. :eq:`eq:c_inv_for_mob_pass_calculation`.
The capacity factor (*c\ p*) is calculated based on the ratio between
yearly distance and average speed, Eq. :eq:`eq:c_p_for_mob_pass_calculation`.
The vehicle capacity is calculated based on the average occupancy and
average speed, Eq. . :eq:`eq:veh_capa_for_mob`.
:numref:`Table %s <tbl:mob_costs>` summarises these information
for each passenger vehicle.

An additional vehicle is proposed: methanol car. 
This choice is motivated to offer a zero emission fuels that could be competitve compared to electric or hydrogen vehicles.
We assume that methanol is used through a spark-ignition engine in cars, 
and has similar performances than a gasoline car. 
This technology is added in the following tables.


.. container::

   .. table:: Passenger mobility financial information, in 2035 (based on data in :numref:`Table %s <tbl:mob_specific_costs_calculation>`). Abbreviations: Fuel Cell (FC), Hybrid Electric Vehicle (HEV), Natural Gas (NG), Plug-in Hybrid Electric Vehicle (PHEV), public (pub.).
      :name: tbl:mob_costs

      +----------+----------+----------+----------+----------+----------+
      | **Vehicle| :math:`c_| :math:`c_| :math:`g | :math:`c_| :math:`V |
      | type**   | {inv}`   | {maint}` | wp_{     | p`       | eh.~capa`|
      |          |          |          | constr}` |          |          |
      +----------+----------+----------+----------+----------+----------+
      | [€/km    | [€/km    | [€/km    | [kgCO\   | [%]      | [pass-km |
      | -pass]   | -pass/h] | -pass    | :sub:`2` |          | /h/veh.] |
      |          |          | /h/y]    | -eq./km  |          |          |
      |          |          |          | -pass/h] |          |          |
      +----------+----------+----------+----------+----------+----------+
      | Gasoline | 420      | 24       | 342      | 5.1      | 50       |
      | car      |          |          |          |          |          |
      +----------+----------+----------+----------+----------+----------+
      | Diesel   | 434      | 24       | 346      | 5.1      | 50       |
      | car      |          |          |          |          |          |
      +----------+----------+----------+----------+----------+----------+
      | NG car   | 429      | 24       | 342      | 5.1      | 50       |
      +----------+----------+----------+----------+----------+----------+
      | HEV car  | 429      | 34       | 519      | 5.1      | 50       |
      +----------+----------+----------+----------+----------+----------+
      | PHEV car | 456      | 34       | 519      | 5.1      | 50       |
      +----------+----------+----------+----------+----------+----------+
      | BEV      | 450      | 10       | 385      | 5.1      | 50       |
      +----------+----------+----------+----------+----------+----------+
      | FC car   | 435      | 10       | 786      | 5.1      | 50       |
      +----------+----------+----------+----------+----------+----------+
      | Methanol | 420      | 24       | 342      | 5.1      | 50       |
      | car      |          |          |          |          |          |
      | [259]_   |          |          |          |          |          |
      +----------+----------+----------+----------+----------+----------+
      | Tram and | 625      | 12.5     | 0        | 34.2     | 4000     |
      | metro    |          |          | [250]_   |          |          |
      +----------+----------+----------+----------+----------+----------+
      | Diesel   | 611      | 30.6     | 0        | 29.7     | 360      |
      | bus      |          |          | [250]_   |          |          |
      +----------+----------+----------+----------+----------+----------+
      | Diesel   | 833      | 33.3     | 0        | 29.7     | 360      |
      | HEV bus  |          |          | [250]_   |          |          |
      +----------+----------+----------+----------+----------+----------+
      | NG bus   | 611      | 30.6     | 0 [250]_ | 29.7     | 360      |
      +----------+----------+----------+----------+----------+----------+
      | FC bus   | 1042     | 31.3     | 0 [250]_ | 29.7     | 360      |
      +----------+----------+----------+----------+----------+----------+
      | Train    | 1506     | 54.4     | 0 [250]_ | 27.5     | 6640     |
      | pub.     |          |          |          |          |          |
      +----------+----------+----------+----------+----------+----------+

.. [250]
   No data found

.. [259]
   No data were found for methanol cars. Thus, we assume that the 
   technology is similar to a gasoline car (except the fuel).


:numref:`Table %s <tbl:passenger_vehicles>` summarises
the forecast energy efficiencies for the different vehicles. For public
vehicles in 2035, the energy efficiencies are calculated with a linear
interpolation between the 2010 and 2050 values presented in Table 6 in
Codina Gironès et al :cite:`codina_girones_strategic_2015`.
For private vehicles, Estimation for energy consumption for Belgium cars
in 2030 are used :cite:`BureaufederalduPlan2012`.


.. container::

   .. table:: Fuel and electricity consumption for passenger mobility technologies in 2035 :cite:`codina_girones_strategic_2015`, and minimum/maximum shares allowed in the model. Abbreviations: Fuel Cell (FC), Hybrid Electric Vehicle (HEV), Natural Gas (NG), Plug-in Hybrid Electric Vehicle (PHEV), public (pub.).
      :name: tbl:passenger_vehicles

      ================ ============ =============== ============================ ============================
      **Vehicle type** **Fuel**     **Electricity** **f**:math:`_\textbf{min,%}` **f**:math:`_\textbf{max,%}`
      \                [Wh/km-pass] [Wh/km-pass]    [Wh/km-pass]                 [%]
      Gasoline car     497  [251]_  0               0                            1
      Diesel car       435  [251]_  0               0                            1
      NG car           543  [251]_  0               0                            1
      HEV [252]_       336  [251]_  0               0                            1
      PHEV [253]_      138  [251]_  109 [251]_      0                            1
      BEV              0            173 [251]_      0                            1
      FC car           264  [254]_  0               0                            1
      Methanol car     497  [251]_  0               0                            1
      Tram & Trolley   0            63  [255]_      0                            0.17  [256]_
      Diesel bus       265          0               0                            1
      Diesel HEV bus   198          0               0                            1
      NG bus           268          0               0                            1
      FC bus           225          0               0                            1
      Train pub.       0            65 [255]_       0                            0.60 [256]_
      ================ ============ =============== ============================ ============================

.. [251]
   calculation based on vehicle consumption in
   2030 :cite:`BureaufederalduPlan2012` and occupancy of
   2030 :cite:`BureaufederalduPlan2012`. According to
   :cite:`codina_girones_strategic_2015`, gas car are
   assumed to consume 25% more than diesel cars.

.. [252]
   Using gasoline as only fuel.

.. [253]
   It is assumed that electricity is used to cover 40% of the total
   distance and petrol to cover the remaining 60%.

.. [254]
   In FC car are estimated to consume 52.6%
   more than BEV in 2035, see Table 2.12 in
   :cite:`national2013transitions`

.. [255]
   Based on real data for the French case
   in 2004, from :cite:`enerdata2004efficacite`. An increase
   of efficiency of 25% was assume.

.. [256]
   In 2015, the public mobility was shared as follow:
   trains (37.0%), trams/metros (8.7%) and buses (54.3%)
   :cite:`Eurostat2017`. In 2035, we assume an upper limit
   twice greater than real data in 2015. Except for train were a maximum
   of 60% is imposed.


The size of the BEV batteries is assumed to be the one from a Nissan
Leaf (ZE0) (24 kWh [257]_). The size of the PHEV batteries is assumed to
be the one from Prius III Plug-in Hybrid (4.4 kWh [258]_). The
performances of BEV and PHEV batteries are assimilated to a Li-ion
battery as presented in :numref:`Table %s <tab:StoDataAdvanced>`. 
The state of charge of the electric vehicles (:math:`soc_{ev}`) is constrained to 60% minimum at 7 am every days.



Freight mobility
~~~~~~~~~~~~~~~~

The technologies available for freight transport are trains, trucks and
boats. Similarly to previous section, the information for the freight is
given per vehicles. These data are summarised in :numref:`Table %s <tbl:mob_specific_costs_calculation_freight>`.

.. container::

   .. table:: Specific investment cost for freight vehicles, in 2035. Trucks data are from a report of 2019 :cite:`Karlstrom_fuetruck_2019`. Abbreviations: electric (elec.), Fuel Cell (FC) and Natural Gas (NG).
      :name: tbl:mob_specific_costs_calculation_freight
   
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | **Vehicle | :math:`Ve | :math:`Ma | :math:`To | :math:`Av.| :math:`Av.| :math:`li |
      | type**    | h.~Cost`  | intenance`| nnage`    | ~distance`| ~speed`   | fetime`   |
      |           |           | [263]_    |           |           | [263]_    |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      |           |           | [k€\      | [k€\      | [         | [1000     | [         |
      |           |           | :math:`_  | :math:`_  | pass/     | km/y]     | km/h]     |
      |           |           | {2015}`   | {2015}`   | veh.]     |           |           |
      |           |           | /veh.]    | /veh./y]  |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Train     | 4020      | 80.4      | 550       | 210       | 70        | 40        |
      | freight   |           |           |           |           |           |           |
      | [263]_    |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Boat      | 2750      | 137.5     | 1200      | 30        | 30        | 40        |
      | Diesel    |           |           |           |           |           |           |
      | [263]_    |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Boat NG   | 2750      | 137.5     | 1200      | 30        | 30        | 40        |
      | [263]_    |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Boat      | 2750      | 137.5     | 1200      | 30        | 30        | 40        |
      | Methanol  |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Truck     | 167       | 8.4       | 10        | 36.5      | 45        | 15        |
      | Diesel    |           |           |           | [264]_    |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Truck     | 181       | 5.4       | 10        | 36.5      | 45        | 15        |
      | FC        |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Truck     | 347       | 10.4      | 10        | 36.5      | 45        | 15        |
      | Elec.     |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+
      | Truck     | 167       | 8.4       | 10        | 36.5      | 45        | 15        |
      | NG        |           |           |           |           |           |           |
      +-----------+-----------+-----------+-----------+-----------+-----------+-----------+

.. [263]
   Own calculation

.. [264]
   In 2016, the average distance was between 16 974 up to 63 305 km per
   year depending on the truck category. Based on our own calculation,
   we found an average of 36 500 km per year.



Trucks have similar cost except for electric trucks. This last have a
battery that supplies the same amount of kilometers than other
technologies. As a consequence, half of the truck cost is related to the
battery pack.

.. math::
   c_{inv} (i) = \frac{vehicle~cost (i)}{tonnage (i)\cdot average~speed (i)} ~~~~~~ \forall i \in \text{TECH OF EUT} (FreightMob)
   :label: eq:c_inv_for_mob_calculation_fr
    
.. math::
   c_p = \frac{average~distance(i)}{average~speed(i)\cdot 8760} ~~~~~~ \forall i \in \text{TECH OF EUT} (FreightMob)
   :label: eq:c_p_for_mob_calculation_fr
    
.. math::
   veh._{capa} (i) = tonnage (i)\cdot average~speed ~~~~~~ \forall i \in \text{TECH OF EUT} (FreightMob)
   :label: eq:veh_capa_for_mob_fr


From :numref:`Table %s <tbl:mob_specific_costs_calculation_freight>`,
specific parameters for the model are deduced. Except for the technology
construction specific GHG emissions (:math:`gwp_{constr}`) where no data was
found. The specific investment cost (*c\ inv*) is calculated from the
vehicle cost, its average speed and occupancy, Eq.
:eq:`eq:c_inv_for_mob_calculation_fr`.
The capacity factor (*c\ p*) is calculated based on the ratio between
yearly distance and average speed, Eq.
:eq:`eq:c_p_for_mob_calculation_fr`. The
vehicle capacity is calculated based on the average occupancy and
average speed, Eq.
Eq. :eq:`eq:veh_capa_for_mob_fr`. :numref:`Table %s <tbl:mob_costs_fr>` summarises these information for each
freight vehicle.

Similarly to the methanol car, additional power trains have been added in order to open the competition between fuels and electric vehicles (including fuel cells electri vehicles). 
Methanol could be use with performances similar to the use of methane. 
Based on this approach, two technologies have been added: methanol boats and methanol trucks.

.. container::

   .. table:: Freight mobility financial information, in 2035. Abbreviations: electric (elec.), Fuel Cell (FC) and Natural Gas (NG).
      :name: tbl:mob_costs_fr
   
      +-------------+------------+-------------+-------------+-------------+
      | **Vehicle   | :math:`c_  | :math:`c_   | :math:`c_   | :math:`V    |
      | type**      | {inv}`     | {maint}`    | p`          | eh.~capa`   |
      |             |            |             |             |             |
      +-------------+------------+-------------+-------------+-------------+
      |             | [€/km-t/h] |[€/km-t/h/y] | [%]         | [t-km/h     |
      |             |            |             |             | /veh.]      |
      |             |            |             |             |             |
      |             |            |             |             |             |
      +-------------+------------+-------------+-------------+-------------+
      | Train       | 104        | 2.1         | 34.2        | 38500       |
      | freight     |            |             |             |             |
      +-------------+------------+-------------+-------------+-------------+
      | Boat Diesel | 76         | 3.8         | 11.4        | 36000       |
      +-------------+------------+-------------+-------------+-------------+
      | Boat NG     | 76         | 3.8         | 11.4        | 36000       |
      +-------------+------------+-------------+-------------+-------------+
      | Boat        | 76         | 3.8         | 11.4        | 36000       |
      | Methnanol   |            |             |             |             |
      +-------------+------------+-------------+-------------+-------------+
      | Truck       | 371        | 18.6        | 9.3         | 450         |
      | Diesel      |            |             |             |             |
      +-------------+------------+-------------+-------------+-------------+
      | Truck FC    | 402        | 12.1        | 9.3         | 450         |
      +-------------+------------+-------------+-------------+-------------+
      | Truck Elec. | 771        | 23.1        | 9.3         | 450         |
      +-------------+------------+-------------+-------------+-------------+
      | Truck NG    | 371        | 18.6        | 9.3         | 450         |
      +-------------+------------+-------------+-------------+-------------+
      | Truck       | 371        | 18.6        | 9.3         | 450         |
      | Methanol    |            |             |             |             |
      +-------------+------------+-------------+-------------+-------------+


Trains and boats benefit on a very high tonnage capacity, and thus
drastically reduce their specific investment cost down to 4-5 times
lower than trucks. :numref:`Table %s <tbl:mob_costs_fr>` summarises the
forecast energy efficiencies for the different vehicles in 2035. Except
for the technology construction specific GHG emissions (:math:`gwp_{constr}`)
where no data was found.

.. container::

   .. table:: Fuel and electricity consumption for freight mobility technologies, in 2035 :cite:`codina_girones_strategic_2015`. Abbreviations: electric (elec.), Fuel Cell (FC) and Natural Gas (NG).
      :name: tbl:freight_vehicles_efficiency
   
   

      ================ ========= ===============
      **Vehicle type** **Fuel**  **Electricity**
      \                [Wh/km-t] [Wh/km-t]
      Train freight    0         68
      Boat Diesel      107       0
      Boat NG          123       0
      Boat Diesel      107       0
      Truck Diesel     513       0
      Truck FC         440       0
      Truck Elec.      0         249  [265]_
      Truck NG  [266]_ 590       0
      Truck Diesel     513       0
      ================ ========= ===============

.. [265]
   Energy intensity calculated based on the diesel one, and corrected
   with an electric to diesel powertrain ratio from
   :cite:`Karlstrom_fuetruck_2019`.

.. [266]
   The efficiency is corrected with the ratio between NG bus and diesel
   bus.

Trains are considered to be only electric. Their efficiency in 2035 is
0.068 kWh/tkm :cite:`codina_girones_strategic_2015`. The
efficiency for freight transport by diesel truck is 0.51 kWh/tkm based
on the weighted average of the efficiencies for the vehicle mix
in :cite:`codina_girones_strategic_2015`. For NG and H2
trucks, no exact data were found. Hence, we assume that the efficiency
ratio between NG coaches and diesel coaches can be used for freight
(same for H2 trucks). As a consequence, the efficiency of NG and H2
trucks are 0.59 and 0.44 kWh/tkm. Boats are considered to be diesel or
gas powered. In 2015, the energy intensity ratio between diesel boats
and diesel trucks were :math:`\approx`\ 20% [267]_. By assuming a
similar ratio in 2035, we find an efficiency of 0.107 kWh/tkm and 0.123
kWh/tkm for diesel and gas boats, respectively.



.. _sec:app1_ned:

Non-energy demand
-----------------

Non-energy demand plays a major role in the primary energy consumption in Belgium (20% in 2015, :cite:`EurostatEnergyBalanceSheets2015`). 
:cite:t:`rixhon2021comprehensive` investigates the importance of non-energy demand worlwide and its projection based on the IEA reports (:cite:`iea2018petrochemicals`). 
Three main feedstocks have been chosen : ammonia, methanol and high-value chemicals (HVCs). This latter encompass different molecules, mainly hydrocarbons chains. 
:numref:`Figure %s <fig:ned_prod_pathways>` illustrates the different conversion pathway to produce the different non-energy demand feedstocks.

.. figure:: /images/belgian_data/ned_pathways.png
   :alt: Illustration of the technologies that produce non-energy feedstocks. 
   :name: fig:ned_prod_pathways

   Illustration of the technologies that produce non-energy feedstocks. 
   For clarity, only the most relevant flows are drawn (Figure
   :numref:`Figure %s <fig:bes_illustration>` includes all the flows).
   Ammonia and methanol can be used in other sectors.


The Non-energy end-use demand is usuallty expressed in TWh/y without specifying the split among the feedstocks, 
such as the forecast used which are proposed by the European commission :cite:`EuropeanCommission2016`.  
In :cite:t:`rixhon2021comprehensive`, they analysed the split among the three proposed feedstocks. 
In 2015, 77.9% of the NED accounted was for HVC, 19.2% for ammonia and only 2.9% for Methanol. 
Worlwide, the IEA forecast a similar growth for the different feedstocks (see Figure 4.5 of :cite:`iea2018petrochemicals`). 
Thus, we assume a constant share between the three feedstocks.


Similarly to electricity, two of the three feedstocks can be used for other end-use demands. As an example, ammonia can be used for electricity production or methanol for mobility.
:numref:`Table %s <tab:hvc_prod>` summarises the technology that produces HVC; :numref:`Table %s <tab:methanol_prod>` summarises the technology that produces methanol; 
and for ammonia, only the Haber-Bosch process is proposed in :numref:`Table %s <tab:ammonia_prod>`  

.. container::

   .. table:: Production of High-Value Chemicals (HVCs) from different feedstocks, in 2035. 
      :name: tab:hvc_prod
   
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`life | :math:`c_p` | :math:`\eta_| :math:`\eta_| :math:`\eta_| :math:`CO_  |
      |             | {inv}`      | {maint}`    | time`       |             | {fuel}`     | {e}`        | {th,ht}`    | {2,direct}` |
      |             |             |             |             |             |             |             |             | [359]_      |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :math:`_| [€\ :math:`_| [y]         | [%]         | [MWh/MWh\   | [MWh/MWh\   | [MWh/MWh\   | [tCO\       |
      |             | {2015}`/kW\ | {2015}`/kW\ |             |             | :math:`_    | :math:`_    | :math:`_    | :sub:`2`    |
      |             | :math:`_    | :math:`_    |             |             | {HVC}`]     | {HVC}`]     | {HVC}`]     | /MWh\       |
      |             | {fuel}`]    | {fuel}`/y]  |             |             |             |             |             | :sub:`e`]   |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Oil to HVC  | 395         | 2.1         | 15          | 100         | 1.82        | 0.021       | 0.017       | 0.213       |
      | :cite:`yan\ |             |             |             |             |             |             |             |             |
      | g2017comp\  |             |             |             |             |             |             |             |             |
      | arative,ren\|             |             |             |             |             |             |             |             |
      | 2009petro\  |             |             |             |             |             |             |             |             |
      | chemicals`  |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Gas to HVC  | 798         | 20          | 25          | 100         | 2.79        | 0.47        | 0           | 0.299       |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | cruellas\   |             |             |             |             |             |             |             |             |
      | 2019\       |             |             |             |             |             |             |             |             |
      | techno`     |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Biomass     | 1743        | 52          | 20          | 100         | 2.38        | 0.029       | 0.052       | 0.669       |
      | to HVC      |             |             |             |             |             |             |             |             |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | haro\       |             |             |             |             |             |             |             |             |
      | 2013\       |             |             |             |             |             |             |             |             |
      | techno\     |             |             |             |             |             |             |             |             |
      | economic`   |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Methanol    | 697         | 63          | 20          | 100         | 1.24        | 0           | 0.045       | 0.304       |
      | to HVC      |             |             |             |             |             |             |             |             |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | tsiropoulos\|             |             |             |             |             |             |             |             |
      | 2018\       |             |             |             |             |             |             |             |             |
      | emerging,   |             |             |             |             |             |             |             |             |
      | reyniers\   |             |             |             |             |             |             |             |             |
      | 2017\       |             |             |             |             |             |             |             |             |
      | techno`     |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+




.. container::

   .. table:: Production of methanol from different feedstocks, in 2035.
      :name: tab:methanol_prod
   
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`life | :math:`c_p` | :math:`\eta_| :math:`\eta_| :math:`\eta_| :math:`CO_  |
      |             | {inv}`      | {maint}`    | time`       |             | {fuel}`     | {e}`        | {th}`       | {2,direct}` |
      |             |             |             |             |             |             |             |             | [359]_      |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :math:`_| [€\ :math:`_| [y]         | [%]         | [%]         | [%]         | [%]         | [tCO\       |
      |             | {2015}`/kW\ | {2015}`/kW\ |             |             |             |             |             | :sub:`2`    |
      |             | :math:`_    | :math:`_    |             |             |             |             |             | /MWh\       |
      |             | {fuel}`]    | {fuel}`/y]  |             |             |             |             |             | :sub:`e`]   |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Biomass to  | 2520        | 38.5        | 20          | 85          | 62          | 2           | 22          | 0.236       |
      | methanol    |             |             |             |             |             |             |             |             |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | DanishEnerg\|             |             |             |             |             |             |             |             |
      | yAgency2019\|             |             |             |             |             |             |             |             |
      | a`\         |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Syn.        | 1680        | 84          | 20          | 67          | 0           | 0           | 26.1        | -0.248      |
      | methanolat\ |             |             |             |             |             |             |             |             |
      | ion [361]_  |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Methane     | 958.6       | 47.9        | 20          | 1           | 65.4        | 0           | 0           | 0.306       |
      | to          |             |             |             |             |             |             |             |             |
      | methanol    |             |             |             |             |             |             |             |             |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | col\        |             |             |             |             |             |             |             |             |
      | lodi2\      |             |             |             |             |             |             |             |             |
      | 017de\      |             |             |             |             |             |             |             |             |
      | monst\      |             |             |             |             |             |             |             |             |
      | ratin\      |             |             |             |             |             |             |             |             |
      | g`          |             |             |             |             |             |             |             |             |
      | [362]_      |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+




.. container::

   .. table:: Production of ammonia with the Haber Bosch process, in 2035. Data from :cite:t:`ikaheimo2018power`.
      :name: tab:ammonia_prod
   
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`life | :math:`c_p` | :math:`\eta_| :math:`\eta_| :math:`\eta_| :math:`CO_  |
      |             | {inv}`      | {maint}`    | time`       |             | {fuel}`     | {e}`        | {th}`       | {2,direct}` |
      |             |             |             |             |             |             |             |             | [359]_      |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :math:`_| [€\ :math:`_| [y]         | [%]         | [%]         | [%]         | [%]         | [tCO\       |
      |             | {2015}`/kW\ | {2015}`/kW\ |             |             |             |             |             | :sub:`2`    |
      |             | :math:`_    | :math:`_    |             |             |             |             |             | /MWh\       |
      |             | {fuel}`]    | {fuel}`/y]  |             |             |             |             |             | :sub:`e`]   |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Haber bosch | 847         | 16.6        | 20          | 85          | 79.8        | 0           |10.7         | 0           |
      | [364]_      |             |             |             |             | (NH3)       |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+

.. [364]
   To produce 1 unit of ammonia, the system uses 1.13 units of H2 and 0.123 of electricity.




.. _ssec:app1_syn_fuels:

Synthetic fuels production
--------------------------

Synthetic fuels are expected to play a key role to phase out fossil
fuels :cite:`Rosa2017`. :numref:`Figure %s <fig:CO2andPtGLayers>` 
represents the technology related to
synthetic fuels, including the CO2 layers. Synthetic fuels can be
imported (Bio-ethanol, Bio-Diesel, H2 or SNG) or produced by converting
biomass and/or electricity. The wet biomass - usually organic waste -
can be converted through the *biogas plant* technology to SNG. This
technology combines anaerobic digestion and cleaning processes. Woody
biomass can be used to produce H2 through *gasification*, or different oils through
*pyrolysis* or SNG through *gasification to SNG*. The different oil account for LFO, Gasoline or Diesel. 
The other processes to produce
synthetic fuels are based on the water electrolysis, where the
*electrolysers* convert electricity to H2. Then, the H2 can be combined
with CO2 and upgraded to SNG through the *methanation* technology. In
this latter, the process requires CO2. It can either be captured from
large scale emitters, such as the industries and centralised heat
technologies; or directly captured from the air but at a higher
energetic and financial cost.

.. figure:: /images/belgian_data/PtG_and_CO2_layers.png
   :alt: Illustration of roduce synthetic fuels. For clarity, only the most relevant flows are drawn (:numref:`Figure %s <fig:bes_illustration>` includes all the flows).
   :name: fig:CO2andPtGLayers

   Illustration of the technologies and processes to produce synthetic
   fuels. For clarity, only the most relevant flows are drawn (Figure
   :numref:`Figure %s <fig:bes_illustration>` includes all the flows).
   This Figure also illustrates how Carbon capture is implemented in the model. 
   The CO:sub:`2` emissions of large scale technologies can be either 
   released at the atmosphere or captured by the *Carbon Capture Industrial* 
   technolgy. Otherwise, CO:sub:`2` can be captured from the atmosphere at 
   a greater cost.


Hydrogen production
~~~~~~~~~~~~~~~~~~~

Three technologies are considered for hydrogen production: electrolysis,
NG reforming and biomass gasification. The last two options can include
CCS systems for limiting the CO\ :math:`_2` emissions. They are
Different technologies for electrolysis, in their work the
:cite:t:`DanishEnergyAgency2019a` review the PEM-EC, A-EC and
SO-EC. :numref:`Table %s <tbl:hydrogen_techs_danish>` summarises the key
characteristics for these technologies in year 2035.
   

.. container::

   .. table:: Characteristics of electrolyser technologies presented in :cite:`DanishEnergyAgency2019a`, in 2035. Efficiencies are represent as follow: Input (negative) and outputs (positive). Abbreviations: temperature (temp.), high temperature (h.t.), low temperature (l.t.), electricity (e), hydrogen (H2).
      :name: tbl:hydrogen_techs_danish


      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`life | :math:`\eta_| :math:`\eta_| :math:`\eta_| :math:`\eta_|
      |             | {inv}`      | {maint}`    | time`       | e`          | {h.t.}`     | {H2}`       | {l.t.}`     |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :math:`_| [€\ :math:`_| [y]         | [%]         | [%]         | [%]         | [%]         |
      |             | {2015}`/kW\ | {2015}`/kW\ |             |             |             |             |             |
      |             | :math:`_    | :math:`_    |             |             |             |             |             |
      |             | {H2}`]      | {H2}`/y]    |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | PEM-EC      | 870         | 40          | 15          | -100        |             | 63          | 12          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | A-EC        | 806         | 43          | 25          | -100        |             | 67          | 11          |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | SO-EC       | 696         | 21          | 23          | -85         | -15         | 79          | 1.5         |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+



The different electrolyser cell technologies have a similar cost,
however each technologies differ by their lifetime and electricity to
hydrogen efficiencies. PEM-EC has the shortest lifetime and the lowest
electricity to hydrogen efficiency, thus this technology will never be
implemented in the model [335]_. Electrolysers will be needed during
excesses of electricity production, where heat demand is usually low.
Thus, they aim at maximising the production of hydrogen rather than low
temperature heat. For this reason, SO-EC appear as the most promising
technology SO-EC appears as the most promising technology and will be
implemented in the model. Thus, in this work, the term *Electrolysis*
refers to SO-EC. :numref:`Table %s <tbl:hydrogen>` contains the
data for the hydrogen production technologies.


.. container::

   .. table:: Hydrogen production technologies, in 2035.
      :name: tbl:hydrogen

      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      |               | :math:`c_     | :math:`c_     | :math:`life   | :math:`c_p`   | :math:`\eta_  | :math:`CO_    |
      |               | {inv}`        | {maint}`      | time`         |               | {H2}`         | {2,direct}`   |
      |               |               |               |               |               |               | [346]_        |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      |               | [€\ :math:`_  | [€\ :math:`_  | [y]           | [%]           | [%]           | [tCO\ :sub:`2`|
      |               | {2015}`/kW\   | {2015}`/kW\   |               |               |               | /MWh\         |
      |               | :math:`_      | :math:`_      |               |               |               | :sub:`e`]     |
      |               | {H2}`]        | {H2}`/y]      |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Electrolysis  | 696           | 21            | 23            | 90            | 79            | 0             |
      | [347]_        |               |               |               | [348]_        | [351]_        |               |
      | :cite:`\      |               |               |               |               |               |               |
      | DanishEnerg\  |               |               |               |               |               |               |
      | yAgency\      |               |               |               |               |               |               |
      | 2019a`        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | NG            | 681           | 64.4          | 25            | 86            | 73            | 0.273         |
      | reforming     |               |               |               |               |               |               |
      | [349]_        |               |               |               |               |               |               |
      | :cite:`to\    |               |               |               |               |               |               |
      | ck_ther\      |               |               |               |               |               |               |
      | mo-envi\      |               |               |               |               |               |               |
      | ronomic\      |               |               |               |               |               |               |
      | _2013`        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Biomass       | 2525          | 196           | 25            | 86            | 43            | 0.902         |
      | gasification  |               |               |               |               |               |               |
      | [350]_        |               |               |               |               |               |               |
      | :cite:`to\    |               |               |               |               |               |               |
      | ck_ther\      |               |               |               |               |               |               |
      | mo-envi\      |               |               |               |               |               |               |
      | ronomic\      |               |               |               |               |               |               |
      | _2013`        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Ammonia       | 1365          | 38            | 25            | 85            | 59.1          | 0             |
      | cracking      |               |               |               |               |               |               |
      | [352]_        |               |               |               |               |               |               | 
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+


.. [346]
   Direct emissions due to combustion. Expressed
   in ton CO2 per MWh of fuel produced. Emissions computed based on
   resource used and specific emissions given in :numref:`Table %s <tbl:prices_resources>`.

.. [347]
   It uses electricity and high temperature heat as feedstock, see :numref:`Table %s <tbl:hydrogen_techs_danish>`.

.. [348]
   Own assumptions.

.. [349]
   It uses gas as feedstock, such as NG.

.. [350]
   It uses wood biomass as feedstock.

.. [351]
   To produce one unit of H2, the system requires 1.076 units of electricity and 0.19 units of heat high temperature. 
   We assume that, on top of the unit of H2 produced, an extra 0.019 units of low temperature heat can be recovered 
   for district heating.

.. [352]
   Cracking ammonia doesn't exist at industrial scale. Indeed, ammonia is produced from hydrogen throuth the Haber-Bosch process.
   Thus, we didn't found reliable data and did our own calculation based on Haber bosch process and methane cracking.



Synthetic methane and oils production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Three technology options are considered for the conversion of biomass to
synthetic fuels: pyrolysis, gasification and biomethanation. The main
product of the pyrolysis process is bio-oil. Two different pyrolysis process are thus proposed. 
One producing light fuel oil, and another one producing a blend of gasoline and diesel. 
The main product of the gasification and
biomethanation processes are SNG, which is considered equivalent to
gas. Data for the technologies are reported in :numref:`Table %s <tbl:sng_pyro>` (from
:cite:`Moret2017PhDThesis`). The biomethanation process is
based on anaerobic digestion followed by a cleaning process in order to
have gas that can be reinjected in the gas grid
:cite:`DanishEnergyAgency2019a,Energiforsk2016`. In the
table, efficiencies are calculated with respect to the wood in input
(50% humidity, on a wet basis LHV) and ‘*fuel*’ stands for the main
synthetic fuel in output. 
Finally, a last technology can produce methane from hydrogen and sequestrated CO:sub:`2`.


.. container::

   .. table:: Synthetic fuels (except H2) conversion technologies (from :cite:`DanishEnergyAgency2019a,Moret2017PhDThesis` or specified), in 2035.
      :name: tbl:sng_pyro
   
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`life | :math:`c_p` | :math:`\eta_| :math:`\eta_| :math:`\eta_| :math:`CO_  |
      |             | {inv}`      | {maint}`    | time`       |             | {fuel}`     | {e}`        | {th}`       | {2,direct}` |
      |             |             |             |             |             |             |             |             | [359]_      |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :math:`_| [€\ :math:`_| [y]         | [%]         | [%]         | [%]         | [%]         | [tCO\       |
      |             | {2015}`/kW\ | {2015}`/kW\ |             |             |             |             |             | :sub:`2`    |
      |             | :math:`_    | :math:`_    |             |             |             |             |             | /MWh\       |
      |             | {fuel}`]    | {fuel}`/y]  |             |             |             |             |             | :sub:`e`]   |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Pyrolysis   | 1344        | 67.2        | 25          | 85          | 66.6        | 1.58        | -           | 0.586       |
      | to LFO      |             |             |             |             |             |             |             |             |
      | [363]_      |             |             |             |             |             |             |             |             | 
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Pyrolysis   | 1365        | 38          | 25          | 85          | 57.4        | 1.58        | -           | 0.586       |
      | to fuels    |             |             |             |             |             |             |             |             |
      | [363]_      |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Gasification| 2525        | 178         | 25          | 85          | 65          | 0           | 22          | 0.260       |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Biomethana\ | 986         | 88          | 25          | 85          | 29.9        | 0           | 0           | 0.722       |
      | tion        |             |             |             |             |             |             |             |             |
      | [360]_      |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Hydrolisis  | 1592        | 112         | 15          | 100         | 42.3        | 0           | 4           | 0.306       |
      | methanation |             |             |             |             |             |             |             |             |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | gassn\      |             |             |             |             |             |             |             |             |
      | er201\      |             |             |             |             |             |             |             |             |
      | 1opti\      |             |             |             |             |             |             |             |             |
      | mal`        |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | Syn.        | 280         | 0.21        | 30          | 86          | 83.3        | 0           | 0           | -0.198      |
      | methanation |             |             |             |             |             |             |             |             |
      | :cite:`\    |             |             |             |             |             |             |             |             |
      | g\          |             |             |             |             |             |             |             |             |
      | orre2\      |             |             |             |             |             |             |             |             |
      | 019pr\      |             |             |             |             |             |             |             |             |
      | oduct\      |             |             |             |             |             |             |             |             |
      | ion`        |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+


.. [359]
   Direct emissions due to combustion. Expressed
   in ton CO2 per MWh of fuel produced. Emissions computed based on
   resource used and produced and specific emissions given in :numref:`Table %s <tbl:prices_resources>`.

.. [360]
   Costs are adapted from :cite:`ro2007catalytic` and
   technical data from :cite:`poschl2010evaluation`.

.. [361]
   Data from
   :cite:`perez2016methanol` to produce 1 MWh of methanol,
   the process requires 1.355 MWh of hydrogen and also 0.04 MWh of
   electricity, 0.107 MWh of heating and 0.210 units of cooling. The
   process is simplified to 1.5 MWh of hydrogen needed to produce 1 MWh
   of methanol.

.. [362]
   This technology might be removed. Indeed, in this version of the
   model, synthetic liquid fuels are gathered together. However, they
   should be split in methanol, ethanol, bio-diesel... As a consequence,
   producing methanol from methane is cheaper than importing diesel.
   However in this version, methanol can be directly used as diesel
   :math:`\rightarrow` a competitor.

.. [363]
   A distinction is made between pyrolysis to LFO and other fuels. 
   The first can produce oil for heating or non-energy demand. The second produce a 
   blend of diesel and gasoline (18% of gasoline and 39.4% of diesel).





Carbon capture and storage
~~~~~~~~~~~~~~~~~~~~~~~~~~

As represented in  :numref:`Figure %s <fig:CO2andPtGLayers>`, two
technologies are proposed to capture the CO2, one from atmosphere (*CC
atmospheric*) and the other from exhaust gases of conversions processes
(*CC industry*), such as after a coal power plant. Indeed, resources
emit direct CO2 from combustion and *CC industry* can concentrate CO2
contained in the exhaust gas and inject it in CO2 captured layer. The
same process can be performed at a higher energetical cost with CO2 from
the atmosphere. No restriction on the available limit of CO2 from the
atmosphere is considered. Data are summarised in :numref:`Table %s <tbl:CC_techs>`.

We suppose that *CC industry* has similar characteristics than a
sequestration unit on a coal power plant as proposed in
:cite:`DanishEnergyAgency2019`. Based on our own
calculation, we evaluated the economical and technical data. We assumed
that the energy drop of the power plant represents the amount of energy
that the sequestration unit consumes. We assume that this energy must be
supplied by electricity.

For *CC atmospheric*, :cite:t:`Keith2018` proposed an
installation where 1 ton of CO2 is captured from the atmosphere with 1.3
kWh of natural gas and electricity. We assume that it can be done with
1.3 kWh of electricity. The thermodynamical limit is estimated to be
around 0.2 kWh of energy to sequestrate this amount
:cite:`Sanz-Perez2016`.


.. container::

   .. table:: Carbon capture (CC) technologies, in 2035. :math:`E_e` represents the electricity required to capture sequestrate CO2. :math:`\eta_{CO_2}` represents the amount of CO2 sequestrated from the CO2 source. Abbreviations: industrial (ind.), atmospheric (atm.).
      :name: tbl:CC_techs
 
 
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | :math:`c_   | :math:`c_   | :math:`life | :math:`E_e` | :math:`\eta_| :math:`f_   | :math:`f_   |
      |             | {inv}`      | {maint}`    | time`       |             | {CO_2}`     | {min,\%}`   | {max,\%}`   |
      |             |             |             |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      |             | [€\ :math:`_| [€\ :math:`_| [y]         | [kWh\:sub`e`| [%]         | [%]         | [%]         |
      |             | {2015}`/kg\ | {2015}`/kg\ |             | /           |             |             |             |
      |             | :math:`_    | :math:`_    |             | kg\         |             |             |             |
      |             | {CO_2}`/h]  | {CO_2}`/h   |             | :sub:`2`]   |             |             |             |
      |             |             | /y]         |             |             |             |             |             |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | CC Ind.     | 2580        | 64.8        | 40          | 0.233       | 90 [367]_   | 0           | 100         |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
      | CC Atm.     | 5160 [368]_ | 129.6       | 40          | 1.3         | 100         | 0           | 100         |
      +-------------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+


.. [367]
   We consider that 10% of the CO2 cannot be collected.

.. [368]
   Based on the economical data given in :cite:`Keith2018`
   and own calculation.


No relevant data were found for the capacity factor (:math:`\textbf{c}_\textbf{p}`) and the
GWP associated to the unit construction.



.. _sec:app1_storage:

Storage
-------

Tables :numref:`%s <tab:StoDataBasic>` and
:numref:`%s <tab:StoDataAdvanced>` detail the data for the
storage technologies. :numref:`Table %s <tab:StoDataBasic>`
summarises the investment cost, GWP, lifetime and potential integration
of the different technologies. :numref:`Table %s <tab:StoDataAdvanced>` summarises the
technical performances of each technology.


.. container::
   

   .. table:: Storage technologies characteristics in 2035: costs, emissions and lifetime. Abbreviations: batteries (batt.), Battery Electric Vehicule (BEV), centralised (cen.), decentralised (dec.), Lithium-ions (Li-on), Natural Gas (NG), Plug-in Hybrid Electric Vehicle (PHEV), Pumped Hydro Storage (PHS), seasonal (seas.), temperature (temp.) and thermal storage (TS).
      :name: tab:stodatabasic

      +-----------+-----------+-----------+-----------+-----------+
      |           | :math:`c_ | :math:`c_ | :math:`gw | :math:`li |
      |           | {inv}`    | {maint}`  | p_{con    | fetime`   |
      |           |           |           | str}`     |           |
      +-----------+-----------+-----------+-----------+-----------+
      |           | [€:math:` | [€:math:` | [kgCO\    | [y]       |
      |           | \_{2015}` | \_{2015}` | :sub:`2`  |           |
      |           | /kWh]     | /kWh/y]   | -eq./kWh] |           |
      +-----------+-----------+-----------+-----------+-----------+
      | Li-on     | 302       | 0.62      | 61.3      | 15 [296]_ |
      | batt.     | [294]_    | [294]_    | [295]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | PHS       | 58.8      | 0 [297]_  | 8.33      | 50 [299]_ |
      |           |           |           | [298]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | TS dec.   | 19.0      | 0.13      | 0         | 25        |
      |           | [300]_    | [300]_    | [297]_    | [300]_    |
      +-----------+-----------+-----------+-----------+-----------+
      | TS seas.  | 0.54      | 0.003     | 0         | 25        |
      | cen.      | [301]_    | [301]_    | [297]_    | [301]_    |
      +-----------+-----------+-----------+-----------+-----------+
      | TS daily  | 3         | 0.0086    | 0         | 40        |
      | cen.      | [301]_    | [301]_    | [297]_    | [300]_    |
      +-----------+-----------+-----------+-----------+-----------+
      | TS high   | 28        | 0.28      | 0         | 25        |
      | temp.     |           |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | Gas       | 0.051     | 0.0013    | 0         | 30        |
      |           | [302]_    | [302]_    | [297]_    | [302]_    |
      +-----------+-----------+-----------+-----------+-----------+
      | H2        | 6.19      | 0.03      | 0         | 20        |
      |           | [303]_    | [303]_    | [297]_    | [303]_    |
      +-----------+-----------+-----------+-----------+-----------+
      | Diesel    | 6.35e-3   | 3.97e-4   | 0         | 20        |
      | [304]_    |           |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | Gasoline  | 6.35e-3   | 3.97e-4   | 0         | 20        |
      | [304]_    |           |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | LFO       | 6.35e-3   | 3.97e-4   | 0         | 20        |
      | [304]_    |           |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | Ammonia   | 6.35e-3   | 3.97e-4   | 0         | 20        |
      | [304]_    |           |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | Methanol  | 6.35e-3   | 3.97e-4   | 0         | 20        |
      | [304]_    |           |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+
      | CO2       | 49.5      | 0.495     | 0         | 20        |
      | [305]_    | [306]_    |           | [297]_    |           |
      +-----------+-----------+-----------+-----------+-----------+


.. [294]
   We assume a Lithium-ion NMC battery at a
   utility-scale in 2030 :cite:`DanishEnergyAgency2018` with
   average use of 100 cycles/year.

.. [295]
   Data from Table 4 of :cite:`limpens2018electricity`.

.. [296]
   Trade off between various sources:
   :cite:`Zakeri2015,DanishEnergyAgency2018`

.. [297]
   Neglected.

.. [298]
   Own calculation based on Hydro Dams emissions from previous work
   :cite:`Limpens2019,Moret2017PhDThesis`.

.. [299]
   Data verified in Table B1 of
   :cite:`Zakeri2015`.

.. [300]
   Adapted from Table 5.2 of
   :cite:`Moritz2015`.

.. [301]
   The technologies used are pit thermal energy
   storage technology and Large-scale hot water tanks for seasonal and
   daily DHN storage, respectively. Data was taken for year 2030
   :cite:`DanishEnergyAgency2018`.

.. [302]
   Data from the Torup Lille
   project :cite:`DanishEnergyAgency2018`. The lifetime is
   assumed similar to a cavern for hydrogen storage.

.. [303]
   Based on tank storage from the JRC
   project:cite:`simoes2013jrc`. The cost is assumed as the
   average of 2020 and 2050 costs.

.. [304]
   In this implementation, the power of fuel imported can be constrained to be constant among the year. 
   Thus, a storage is created for the fuel, even if the storage cost is negligeable (see Eq. :eq:`eq:import_resources_constant`).
   Data were obtained by our own calculation.  


.. [305]
   Based on liquid CO2 tank storage. Data from a
   datasheet of *Ever grow gas* company https://www.evergrowgas.com/.
   Lifetime and maintenance cost based on own calculation.

.. [306]
   Units: **c\ inv** [€\ \ :sub:`2015`/tCO\ \ :sub:`2`],
   **c\ op** [€\ \ :sub:`2015`/tCO\ \ :sub:`2`/y]


The PHS in Belgium can be resumed to the Coo-Trois-Ponts hydroelectric
power station. The characteristics of the station in 2015 are the
following: installed capacity turbine (1164MW), pumping (1035MW),
overall efficiency of 75%, all reservoirs capacity (5000 MWh). We assume
that the energy losses is shared equally between the pumping and
turbining, resulting by a charge/discharge efficiencies of 86.6%. The
energy to power ratio are 4h50 and 4h18 for charge and discharge,
respectively :cite:`Electrabel2014`. A project started to
increase the height of the reservoirs and thus increase the capacity by
425 MWh. In addition, the power capacity will be increase by 80MW. The
overall project cost is estimated to 50M€ and includes also renovation
of other parts [307]_. We arbitrary assume that 50% is dedicated for the
height increase. It results in an investment cost of 58.8€\ :sub:`2015`
per kWh of new capacity. The overall potential of the PHS could be
extended by a third reservoir with an extra capacity of around 1.2 GWh.
Hence, we assume that the upper limit of PHS capacity is 6.5 GWh. No
upper bound were constrained for other storage technologies.

Estimation for the gas storage is based on an existing facility using
salt caverns as reservoirs: Lille Torup in Danemark
:cite:`DanishEnergyAgency2018`. The project cost is
estimated to 254M€\ :sub:`2015` for an energy capacity of 4965 GWh. The
yearly operating cost is estimated to 6.5 M€\ :sub:`2015`. Part of it is
for electricity and gas self consumption. We assume that the electricity
is used for charging the system (compressing the gas) and the gas is
used for heating up the gas during the discharge. These quantities
slightly impact the charge and discharge efficiency of the system. The
charge and discharge power are 2200 and 6600 [MW] respectively. As the
technology is mature, we assume that the cost of the technology in 2035
will be similar to Lille Torup project.


.. container::

   .. table:: Storage technologies characteristics in 2035: efficiencies, energy to power ratios, losses and availabilities. Abbreviations: batteries (batt.), Battery Electric Vehicule (BEV), centralised (cen.), decentralised (dec.), Lithium-ions (Li-on), Natural Gas (NG), Plug-in Hybrid Electric Vehicle (PHEV), Pumped Hydro Storage (PHS), seasonal (seas.), temperature (temp.) and thermal storage (TS).
      :name: tab:stodataadvanced

      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      |               | :math:`\eta_  | :math:`\eta_  | :math:`t_     | :math:`t_     | :math:`%_     | :math:`%_     |
      |               | {sto,in}`     | {sto,out}`    | {sto,in}`     | {sto,out}`    | {sto_{loss}}` | {sto_{avail}}`|
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      |               | [-]           | [-]           | [h]           | [h]           | [s\ :math:`^  | [-]           |
      |               |               |               |               |               | {-1}`]        |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Li-on         | 0.95          | 0.95          | 4             | 4             | 2e-4          | 1             |
      | batt.         | [326]_        | [326]_        | [326]_        | [326]_        | [326]_ [327]_ |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | BEV           | 0.95          | 0.95          | 4             | 10            | 2e-4          | 0.2           |
      | batt.         | [326]_        | [326]_        | [328]_        | [328]_        | [326]_ [327]_ | [328]_        |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | PHEV          | 0.95          | 0.95          | 4             | 10            | 2e-4          | 0.2           |
      | batt.         | [326]_        | [326]_        | [328]_        | [328]_        | [326]_ [327]_ | [328]_        |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | PHS           | 0.866         | 0.866         | 4.30          | 4.83          | 0             | 1             |
      |               |               |               |               |               | [329]_        |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | TS dec.       | 1             | 1             | 4             | 4             | 82e-4         | 1             |
      |               | [329]_        | [329]_        | [328]_        | [328]_        | [330]_        |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | TS            | 1             | 1             | 150           | 150           | 6.06e-5       | 1             |
      | seas.         | [331]_        | [331]_        | [331]_        | [331]_        | [331]_        |               |
      | cen.          |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | TS            | 1             | 1             | 60.3          | 60.3          | 8.33e-3       | 1             |
      | daily         | [331]_        | [331]_        | [331]_        | [331]_        | [331]_        |               |
      | cen.          |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | TS high       | 1             | 1             | 2             | 2             | 3.55e-4       | 1             |
      | temp.         | [331]_        | [331]_        |               |               | [331]_        |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | NG            | 0.99          | 0.995         | 2256          | 752           | 0             | 1             |
      |               | [332]_        | [332]_        | [332]_        | [332]_        |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | H2            | 0.90          | 0.98          | 4             | 4             | 0             | 1             |
      |               | [333]_        | [333]_        | [333]_        | [333]_        |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Diesel        | 1             | 1             | 168           | 168           | 0             | 1             |
      | [334]_        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Gasoline      | 1             | 1             | 168           | 168           | 0             | 1             |
      | [334]_        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | LFO           | 1             | 1             | 168           | 168           | 0             | 1             |
      | [334]_        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Ammonia       | 1             | 1             | 168           | 168           | 0             | 1             |
      | [334]_        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | Methanol      | 1             | 1             | 168           | 168           | 0             | 1             |
      | [334]_        |               |               |               |               |               |               |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+
      | CO2           | 1             | 1             | 1             | 1             | 0             | 1             |
      +---------------+---------------+---------------+---------------+---------------+---------------+---------------+


.. [326]
   Data verified in Table B1 of
   :cite:`Zakeri2015`.

.. [327]
   Data from Table 4 of
   :cite:`limpens2018electricity`.

.. [328]
   Own calculation.

.. [329]
   Neglected.

.. [330]
   Adapted from Table 5.2 of
   :cite:`Moritz2015`

.. [331]
   Based on the Pit thermal energy storage
   technology in 2030 for seasonal and Large-scale hot water tanks for
   DHN daily storage. Data from
   :cite:`DanishEnergyAgency2018`.

.. [332]
   Data from the Torup Lille
   project:cite:`DanishEnergyAgency2018`. Efficiencies are
   based on our own calculation based on electricity and gas consumed by
   the installation over a year.

.. [333]
   :cite:t:`Sadaghiani2017` an efficiency of
   88.6% in an ideal configuration for liquid hydrogen liquefaction.
   This high efficiency is used and we arbitrary impose that the charge
   efficiency is 90% and the discharge 98%. The tank design by JRC
   :cite:`simoes2013jrc` has a charge/discharge energy to
   power ratio of 4 hours.

.. [334]
   We assume a perfect storage with 1 week of charge/discharge time.




.. _App:Data:OtherParam:

Others 
------

.. _ssec:app1_grid:

Electricity grid
~~~~~~~~~~~~~~~~

No data were found for the Belgian grid. Hence, by assuming that the
grid cost is proportional to the population, the Belgian grid cost can
be estimated based on the known Swiss grid cost. In 2015, the population
of Belgium and Switzerland were 11.25 and 8.24 millions, respectively
(Eurostat). The replacement cost of the Swiss electricity grid is 58.6
billions CHF\ :sub:`2015`
:cite:`association_des_entreprises_electriques_suisses_aes_scenarios_2012`
and its lifetime is 80 years :cite:`stump_swiss_2010`. The
electricity grid will need additional investment depending on the
penetration level of the decentralised and stochastic electricity
production technologies. The needed investments are expected to be 2.5
billions CHF\ :sub:`2015` for the high voltage grid and 9.4 billions
CHF\ :sub:`2015` for the medium and low voltage grid. This involves the
deployment of 25GW of PV and 5.3 GW of wind onshore. These values
correspond to the scenario 3 in
:cite:`association_des_entreprises_electriques_suisses_aes_scenarios_2012`.
The lifetime of these additional investments is also assumed to be 80
years.

By assuming a linear correlation between grid reinforcement and
intermittent renewable deployment, the specific cost of integration is
estimated to 393 MCHF per GW of renewable intermittent energy installed
(:math:`(9.4+2.5)`\ bCHF\ :math:`/(25+5.3)GW = 0.393`\ bCHF/GW) .

As a consequence, the estimated cost of the Belgian grid is
:math:`58.6/1.0679\cdot 11.25/8.24=74.9` b€\ :sub:`2015`. And the extra
cost is :math:`393/1.0679\approx 367.8` M€\ :sub:`2015`/GW.

Belgium is strongly interconnected to neighbouring countries. Based on
an internal report of the TSO
:cite:`ELIA_2016_avancementInterconnexion`, the TTC is
estimated to be 6500 GW in 2020, which is in line with another study
from EnergyVille :cite:`Meinke-Hubeny2017` and the ENTSOE
:cite:`ENTSO-E2019`. However, the NTC published by the TSO
on his website is much lower, around 3100 MW: 950 MW from Netherlands,
1800 MW from France and 350 MW from England (in 2020). This NTC is
defined as ‘*The net transfer capacity (NTC) is the forecast transfer
capacity agreed by Elia and its neighbouring transmission system
operators (TSOs) for imports and exports across Belgium’s borders. [...]
EU Regulation 543/2013 refers to net transmission capacity as
‘forecasted capacity’.*’ [369]_. As explained in an internal report of
the TSO :cite:`ELIA_ntcCalculation_2019`, the TTC is an
upper bound of the NTC. In the literature, studies analysing the Belgium
energy system accounts for the TTC, thus this capacity was implemented
in this work: 6500 MW in 2020. The ENTSOE published his Ten Year Network
Development Plan for different periods up to 2040. They estimates, if
all projects are commissionned before 2035, the cross border capacities
in 2035 up to 14 780 MW, which represents more than twice the available
capacity in 2020 :cite:`ENTSO-E2019`. 
:numref:`Figure %s <fig:be_ttc>` illustrates the capacity changes for each
neighbouring country, interconnections are reinforced in every countries
more or less proportionally to the existing capacities.


.. figure:: /images/belgian_data/TTC_entsoe.png
   :alt: Expected capacities between Belgium and neighbouring countries. Data from :cite:`ENTSO-E2019`.
   :name: fig:be_ttc
   :width: 14cm

   Expected capacities between Belgium and neighbouring countries. Data
   from :cite:`ENTSO-E2019`.


Losses (:math:`\%_{\emph{net\textsubscript{loss}}}`) in the electricity
grid are fixed to 4.7%. This is the ratio between the losses in the grid
and the total annual electricity production in Belgium in
2016 :cite:`Eurostat2017`.


In a study about “\ *electricity scenarios for Belgium towards
2050*\ ´´, the TSO estimates the overall import capacity up to 9.88 GW
:cite:`EliaSystemOperator2017`. The interconnections are
built as follow: 3.4 GW from Netherlands, 4.3 GW from France, 1.0 GW
from Germany, 1.0 GW from Great Britain and 0.18 GW from
Luxembourg [370]_. However, a maximum simultaneous import capacity is
fixed to 6.5 GW and justified as follow “\ *Additionally, the total
maximum simultaneous import level for Belgium is capped at 6500 MW. For
a relatively small country with big and roughly adequate neighbours, the
simulations show that a variable import volume up to the maximum of 6500
MW can happen, thanks to the non-simultaneousness of peaks between the
countries. But during certain hours, there is not enough generation
capacity abroad due to simultaneous needs in two or more countries which
will result in a lower import potential for Belgium. This effect is
taken into account in the model*\ ´´
:cite:`EliaSystemOperator2017`. The same ratio of
simultaneous import and NTC (66%) is used for the other years.

Losses (:math:`%_{net_{loss}}`) in the electricity
grid are fixed to 4.7%. This is the ratio between the losses in the grid
and the total annual electricity production in Belgium in
2016 :cite:`Eurostat2017`.


.. _app:DHN_grid_data:

DHN grid
~~~~~~~~

For the DHN, the investment for the network is also accounted for. The
specific investment (:math:`c_{inv}`) is 882 CHF\ :sub:`2015`/kW\ :sub:`th` in
Switzerland. This value is based on the mean value of all points in
:cite:`s._thalmann_analyse_2013` (Figure 3.19), assuming a
full load of 1535 hours per year (see table 4.25 in
:cite:`s._thalmann_analyse_2013`). The lifetime of the DHN
is expected to be 60 years. DHN losses are assumed to be 5%.

As no relevant data were found for Belgium, the DHN infrastructure cost
of Switzerland was used. As a consequence, the investment cost
(:math:`c_{inv}`) is 825 €\ :sub:`2015`/kW\ :sub:`th`. Based on the heat
roadmap study :cite:`Paardekooper2018`, heat provided by DHN
is “*around 2% of the heating for the built environment (excluding for
industry) today to at least 37% of the heating market in 2050*”. Hence,
the lower (*%\ dhn,min*) and upper bounds (*%\ dhn,max*) for the use of
DHN are 2% and 37% of the annual low temperature heat demand,
respectively.
 

Energy demand reduction cost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By replacing former device at the end user side, the EUD can be reduced.
This is usually called an ‘*energy efficiency*’ measure. As an example,
by insulating a house, the space heating demand can be reduced. However,
energy efficiency has a cost which represents the extra cost to reduce
the final energy needed to supply the same energy service. As in the
model the demand reduction is fixed, hence the energy efficiency cost is
fixed. The American Council for an Energy-Efficient Economy summarises
study about the levelised cost of energy savings
:cite:`ACEEE2015`. They conclude that this cost is below
0.04 USD\ :sub:`2014`/kWh saved and around 0.024 USD\ :sub:`2014`/kWh,
hence 0.018€\ :sub:`2015`/kWh. In 2015, Belgium FEC was 415 TWh
:cite:`EurostatEnergyBalanceSheets2015` and the energy
efficiency around 15% compare to 1990. The European target is around 35%
in 2035, hence the energy efficiency cost for Belgium between 2015 and
2035 is 3.32b€\ :sub:`2015`. This result is in line with another study
for Switzerland where the energy efficiency cost is 1.8b€\ :sub:`2015`
for the same period and similar objectives
:cite:`_perspectives_2013` (see
:cite:`Moret2017PhDThesis` for more details about
Switzerland).









.. [1]
   The database is consulted online: http://www.ecoinvent.org

.. [2]
   *Real* values are expressed at the net of inflation. They differ from
   *nominal* values, which are the actual prices in a given year,
   accounting for inflation.


.. [9]
   250 km\ \ :math:`^2` represents almost a hundredth
   of Belgium’s land area, which is 28635 km\ \ :math:`^2`. The total
   area, accounting for water areas, of Belgium is
   30528 km\ \ :math:`^2`. From
   https://fr.wikipedia.org/wiki/G%C3%A9ographie_de_la_Belgique, visited
   the 10/08/2020.

.. [10]
   A similar calculation was done for solar thermal with an efficiency
   of 28%.

.. [11]
   In the study, potential are given in PetaJoules of electricity per
   year (58-185 PJ for onshore and 8-10 PJ for offshore) for EROI of 5
   and 12 (see Table 13 of :raw-latex:`\cite{Dupont2017}`). To convert
   energy into power capacity, capacity factors of 24% and 41% for
   onshore and offshore, were assumed respectively.


.. [37b]
   From
   https://www.eea.europa.eu/data-and-maps/indicators/heating-degree-days-2,
   consulted the 06-12-2019

.. [38]
   Source: https://ec.europa.eu/eurostat, consulted the 06/12/2019.


.. [40]
   it corresponds to the share of 2015 (From Tables
   2.2.3 and 2.3.3 of :cite:`Eurostat2017`), in line with
   data from the SPF :cite:`SPF-Mobility2017`.


.. [257]
   from https://en.wikipedia.org/wiki/Nissan_Leaf, consulted on
   29-01-2019

.. [258]
   from https://fr.wikipedia.org/wiki/Toyota_Prius, consulted on
   29-01-2019

.. [267]
   Value calculated based on the ratio between the transported tons and
   the consumed energy per technologies in 2015. Data from
   :cite:`EuropeanCommission2016`


.. [307]
   This information was shared by Engie, the facility manager
   https://corporate.engie-electrabel.be/projet-extension-centrale-coo/
   and also publicised by newspapers:
   https://www.renouvelle.be/fr/actualite-belgique/la-centrale-de-coo-augmente-sa-capacite-de-stockage,
   https://www.lameuse.be/403176/article/2019-06-20/va-agrandir-les-lacs-de-la-centrale-coo.


.. [335]
   Not all the characteristics of the cell has been implemented, thus
   PEM-EC can be competitive compare to other technologies.



.. [369]
   Information and definition from the TSO website:
   https://www.elia.be/en/grid-data/transmission/yearly-capacity,
   visited on the 29th of May 2020


.. [370]
   More details about capacities and projects are given in Figure 56 of
   :cite:`EliaSystemOperator2017`.


