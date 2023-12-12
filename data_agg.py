import glob
import pandas as pd
import configparser

configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)


def create_initial_dataframe(gw_dir_path='data/gws'): 
    gw_file_list = glob.glob(f'{gw_dir_path}/gw*.csv')
    for gw_file in gw_file_list:
        curr_gw_csv = pd.read_csv(gw_file)
        # Keep this list of columns
        column_names = configParser.get("Data", "pred_column_names").split(',') + configParser.get("Data", "res_column_names").split(',')
        curr_gw_csv = curr_gw_csv[column_names]
        print(curr_gw_csv)

create_initial_dataframe()
