import pandas as pd
import os
import energyscope as es
from pathlib import Path

# TODO adapt to updates and test
# TODO write doc

def run_ESTD_UQ(sample):

    # define project path
    project_path = Path(__file__).parents[2]

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn=os.path.join(project_path,'config_ref.yaml'), project_path=project_path)
    config['Working_directory'] = os.getcwd() # keeping current working directory into config

    # Reading the data of the csv
    es.import_data(config)

    s = sample[0]
    sample_index = s[0]
    sample_dict = s[1]
    print()
    name = sample[1]

    config['case_study'] = name + '/Run_{}'.format(sample_index)

    config['print_sankey'] = False #For the UQ analysis, no need to print the Sankey

    # # Test to update uncertain parameters
    uncer_params = sample_dict

    config['all_data'] =  es.transcript_uncertainties(uncer_params,config)

    # Printing the .dat files for the optimisation problem
    es.print_data(config)

    # Running EnergyScope
    es.run_es(config)

    # Example to get total cost
    total_cost = es.get_total_cost(config)

    return total_cost




def transcript_uncertainties(uncer_params, config):

    # to fill the undefined uncertainty parameters
    uncert_param = config['all_data']['Uncertainty_ranges']

    up = dict.fromkeys(uncert_param.index)

    rel_uncert_param = uncert_param.loc[uncert_param['Type']=='Relative']

    # Set here the value uncertain parameters, 0.0
    up.update(dict.fromkeys(rel_uncert_param.index,0.0))

    # Set here the nominal value of the absolute uncertain parameters
    up['f_max_nuc'] = config['all_data']['Technologies'].loc['NUCLEAR', 'f_max']

    # Extract the new value from the RHEIA sampling
    for key in uncer_params:
        up[key] = uncer_params[key]

    config['all_data']['Misc']['i_rate'] *= (1. + up['param_i_rate'])
    config['all_data']['Resources'].loc['ELECTRICITY', 'avail'] *= (1. + up['avail_elec'])
    config['all_data']['Resources'].loc['WASTE', 'avail'] *= (1. + up['avail_waste'])
    config['all_data']['Resources'].loc['COAL', 'avail'] *= (1. + up['avail_coal'])
    config['all_data']['Resources'].loc['WOOD', 'avail'] *= (1. + up['avail_biomass'])
    config['all_data']['Resources'].loc['WET_BIOMASS', 'avail'] *= (1. + up['avail_biomass'])
    # Changing cost of operating:
    config['all_data']['Resources'].loc['ELECTRICITY', 'c_op'] *= (1. + up['c_op_electricity'])
    config['all_data']['Resources'].loc['COAL', 'c_op'] *= (1. + up['c_op_coal'])
    # c_op biomass
    config['all_data']['Resources'].loc['WOOD', 'c_op'] *= (1. + up['c_op_biomass'])
    config['all_data']['Resources'].loc['WET_BIOMASS', 'c_op'] *= (1. + up['c_op_biomass'])
    # c_op_biofuels
    config['all_data']['Resources'].loc['BIODIESEL', 'c_op'] *= (1. + up['c_op_biofuels'])
    config['all_data']['Resources'].loc['BIOETHANOL', 'c_op'] *= (1. + up['c_op_biofuels'])
    # c_op_syn_fuels
    config['all_data']['Resources'].loc['H2_RE', 'c_op'] *= (1. + up['c_op_syn_fuels'])
    config['all_data']['Resources'].loc['GAS_RE', 'c_op'] *= (1. + up['c_op_syn_fuels'])
    config['all_data']['Resources'].loc['METHANOL_RE', 'c_op'] *= (1. + up['c_op_syn_fuels'])
    config['all_data']['Resources'].loc['AMMONIA_RE', 'c_op'] *= (1. + up['c_op_syn_fuels'])
    # c_op_ hydrocarbons
    config['all_data']['Resources'].loc['GASOLINE', 'c_op'] *= (1. + up['c_op_hydrocarbons'])
    config['all_data']['Resources'].loc['DIESEL', 'c_op'] *= (1. + up['c_op_hydrocarbons'])
    config['all_data']['Resources'].loc['LFO', 'c_op'] *= (1. + up['c_op_hydrocarbons'])
    config['all_data']['Resources'].loc['H2', 'c_op'] *= (1. + up['c_op_hydrocarbons'])
    config['all_data']['Resources'].loc['GAS', 'c_op'] *= (1. + up['c_op_hydrocarbons'])
    config['all_data']['Resources'].loc['METHANOL', 'c_op'] *= (1. + up['c_op_hydrocarbons'])
    config['all_data']['Resources'].loc['AMMONIA', 'c_op'] *= (1. + up['c_op_hydrocarbons'])

    config['all_data']['Technologies'].loc['PV', 'c_inv'] *= (1. + up['c_inv_pv'])
    config['all_data']['Technologies'].loc['WIND_ONSHORE', 'c_inv'] *= (1. + up['c_inv_wind_onshore'])
    config['all_data']['Technologies'].loc['WIND_OFFSHORE', 'c_inv'] *= (1. + up['c_inv_wind_offshore'])
    config['all_data']['Technologies'].loc['DHN_HP_ELEC', 'c_inv'] *= (1. + up['c_inv_dhn_hp_elec'])
    config['all_data']['Technologies'].loc['DEC_HP_ELEC', 'c_inv'] *= (1. + up['c_inv_dec_hp_elec'])
    
    config['all_data']['Technologies'].loc['H2_ELECTROLYSIS', 'c_inv'] *= (1. + up['c_inv_h2_electrolysis'])

    config['all_data']['Technologies'].loc['PV', 'f_max'] *= (1. + up['f_max_pv'])
    config['all_data']['Technologies'].loc['WIND_ONSHORE', 'f_max'] *= (1. + up['f_max_windon'])
    config['all_data']['Technologies'].loc['WIND_OFFSHORE', 'f_max'] *= (1. + up['f_max_windoff'])

    # demand
    config['all_data']['Demand'].loc[
        'ELECTRICITY', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'elec_extra'])
    config['all_data']['Demand'].loc[
        'LIGHTING', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'elec_extra'])
    config['all_data']['Demand'].loc[
        'HEAT_HIGH_T', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'ht_extra'])
    config['all_data']['Demand'].loc[
        'HEAT_LOW_T_SH', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'sh_extra'])
    config['all_data']['Demand'].loc[
        'MOBILITY_PASSENGER', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'passenger_extra'])
    config['all_data']['Demand'].loc[
        'MOBILITY_FREIGHT', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'freight_extra'])
    config['all_data']['Demand'].loc[
        'NON_ENERGY', config['all_data']['Demand'].select_dtypes(include=['number']).columns] *= (1. + up[
        'ned_extra'])

    # hourly capacity factors of RE
    config['all_data']['Time_series'].loc[:, 'PV'] *= (1. + up['cpt_pv'])
    config['all_data']['Time_series'].loc[:, 'Wind_onshore'] *= (1. + up['cpt_winds'])
    config['all_data']['Time_series'].loc[:, 'Wind_offshore'] *= (1. + up['cpt_winds'])

    # update mobility costs
    config['all_data']['Technologies'].loc['BUS_COACH_DIESEL', 'c_inv'] *= (1. + up['c_inv_bus']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['BUS_COACH_HYDIESEL', 'c_inv'] *= (1. + up['c_inv_bus']) * 0.5 * ((1. + up['c_inv_ic_prop']) + (1. + up['c_inv_e_prop']))
    config['all_data']['Technologies'].loc['BUS_COACH_CNG_STOICH', 'c_inv'] *= (1. + up['c_inv_bus']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['BUS_COACH_FC_HYBRIDH2', 'c_inv'] *=  (1. + up['c_inv_bus']) * (1. + up['c_inv_fc_prop'])

    config['all_data']['Technologies'].loc['CAR_GASOLINE', 'c_inv'] *= (1. + up['c_inv_car']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['CAR_DIESEL', 'c_inv'] *= (1. + up['c_inv_car']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['CAR_NG', 'c_inv'] *= (1. + up['c_inv_car']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['CAR_METHANOL', 'c_inv'] *= (1. + up['c_inv_car']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['CAR_HEV', 'c_inv'] *= (1. + up['c_inv_car']) * 0.5 * ((1. + up['c_inv_ic_prop']) + (1. + up['c_inv_e_prop']))
    config['all_data']['Technologies'].loc['CAR_PHEV', 'c_inv'] *= (1. + up['c_inv_car']) * 0.5 * ((1. + up['c_inv_ic_prop']) + (1. + up['c_inv_e_prop']))
    config['all_data']['Technologies'].loc['CAR_BEV', 'c_inv'] *= (1. + up['c_inv_car']) * (1. + up['c_inv_e_prop'])
    config['all_data']['Technologies'].loc['CAR_FUEL_CELL', 'c_inv'] *= (1. + up['c_inv_car']) * (1. + up['c_inv_fc_prop'])

    config['all_data']['Technologies'].loc['BOAT_FREIGHT_DIESEL', 'c_inv'] *= (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['BOAT_FREIGHT_NG', 'c_inv'] *= (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['BOAT_FREIGHT_METHANOL', 'c_inv'] *= (1. + up['c_inv_ic_prop'])

    config['all_data']['Technologies'].loc['TRUCK_DIESEL', 'c_inv'] *= (1. + up['c_inv_truck']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['TRUCK_FUEL_CELL', 'c_inv'] *= (1. + up['c_inv_truck']) * (1. + up['c_inv_fc_prop'])
    config['all_data']['Technologies'].loc['TRUCK_ELEC', 'c_inv'] *= (1. + up['c_inv_truck']) * (1. + up['c_inv_e_prop'])
    config['all_data']['Technologies'].loc['TRUCK_NG', 'c_inv'] *= (1. + up['c_inv_truck']) * (1. + up['c_inv_ic_prop'])
    config['all_data']['Technologies'].loc['TRUCK_METHANOL', 'c_inv'] *= (1. + up['c_inv_truck']) * (1. + up['c_inv_ic_prop'])

    # Set here the absolute value for the absolute uncertain parameters. It's "=" and not "*="
    config['all_data']['Technologies'].loc['NUCLEAR', 'f_max'] = up['f_max_nuc']

    return config['all_data']