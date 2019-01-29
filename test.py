from data import *

# Test cost()
kospi = code('kospi')
kosdaq = code('kosdaq')
mkt = code('all')

# Test convert()
kospi = convert(set_code_df(kospi))
print(kospi)