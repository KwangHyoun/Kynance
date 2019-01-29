# Pynance
#### Python module to help Quant back-test easily

## API Description
### 

Ready to write


## How to use
#### Pynance.data
* Get stock 'code' data
    ```
    Pynance.data.code('kospi')
    Pynance.data.code('kosdaq')
    Pynance.data.code('all')
    ```
 
* Replace company code and company name
    ```
    Pynance.data.replace(df)
    Pynance.data.replace(df, intoName = True)
    Pynance.data.replace(df, intoName = False)
    Pynance.data.replace(df, maintain = True)
    ```
* Get the Price data of a stock
def get_a_price(start, end, code, source):

    ```
    Pynance.data.price('005930.KS','2018-01-01')
    Pynance.data.price('005930', '2018-01-01', end = '2018-12-31')
    Pynance.data.price('삼성전자', '2018-01-01', end = '2018-12-31')
    
    Pynance.data.price(code_list, '2018-01-01')
    Pynance.data.price(code_df, '2018-01-01')
    ```

### Pynance.util