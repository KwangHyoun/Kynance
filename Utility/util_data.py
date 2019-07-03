from _util import *
import time as dt
from multiprocessing import Process

# ---------- RUN WITH IMPORT ----------
code_df = code('all')
yahoo_code_df = purify(code_df)
thread = 16

# ---------- PRICE DATA ----------

# Get price data for Republic of KOREA, Stock market.
    # Suppose that the type of data is 'List'
`
    result = {} # Dictionary to remember price data.

    # 기업들의 기록 형식을 Yahoo finance API에 적절한 형태로 변환
    data = list(map(lambda stock: code_df['code'][list(np.where(code_df==stock)[0])[0]] + \
             code_df['market'][list(np.where(code_df==stock)[0])[0]]\
             , stock_list))

    for index, stock in enumerate(data):
        proc = Process(target=get_a_price, args=(stock, start, end,))
        result.append(proc)
        if (index + 1) % thread == 0 or index == len(data) - 1:
            try: proc.start()
            except: print("ERROR IN PROC!")

    result_df = pd.concat(result, axis=1)
    return result_df



# Convert 'code' attribute into 'name'(Or 'name' into 'code')
def convert(data, intoName=True, maintain = False,):
    # The case that data is 'a' stock.
    if type(data) == str:
        if intoName:
            return code_df['name'][list(np.where(code_df==data)[0])[0]]
        elif not intoName:
            return code_df['code'][list(np.where(code_df==data)[0])[0]]

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



