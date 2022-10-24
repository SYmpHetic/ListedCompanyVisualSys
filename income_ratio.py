import pymysql
from visual import getNetprofit, gettotalcost, getName
import matplotlib.pyplot as plt

def divide(a,b):
    c=[]
    for i in range(0, len(a)):
        c.append(a[i]/b[i])
    return c


def visual_income_ratio():
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
    cursor = connect.cursor()
    net_profit = getNetprofit()
    total_cost = gettotalcost()
    name = getName()
    name_list = []
    no=[]
    a=1
    for i in name:
        no.append(a)
        name_list.append(name[a-1][0])
        a+=1
    profit_ratio = divide(net_profit, total_cost)
    print(profit_ratio)
    plt.bar(no, profit_ratio)
    for a, b, c in zip(no, profit_ratio, name_list):
        plt.text(a, b, c, ha='center', va='bottom', fontsize=8)
    plt.show()
