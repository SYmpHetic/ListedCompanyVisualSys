import pymysql
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import time
from matplotlib.pylab import style
style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.float_format', lambda x: '%.5f' % x)
np.set_printoptions(precision=5, suppress=True)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
cursor = connect.cursor()


def str2value(valueStr):
    key = -1
    valueStr = str(valueStr)
    idxOfFu = valueStr.find('-')
    if idxOfFu == 0:
        valueStr = valueStr[1:]
        key = 1
    idxOfYi = valueStr.find('亿')
    idxOfWan = valueStr.find('万')

    if idxOfYi != -1 and idxOfWan != -1:
        return key*-1*int(float(valueStr[:idxOfYi])*1e8 + float(valueStr[idxOfYi+1:idxOfWan])*1e4)+1
    elif idxOfYi != -1 and idxOfWan == -1:
        return key*-1*int(float(valueStr[:idxOfYi])*1e8)+1
    elif idxOfYi == -1 and idxOfWan != -1:
        return key*-1*int(float(valueStr[idxOfYi+1:idxOfWan])*1e4)+1
    elif idxOfYi == -1 and idxOfWan == -1:
        return key*-1*int(float(valueStr))+1

def adf_test(timeseries):  # 平稳性检验
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
       dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

def getcashflow(company):
    sql = "SELECT net_cash_flow FROM cash_flow_"+company
    cursor.execute(sql)
    results_cash_flow= cursor.fetchall()
    results_num_cash_flow = []
    for i in results_cash_flow:
        for j in i:
            results_num_cash_flow.append(str2value(j))
    return results_num_cash_flow


def fun_calDiff(data):
    data_diff = []
    for i in range(len(data) - 1):
        data_diff.append(data[i + 1] - data[i])
    return data_diff

def ts_diff_rvs(data):
    return np.cumsum(data)

def doit(company):
    cash_flow = getcashflow(company)
    D_cash_flow = fun_calDiff(cash_flow)
    adf_test(D_cash_flow)
    res = sm.tsa.ARMA(cash_flow, (1,1)).fit(disp=-1)
    #print(sm.tsa.ARMA(cash_flow,(1,1)).fit(disp=-1).summary())
    ss = sm.tsa.ARMA(cash_flow, (1,1)).fit(disp=-1).plot_predict(0,30)

#doit('603339')
