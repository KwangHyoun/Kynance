import pandas as pd
import pandas_datareader as pdr
from datetime import datetime as dt
# from multiprocessing import Pool
# import qgrid

def get_listed_df():
    # get_KOSPI
    kospi_code_df = \
        pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?marketType=stockMkt&method=download&searchType=13',
                     header=0)[0]
    kospi_code_df["market"] = "kospi"

    # get_KOSDAQ
    kosdaq_code_df = \
        pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?marketType=kosdaqMkt&method=download&searchType=13',
                     header=0)[0]
    kosdaq_code_df["market"] = "kosdaq"

    # get_KONNEX
    kkonex_code_df = \
        pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?marketType=konexMkt&method=download&searchType=13',
                     header=0)[0]
    kkonex_code_df["market"] = "kkonex"

    # Merge KSOPI, KOSDAQ, KONNEX
    code_df = kospi_code_df.append(kosdaq_code_df)
    # Yahoo Finance does not support inquiring about Connex.
    # code_df = (kospi_code_df.append(kosdaq_code_df)).append(kkonex_code_df)

    # Change cloumn name to English
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code', '업종': 'industry', '주요제품': 'major_products', \
                                      '상장일': 'day_of_listing', '결산월': 'settlement_month', '대표자명': 'CEO', \
                                      '홈페이지': 'home_page', '지역': 'location'})

    # convert the stock code into a proper form
    code_df.code = code_df.code.map('{:06d}'.format)

    return code_df

def get_deListed_df():
    # Not written
    return None

# 적절한 형태로 가공
def set_code_df(code_df, attribute=['code', 'market'], mkt_list=['kospi', 'kosdaq'], convert={'kospi': '.KS', 'kosdaq': '.KQ'}):
    code_df = code_df[attribute]  # Processed for 'attribute'
    code_df = code_df.loc[code_df['market'].isin(mkt_list)]  # Processed for 'mkt_list'

    # Check the validity - elements of (List)mkt_list should be equal to keys of (Dict)convert
    for mkt in mkt_list:
        if not mkt in convert.keys():
            print("ERROR - There is no conversion form for %s." % (mkt))
            return 1

    # Convert to match transformation form
    for mkt in mkt_list:
        code_df.loc[code_df['market'] == mkt, 'market'] = convert[mkt]

    return code_df




# Get price histroy of the firm
def get_a_price(start, end, code, source):
    '''
    # 포맷 확인
    '''
    market = code['market']
    code = code['code']
    return pdr.DataReader(code + market, source, start, end)

# Get all price histories listed
def get_prices(start, end=dt.now().strftime('%Y-%m-%d'), market='all', source='yahoo'):
    """
    :param code_df: (Dataframe) has two attributes, 'code' and 'market'.
    :param source: (String) the source of information. ex:'yahoo'
    :param start: (String) Start date format "%Y-%m-%d".
    :param end: (String) End date format "%Y-%m-%d".
    :return:
    """
    results = {}
    # Change 'code_df', if entered, to the entered value.
    code_df = set_code_df(code('all')) if market == 'all' else set_code_df(code('all'), mkt_list=[market])

    for i, row_df in code_df.iterrows():
        results[row_df['code']] = get_a_price(start, end, row_df, source)
        print(row_df['code'], " data collecting...")
    df = pd.concat(results, axis=1)
    return df



