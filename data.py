import pandas as pd
import pandas_datareader as pdr
from datetime import datetime as dt
# from multiprocessing import Pool
# import qgrid
from util import *


# ---------- PRICE DATA ----------

# Get all price histories listed
def price(start, end=dt.now().strftime('%Y-%m-%d'), market='all', source='yahoo'):

    results = {}
    # Change 'code_df', if entered, to the entered value.
    code_df = purify(code('all')) if market == 'all' else set_code_df(code('all'), mkt_list=[market])

    for i, row_df in code_df.iterrows():
        results[row_df['code']] = get_a_price(start, end, row_df, source)
        print(row_df['code'], " data collecting...")
    df = pd.concat(results, axis=1)
    return df

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
def convert(data, maintain = False, intoName=True, code_df=code('all', attribute=['code', 'name'], listed='both')):

    # Ensure that 'data' is (Dataframe)
    if type(data) == list: data = pd.DataFrame(data, columns=['code'])

    # The case 'code', 'name' column both arrive
    if not maintain:
        if intoName: # Convert 'code' attribute to 'name'
            if 'name' in data.columns:
                print("ERROR - Column 'name' already exists within data.")
                return data
            data = pd.merge(data, code_df[['code', 'name']])
            data = data.drop('code', 1)
        elif not intoName: # Conver 'name' attribute to 'code'
            if 'code' in data.columns:
                print("ERROR - Column 'code' already exists within data.")
                return data
            data = pd.merge(data, code_df[['code', 'name']])
            data = data.drop('name', 1)
    elif maintain:
        # Check ERRORS
        if ('name' in data.columns) and ('code' in data.columns):
            print("ERROR - There are 'code' and 'name' attributes already.")
            return data
        data = pd.merge(data, code_df[['code', 'name']])

    return data



