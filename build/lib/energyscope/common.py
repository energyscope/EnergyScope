# -*- coding: utf-8 -*-
"""
This file defines a dictionary with global variables to be used in EnergyScope such as fuels, technologies, etc.
"""
import datetime

commons = {}

commons['logfile'] = str(datetime.datetime.now()).replace(':', '-').replace(' ', '_') + '.energyscope.log'


# list giving the order in which the technologies should be plotted into the layer elec graph
elec_order_graphs = ['IND_COGEN_GAS', 'IND_COGEN_WOOD', 'IND_COGEN_WASTE',
                'DHN_COGEN_GAS', 'DHN_COGEN_WOOD', 'DHN_COGEN_WASTE', 'DHN_COGEN_WET_BIOMASS',
                'DHN_COGEN_BIO_HYDROLYSIS',
                'DEC_COGEN_GAS', 'DEC_COGEN_OIL', 'DEC_ADVCOGEN_GAS', 'DEC_ADVCOGEN_H2',
                'CCGT',
                'PV', 'WIND_ONSHORE', 'WIND_OFFSHORE', 'HYDRO_RIVER',
                'BIOMASS_TO_METHANOL', 'BIO_HYDROLYSIS', 'PYROLYSIS_TO_LFO', 'PYROLYSIS_TO_FUELS',
                'ELECTRICITY',
                'PHS_Pout', 'BATT_LI_Pout', 'BEV_BATT_Pout', 'PHEV_BATT_Pout',
                'END_USE',
                'TRAMWAY_TROLLEY', 'TRAIN_PUB', 'CAR_PHEV', 'CAR_BEV', 'TRAIN_FREIGHT', 'TRUCK_ELEC',
                'HABER_BOSCH', 'SYN_METHANOLATION', 'OIL_TO_HVC', 'GAS_TO_HVC', 'BIOMASS_TO_HVC', 'ATM_CCS',
                'INDUSTRY_CCS',
                'DHN_HP_ELEC', 'DEC_HP_ELEC', 'DEC_DIRECT_ELEC',
                'IND_DIRECT_ELEC', 'H2_ELECTROLYSIS', 'PHS_Pin', 'BATT_LI_Pin', 'BEV_BATT_Pin', 'PHEV_BATT_Pin',
                'ELEC_EXPORT']

