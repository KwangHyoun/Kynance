import pandas as pd
import pandas_datareader as pdr
from datetime import datetime as dt
# from multiprocessing import Pool
# import qgrid
from util import *

def code(market, attribute=['code', 'name', 'market'], listed=True):
    # print("Collecting code data for %s as requested form" % ("KOSPI & KOSDAQ" if market == 'all' else market.upper()))
    # ERROR CHECK
    if market not in ['kospi', 'kosdaq', 'all']:
        print("ERROR - Invalid value of market")
        return None

    # Get code data
    code_df = get_listed_df()   

    # listed에 따라 데이터 추가
    if not listed:
        code_df = get_deListed_df()
    elif listed == 'both':
        code_df.append(get_deListed_df())

    # Eliminate unnecessary attributes
    code_df = code_df[attribute]

    # Eliminate unnecessary records
    if market == 'all':
        pass  # 'all' - Kospi & Kosdaq
    else:
        code_df = code_df[code_df['market'] == market]  # Specific market

    return code_df

# Convert 'code' attribute into 'name'(Or 'name' into 'code')
def convert(dataframe, intoName=True, code_df=code('all', attribute=['code', 'name'], listed='both')):
    if intoName:
        if 'name' in dataframe.columns:
            print("ERROR - Column 'name' already exists within data.")
            return dataframe
        dataframe = pd.merge(dataframe, code_df[['code', 'name']])
        dataframe = dataframe.drop('code', 1)
    elif not intoName:
        if 'code' in dataframe.columns:
            print("ERROR - Column 'code' already exists within data.")
            return dataframe
        dataframe = pd.merge(dataframe, code_df[['code', 'name']])
        dataframe = dataframe.drop('name', 1)

    return dataframe
