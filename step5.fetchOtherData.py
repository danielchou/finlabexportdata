# 找出提早公布月營收資料的股票
import finlab
finlab.login(open("config.txt", "r").read())

from finlab import data
df = data.get('monthly_revenue:當月營收')
import _beowFmt as fm 
import pandas as pd
# pd.set_option('display.expand_frame_repr', False)


dfm = df.tail(1).to_period('M')

not_nan_columns = dfm.columns[dfm.notna().all()]

print(not_nan_columns)
ss=''
for c in not_nan_columns:
    ss += f'{c},'
fm.write_LogFile(f"data/json/monthlyRevenue.json", f"[{ss[:-1]}]") 
#####################################################################################