# dictionnary to map the names of the resources and technologies into the model into a format to be plotted
plotting_names = {'ELECTRICITY': 'Electricity',
                  'GASOLINE': 'Gasoline',
                  'DIESEL': 'Diesel',
                  'BIOETHANOL': 'Bioethanol',
                  'BIODIESEL': 'Biodiesel',
                  'LFO': 'Oil',
                  'GAS': 'Gas',
                  'GAS_RE': 'Gas RE',
                  'WOOD': 'Woody biomass',
                  'WET_BIOMASS': 'Wet biomass',
                  'COAL': 'Coal',
                  'URANIUM': 'Uranium',
                  'WASTE': 'Waste',
                  'H2': 'Hydrogen',
                  'H2_RE': 'Hydrongen RE',
                  'AMMONIA': 'Ammonia',
                  'METHANOL': 'Methanol',
                  'AMMONIA_RE': 'Ammonia RE',
                  'METHANOL_RE': 'Methanol RE',
                  'ELEC_EXPORT': 'Elec export',
                  'CO2_EMISSIONS': 'CO2 emissions',
                  'RES_WIND': 'Wind', 'RES_SOLAR': 'Solar', 'RES_HYDRO': 'Hydro', 'RES_GEO': 'Geothermal',
                  'CO2_ATM': 'CO2 atm', 'CO2_INDUSTRY': 'CO2 industry', 'CO2_CAPTURED': 'CO2 captured',
                  'NUCLEAR': 'Nuclear', 'CCGT': 'CCGT', 'CCGT_AMMONIA': 'CCGT ammonia',
                  'COAL_US': 'Coal US', 'COAL_IGCC': 'Coal IGCC',
                  'PV': 'PV', 'WIND_ONSHORE': 'Wind onshore', 'WIND_OFFSHORE': 'Wind offshore', 'HYDRO_RIVER': 'Hydro river',
                  'GEOTHERMAL': 'Geothermal',
                  'IND_COGEN_GAS': 'Ind. cogen. gas', 'IND_COGEN_WOOD': 'Ind. cogen. wood', 'IND_COGEN_WASTE': 'Ind. cogen. waste',
                  'IND_BOILER_GAS': 'Ind. boiler gas', 'IND_BOILER_WOOD': 'Ind. boiler wood', 'IND_BOILER_OIL': 'Ind. boiler oil',
                  'IND_BOILER_COAL': 'Ind. boiler coal', 'IND_BOILER_WASTE': 'Ind. boiler waste', 'IND_DIRECT_ELEC': 'Ind. direct elec.',
                  'DHN_HP_ELEC': 'DHN HP elec.',
                  'DHN_COGEN_GAS': 'DHN cogen. gas', 'DHN_COGEN_WOOD': 'DHN cogen. wood', 'DHN_COGEN_WASTE': 'DHN cogen. waste',
                  'DHN_COGEN_WET_BIOMASS': 'DHN cogen. wet biomass', 'DHN_COGEN_BIO_HYDROLYSIS': 'DHN cogen. bio hydrolysis',
                  'DHN_BOILER_GAS': 'DHN boiler gas', 'DHN_BOILER_WOOD': 'DHN boiler wood', 'DHN_BOILER_OIL': 'DHN boiler oil',
                  'DHN_DEEP_GEO': 'DHN deep geo',
                  'DHN_SOLAR': 'DHN solar',
                  'DEC_HP_ELEC': 'Dec. HP elec.', 'DEC_THHP_GAS': 'Dec. Thermal HP gas',
                  'DEC_COGEN_GAS': 'Dec. cogen. gas', 'DEC_COGEN_OIL': 'Dec. cogen. oil',
                  'DEC_ADVCOGEN_GAS': 'Dec. advcogen. gas', 'DEC_ADVCOGEN_H2': 'Dec. advcogen. h2',
                  'DEC_BOILER_GAS': 'Dec. boiler gas', 'DEC_BOILER_WOOD': 'Dec. boiler wood', 'DEC_BOILER_OIL': 'Dec. boiler oil',
                  'DEC_SOLAR': 'Dec. solar',
                  'DEC_DIRECT_ELEC': 'Dec. direct elec.',
                  'TRAMWAY_TROLLEY': 'Tramway trolley',
                  'BUS_COACH_DIESEL': 'Bus diesel', 'BUS_COACH_HYDIESEL': 'Bus hybrid diesel',
                  'BUS_COACH_CNG_STOICH': 'Bus gas', 'BUS_COACH_FC_HYBRIDH2': 'Bus FC hybrid',
                  'TRAIN_PUB': 'Train public',
                  'CAR_GASOLINE': 'Car gasoline', 'CAR_DIESEL': 'Car diesel',
                  'CAR_NG': 'Car gas', 'CAR_METHANOL': 'Car methanol',
                  'CAR_HEV': 'Car hybrid', 'CAR_PHEV': 'Car plug-in hybrid', 'CAR_BEV': 'Car elec..',
                  'CAR_FUEL_CELL': 'Car fuel cell',
                  'TRAIN_FREIGHT': 'Train freight',
                  'BOAT_FREIGHT_DIESEL': 'Boat freight diesel', 'BOAT_FREIGHT_NG': 'Boat freight gas',
                  'BOAT_FREIGHT_METHANOL': 'Boat freight methanol',
                  'TRUCK_DIESEL': 'Truck diesel', 'TRUCK_METHANOL': 'Truck methanol',
                  'TRUCK_FUEL_CELL': 'Truck fuel cell', 'TRUCK_ELEC': 'Truck elec.', 'TRUCK_NG': 'Truck gas',
                  'EFFICIENCY': 'Efficiency', 'DHN': 'DHN', 'GRID': 'Grid',
                  'H2_ELECTROLYSIS': 'H2 elec.trolysis', 'SMR': 'H2 SMR', 'H2_BIOMASS': 'H2 biomass',
                  'GASIFICATION_SNG': 'Wood gasification', 'SYN_METHANATION': 'Synthetic methanation',
                  'BIOMETHANATION': 'Biomethanation', 'BIO_HYDROLYSIS': 'Bio hydrolysis',
                  'PYROLYSIS_TO_LFO': 'Pyrolysis to oil', 'PYROLYSIS_TO_FUELS': 'Pyrolysis to fuels',
                  'ATM_CCS': 'Atmospheric CCS', 'INDUSTRY_CCS': 'Industry CCS',
                  'SYN_METHANOLATION': 'Synthetic methanolation', 'METHANE_TO_METHANOL': 'Methane to methanol',
                  'BIOMASS_TO_METHANOL': 'Biomass to methanol', 'HABER_BOSCH': 'Haber bosch',
                  'AMMONIA_TO_H2': 'Ammonia to H2', 'OIL_TO_HVC': 'Oil to HVC', 'GAS_TO_HVC': 'Gas to HVC',
                  'BIOMASS_TO_HVC': 'Biomass to HVC', 'METHANOL_TO_HVC': 'Methanol to HVC',
                  'END_USE':'End use',
                  'PHS': 'Pumped hydro sto.', 'BATT_LI': 'Lithium batt.', 'BEV_BATT': 'Electric vehicle batt.', 'PHEV_BATT': 'Plug-in hybrid batt.',
                  'TS_DEC_DIRECT_ELEC': 'TS dec. direct elec.', 'TS_DEC_HP_ELEC': 'Thermal sto. dec.',
                  'TS_DEC_THHP_GAS': 'TS dec. THHP gas',
                  'TS_DEC_COGEN_GAS': 'TS dec. cogen. gas', 'TS_DEC_COGEN_OIL': 'TS dec. cogen. oil',
                  'TS_DEC_ADVCOGEN_GAS': 'TS dec. advcogen. gas', 'TS_DEC_ADVCOGEN_H2': 'TS dec. advcogen. h2',
                  'TS_DEC_BOILER_GAS': 'TS dec. boiler gas', 'TS_DEC_BOILER_WOOD': 'TS dec. boiler wood',
                  'TS_DEC_BOILER_OIL': 'TS dec. boiler oil',
                  'TS_DHN_DAILY': 'TS DHN daily', 'TS_DHN_SEASONAL': 'Thermal sto. DHN seasonal',
                  'TS_HIGH_TEMP': 'Thermal sto. high temp.',
                  'GAS_STORAGE': 'Gas storage', 'H2_STORAGE': 'H2 storage',
                  'DIESEL_STORAGE': 'Diesel storage', 'GASOLINE_STORAGE': 'Gasoline storage',
                  'LFO_STORAGE': 'Oil storage',
                  'AMMONIA_STORAGE': 'Ammonia storage', 'METHANOL_STORAGE': 'Methanol storage',
                  'CO2_STORAGE': 'CO2 storage'}

