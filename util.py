import pandas as pd
import pandas_datareader as pdr
# from multiprocessing import Pool


# ---------- PRICE DATA ----------

# Get price data of the firm
def get_a_price(start, end, code, source):
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


def purify(data, attribute = ['code', 'market'], convertRull = {'market' : {'kospi': '.KS', 'kosdaq': '.KQ'}}):
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




'''
        

    data = data[attribute]
    data = data.loc[data['market'].isin(mktList)]





def set_code_df(code_df, attribute=['code', 'market'], mkt_list=['kospi', 'kosdaq'], rull=
    code_df = code_df[attribute]  # Processed for 'attribute'
    code_df = code_df.loc[code_df['market'].isin(mkt_list)]  # Processed for 'mkt_list'

    # Check the validity - elements of (List)mkt_list should be equal to keys of (Dict)convert
    for mkt in mkt_list:
        if  mkt not in rull.keys():
            print("ERROR - There is no conversion form for %s." % (mkt))
            return 1

    # Convert to match transformation form
    for mkt in mkt_list:
        code_df.loc[code_df['market'] == mkt, 'market'] = rull[mkt]

    return code_df

'''
