import glob
import pandas as pd
import numpy as np
import configparser
from tqdm import tqdm
tqdm.pandas()

configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)


def create_initial_dataframe(gw_dir_path='data/gws'): 
    gw_dfs = []
    gw_file_list = glob.glob(f'{gw_dir_path}/gw*.csv')
    for gw_file in gw_file_list:
        curr_gw_csv = pd.read_csv(gw_file)
        # Keep this list of columns
        column_names = configParser.get("Data", "pred_column_names").split(',') + configParser.get("Data", "res_column_names").split(',')
        curr_gw_csv = curr_gw_csv[column_names]
        curr_gw_csv['gw'] = int((gw_file.removeprefix(f"{gw_dir_path}\\gw")).removesuffix(".csv"))
        gw_dfs.append(curr_gw_csv)

    agg_df = pd.concat(gw_dfs, ignore_index=True)
    return agg_df

init_df = create_initial_dataframe()

print(init_df)

def preprocess_df(df):
    # First get total stats so far this season
    total_stat_list = configParser.get("Preprocessing", "total_stat_list").split(',')



    for stat in total_stat_list:
        def tot_stat_helper(df_row):
            temp_df = df.copy()
            temp_df = temp_df[temp_df["name"] == df_row["name"]]
            temp_df = temp_df[temp_df["gw"] < int(df_row["gw"])]
            return np.sum(temp_df[stat])
        
        df[f'tot_{stat}'] = df.progress_apply(tot_stat_helper, axis=1)

    min_starts = int(configParser.get("Preprocessing", "min_starts"))
    df = df[df['tot_starts'] >= min_starts]

    print(df['starts'])
    
    return df 

preprocessed_df = preprocess_df(init_df)
print(preprocessed_df)
