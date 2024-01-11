# %%
#前置作業準備，只要一次!!
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json
import _beowFmt as fm 

from finlab import data
import os

rootpath= "D:/project/finlabexportdata/"

yesterday = fm.getLastFileDate(f"{rootpath}/volumeData", "ma_")

df5k = pd.read_json(f"{rootpath}paras/mapping5K.json")
dfv = pd.read_csv(f"{rootpath}volumeData/ma_{yesterday}.csv")
dfv["id"] = dfv["id"].astype("string")
# dfv = dfv.drop(columns=['close'])
#print(dfv[dfv["id"] == "3265"])

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}

url4 = "https://www.wantgoo.com/investrue/all-alive"
r3 = requests.get(url4, headers = headers).content
soup = BeautifulSoup(r3, "html.parser")
rr3 = soup.prettify()
dfn = pd.read_json(rr3)
dfn = dfn[(dfn["id"]>="1101") & (dfn["id"]<="9999") & (dfn["id"].str.len() == 4)]
dfn = dfn.drop(columns=['type','country','url', 'industries'])
dfn["id"] = dfn["id"].astype("string")

def comp_stockName(r):
    id, name = r["id"], r["name"]
    return f"{id},{name}"

dfn["comp"] = dfn.apply(comp_stockName, axis = 1)
stockNameStr = ""
for c in dfn["comp"].tolist():
    stockNameStr += f"{c}\n"
fm.write_LogFile(f"{rootpath}paras/股票名稱.csv", stockNameStr)  

### 計算量比參數 ###
import time
def getRate5K():
    localtime = time.localtime()
    nowTime = time.strftime("%H:%M", localtime)
    Rate5k = df5k[(df5k["e"] >= nowTime) & (df5k["b"] <= nowTime)]["w"].values[0]  #五分K量比預估放大參數 
    print(f"目前時間：{nowTime},預估量放大係數:{Rate5k}")
    return Rate5k

# print(getRate5K())

from IPython.display import display

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', 500)
pd.set_option("expand_frame_repr", False)
pd.set_option('display.width', 180)                       # 设置打印宽度(**重要**)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
}

r = requests.get("https://www.wantgoo.com/investrue/all-quote-info", headers = headers).content
soup = BeautifulSoup(r, "html.parser")
rr = soup.prettify()
df = pd.read_json(rr)
df = df.drop(columns=['tradeDate', 'time','millionAmount'])
df["id"] = df["id"].astype("string")
df = pd.merge(df, dfn, left_on="id", right_on="id")  ## 結合股票名稱
df["float"] = df["close"].astype("float")
df["amp"] = ((df["close"] - df["previousClose"])/df["previousClose"] * 100).round(2)
df["jump"] = df["open"] - df["previousClose"]
df["jumpRate"] = (df["jump"] / df["open"] * 100).round(2)
df = df[(df["id"]>="1101") & (df["id"]<="9999") & (df["id"].str.len() == 4)].sort_values("jumpRate", ascending=False)
# df.info()
# print(df.head(50))


######################################################################################################################################
r2 = requests.get("https://www.wantgoo.com/stock/all-turnover-rates", headers = headers).content
soup = BeautifulSoup(r2, "html.parser")
rr2 = soup.prettify()
dfa = pd.read_json(rr2)
# print(dfv)

dfa["investrueId"] = dfa["investrueId"].astype("string")
dfb = pd.merge(df, dfa, left_on="id", right_on="investrueId")
dfb = dfb.drop(columns=['investrueId'])          
dfb["周轉率"] = dfb["value"].round(2) #周轉率

dfc = pd.merge(dfb, dfv, left_on="id", right_on="id")
dfc["預估量"] = (dfc["volume"] * getRate5K()).astype(int)        ##預估量
dfc["量比"] = (dfc["預估量"] / dfc["yVolume"]).round(2)
dfc["週量比"] = (dfc["預估量"] / dfc["ma5"]).round(2)
dfc["月量比"] = (dfc["預估量"] / dfc["ma20"]).round(2)
dfc["季量比"] = (dfc["預估量"] / dfc["ma60"]).round(2)
dfc["半年量比"] = (dfc["預估量"] / dfc["ma120"]).round(2)
dfc["年量比"] = (dfc["預估量"] / dfc["ma240"]).round(2)
dfc["量比周轉"] = ((dfc["量比"] + dfc["value"]) / 2).round(4)
dfc.replace([np.inf, -np.inf], 0, inplace=True)
dfc["json"] = dfc.apply(fm.fmt_all_infor_stock, axis=1)
print(dfc)

## 策略1:找出今天開盤跳空
dfc1 = dfc[ (dfc["low"] > dfc["yHigh"]) & (dfc["close"] > dfc["yHigh"])] # & (dfc["close"] >= dfc["open"]) ]  # & (dfc["yVolume"] > 1800) ] 

## 策略2:找出周轉率高  
## 20230907:預估量大於5000張
## 20230907:振福小於4%
dfc2 = dfc[ (dfc["yVolume"] > 400) & (dfc["close"] < 400) & (dfc["amp"] > 0.3) & (dfc["量比"] > 1.5) & (dfc["預估量"] > 2000 ) ] # & (dfc["周轉率"] > 1)]

df1a = dfc1.loc[:, ["id","market","name","yClose","low","previousClose","open","close","jump","amp","jumpRate","yVolume","預估量","量比","週量比","月量比","季量比","半年量比","年量比","周轉率","量比周轉"]].sort_values("半年量比", ascending=False)
df2a = dfc2.loc[:, ["id","market","name","yClose","low","previousClose","open","close","jump","amp","jumpRate","yVolume","預估量","量比","週量比","月量比","季量比","半年量比","年量比","周轉率","量比周轉"]].sort_values("周轉率", ascending=False)
# df2a["json"] = df2a.apply(fm.fmt_all_infor_stock, axis=1)

s1 ,s2 ,s3, o_nowDate, o_nowTime = '', '', '', time.strftime("%Y%m%d", time.localtime()) , time.strftime("%Y%m%d_%H%M", time.localtime())

df3 = df1a["id"].tolist()
for d in df3:
  s1 += f"{d}.TW,"
fm.write_LogFile(f"{rootpath}xq_import/趨勢扭轉{o_nowDate}_跳空.csv", s1)

df4 = df2a["id"].tolist()
#for d in [item for item in df4 if item not in df3]:         # PROD
for d in df4:
  s2 += f"{d}.TW,"
fm.write_LogFile(f"{rootpath}xq_import/量價型態{o_nowTime}_量比大.csv", s2)

df5 = dfc["json"].tolist()
for d in df5:
  s3 += "{" + d + "},"
s3 = s3[:-1]
fm.write_LogFile(f"{rootpath}data/json/all_info.json", f"[{s3}]")
