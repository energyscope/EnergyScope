import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import energyscope as es
import plotly.subplots as sp


directory_path = os.path.join(os.getcwd(),'case_studies', 'paper1', 'base_case')
df = es.file_compute_parameters(directory_path, False, False)

row = {'CASE_NUMBER': [], 'E_FUEL': [], 'E_BIO_FUEL': [], 'BIOFUEL': [], 'TOTAL_FUEL_PRODUCED': [],
                'COST': [], 'BIOMASS_SEQU': [], 'SEQU': [], 'ELEC': [],
                'BIOMASS_USE': [], 'CC_SHARE': [], 'QTT_JETFUEL_IMP': [],
                'ELY_LOAD_FACTOR': [], 'PV_PROD': [], 'WIND_PROD': [], 'H2_PROD': [],
                'NG_STORAGE': [], 'H2_STORAGE': [], 'METHANOL_STORAGE': [], 'AMMONIA_STORAGE': [],
                'DAC': [], 'METHANOL_PROD': [], 'TRUCK_H2': [], 'QTT_JETFUEL_IMPORT': [], 'PRICE_QTT_JETFUEL_IMPORT': []}
for index, row in df.iterrows():
    print('-------------------', index, '--------------------')
    print('Folder name : ', row['FOLDER_NAME'])
    print('Total cost of the system (MEUR) : ', round(row['COST'],1))
    print('Electricity produced (TWHh) : ', round(row['ELEC'],1))
    print('Hydrogen produced (TWh) : ', round(row['H2_PROD'],1))
    print('Biomass sequ  (TWh) : ', round(row['BIOMASS_SEQU'],1))
    print('Carbon capture share (%) : ', round(row['CC_SHARE'],1))
    print('Share E/E-Bio/Bio-Fuel (%) : ', round(row['E_FUEL'],1), round(row['E_BIO_FUEL'],1), round(row['BIOFUEL'],1))
    share_prod_jetfuel = round(1-row['QTT_JETFUEL_IMP']/91000, 3)
    print('Share jetfuel e/e-bio/bio/fossil fuel', share_prod_jetfuel*row['SHARE_EFUEL_PROD_FT'], round(share_prod_jetfuel*row['SHARE_EBIOFUEL_PROD_FT'],2), round(share_prod_jetfuel*row['SHARE_BIOFUEL_PROD_FT'], 2), round(row['QTT_JETFUEL_IMP']/91000,2))
    print('Quantity of biomass for jet fuel production (TWh) : ', row['BIOMASS_PROD_FT'])
    print('Quantity of co2 for jet fuel production (mtCO2) : ', row['CO2_PROD_FT'])
    print('Quantity of hydrogen for jet fuel production (TWh) : ', row['HYDROGEN_PROD_FT'])
    print('Quantity of jet fuel imported (TWh) : ', row['QTT_JETFUEL_IMP'])
    print('BIOMASS_USE', row['BIOMASS_USE'])