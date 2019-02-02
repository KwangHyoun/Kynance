import numpy as np
import pandas as pd
import pandas_datareader as pdr
# from multiprocessing import Pool


# ---------- PRICE DATA ----------

# Get price data of the firm
def get_a_price(code, start, end, source='yahoo'):
    try:
        return pdr.DataReader(code, source, start, end)
    except:
        return False


# ---------- CODE DATA ----------

# Get listed code data
def get_codeListed_df(source = 'KR', target = 'stock'):
    # if source == '미국시장'
    # elif source == '중국시장'
    # elif source ==

    if source == 'KR':
        if target == 'stock':
            return get_KOR_stockListed_df()
        elif target == 'ETF':
            # Not yet created
            pass

    return False

# Get delisted code data
def get_codeDelisted_df(source = 'KR', target = 'stock'):
    # Not yet created
    return None

# Get listed data on KRX, stock.
def get_KOR_stockListed_df(target = ['kospi', 'kosdaq']):
    # Yahoo Finance does not support inquiring about Konnex.
    df_dict = {}

    # get_KOSPI
    kospi_code_df = \
        pd.read_html(
            'http://kind.krx.co.kr/corpgeneral/corpList.do?marketType=stockMkt&method=download&searchType=13',
            header=0)[0]
    kospi_code_df["market"] = "kospi"
    df_dict['kospi'] = kospi_code_df

    # get_KOSDAQ
    kosdaq_code_df = \
        pd.read_html(
            'http://kind.krx.co.kr/corpgeneral/corpList.do?marketType=kosdaqMkt&method=download&searchType=13',
            header=0)[0]
    kosdaq_code_df["market"] = "kosdaq"
    df_dict['kosdaq'] = kosdaq_code_df

    # get_KONNEX
    kkonex_code_df = \
        pd.read_html(
            'http://kind.krx.co.kr/corpgeneral/corpList.do?marketType=konexMkt&method=download&searchType=13',
            header=0)[0]
    kkonex_code_df["market"] = "kkonex"
    df_dict['konnex'] = kkonex_code_df

    # Merge
    target = list_caseConverter(target)
    data = pd.DataFrame
    for mkt in target:
        data = data.append(df_dict[mkt])


    # Change cloumn name to English
    data = data.rename(columns={'회사명': 'name', '종목코드': 'code', '업종': 'industry', '주요제품': 'major_products', \
                                      '상장일': 'day_of_listing', '결산월': 'settlement_month', '대표자명': 'CEO', \
                                      '홈페이지': 'home_page', '지역': 'location'})

    # convert the stock code into a proper form
    data.code = data.code.map('{:06d}'.format)

    return data

# Get code data easily
def code(market, attribute=['code', 'name', 'market'], listed=True):
    # print("Collecting code data for %s as requested form" % ("KOSPI & KOSDAQ" if market == 'all' else market.upper()))
    # ERROR CHECK
    if market not in ['kospi', 'kosdaq', 'all']:
        print("ERROR - Invalid value of market")
        return None

    # Get code data
    code_df = get_codeListed_df()

    # listed에 따라 데이터 추가
    if not listed:
        code_df = get_codeDelisted_df()
    elif listed == 'both':
        code_df.append(get_codeListed_df())

    # Eliminate unnecessary attributes
    code_df = code_df[attribute]

    # Eliminate unnecessary records
    if market != 'all':
        code_df = code_df[code_df['market'] == market]  # Specific market

    return code_df


# ---------- TOOLS ----------

# Set all elements in (List)data lower(or upper) capital.
def list_caseConverter(data, toLower = True):
    if not type(data) == list:
        print("Argument type ERROR in Kynance.util.modifyCapital_list()")
        return None

    for index, value in data:
        if type(value) == str:
            if toLower: data[index] = value.lower()
            elif not toLower: data[index] = value.upper()

    return data

def purify(data, attribute = ['code', 'name', 'market'], convertRull = {'market' : {'kospi': '.KS', 'kosdaq': '.KQ'}}):
    # Check the validity

    # Check converted data has meaning - attribute
    for col in convertRull.keys():
        if col not in attribute:
            print("WARNING - %s is not in attribute. There's possibility of data loss." % (col))

    # Modify data by convertRull
    for col in convertRull.keys():
        for before in convertRull[col].keys():
            data.loc[data[col] == before, col] = convertRull[col][before]

    # Drop columns except in (List)attribute
    data = data[attribute]

    return data