# dictionnary specifying the colors of the different technologies for plot of the elec layer
colors_elec = {'Ind. cogen. gas': '#DC143C', # Heat HT in sankey
               'CCGT': '#FFD700', # Gas in sankey
               'PV': '#FFFF00', # Solar in sankey
               'Wind onshore': '#00B050', # Light green
               'Wind offshore': '#548235', # Darker green
               'Other prod.': '#a85432', # Red-brown
               'Pumped hydro sto. Pout': '#0369AB', # blue
               'Pumped hydro sto. Pin': '#0369AB', # blue
               'Electric vehicle batt. Pout': '#BD7B00', # light brown
               'Electric vehicle batt. Pin': '#BD7B00', # Light brown
               'End use': '#BAD3EE', # Light blue
               'Public mobility': '#EDA200', # Very light brown
               'Other cons.': '#329da8', # Blue-green
               'DHN HP elec.': '#F20000', # Red
               'Dec. HP elec.': '#FF6D66', # Light red
               'Ind. direct elec.': '#B60000', # Dark red
               'Lithium batt. Pout': '#6fb1c7', #Light blue (close to elec)
               'Lithium batt. Pin': '#6fb1c7', # Light blue (close to elec)
               'Electricity': '#00BFFF', # Light blue
               'Elec export': '#00BFFF'  # Light blue
}
#TODO add other tech into colors_elec