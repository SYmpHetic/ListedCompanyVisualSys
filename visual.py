import pymysql
import matplotlib.pyplot as plt
import pandas as np
from matplotlib.pyplot import cm
from sklearn import manifold, datasets


connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
cursor = connect.cursor()
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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



def getNetprofit():
    sql = "SELECT Net_profit FROM _test_income_statement_202112"
    cursor.execute(sql)
    results_net_profit = cursor.fetchall()
    results_num_net_profit = []
    for i in results_net_profit:
        for j in i:
            results_num_net_profit.append(str2value(j))
    return results_num_net_profit

def getOperatingIncome():
    sql = "SELECT Operating_income FROM _test_income_statement_202112"
    cursor.execute(sql)
    results_o_i = cursor.fetchall()
    results_num_o_i = []
    for i in results_o_i:
        for j in i:
            results_num_o_i.append(str2value(j))
    return results_num_o_i

def getTotalProfit():
    sql = "SELECT Total_profit FROM _test_income_statement_202112"
    cursor.execute(sql)
    results_t_p= cursor.fetchall()
    results_num_t_p = []
    for i in results_t_p:
        for j in i:
            results_num_t_p.append(str2value(j))
    return results_num_t_p

def getName():
    sql = "SELECT Name FROM _test_income_statement_202112"
    cursor.execute(sql)
    results_name = cursor.fetchall()
    return results_name

def getassets():
    sql = "select assets from _test_balance_sheet_202112"
    cursor.execute(sql)
    results_assets = cursor.fetchall()
    results_num_assets = []
    for i in results_assets:
        for j in i:
            results_num_assets.append(str2value(j))
    print(results_num_assets)
    return results_num_assets


def getequity():
    sql = "select equity from _test_balance_sheet_202112"
    cursor.execute(sql)
    results_equity = cursor.fetchall()
    results_num_equity = []
    for i in results_equity:
        for j in i:
            results_num_equity.append(str2value(j))
    print(results_num_equity)
    return results_num_equity

def gettotalcost():
    sql = "SELECT total_cost FROM _test_income_statement_202112"
    cursor.execute(sql)
    results_t_c = cursor.fetchall()
    results_num_t_c = []
    for i in results_t_c:
        for j in i:
            results_num_t_c.append(str2value(j))
    return results_num_t_c

def getliability():
    sql = "SELECT liability FROM _test_balance_sheet_202112"
    cursor.execute(sql)
    results_li = cursor.fetchall()
    results_num_li = []
    for i in results_li:
        for j in i:
            results_num_li.append(str2value(j))
    return results_num_li

def getequlity():
    sql = "SELECT equity FROM _test_balance_sheet_202112"
    cursor.execute(sql)
    results_eq = cursor.fetchall()
    results_num_eq = []
    for i in results_eq:
        for j in i:
            results_num_eq.append(str2value(j))
    return results_num_eq

def visual_income():
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
    cursor = connect.cursor()
    net_profit = getNetprofit()
    operating_income = getOperatingIncome()
    total_profit = getTotalProfit()
    total_cost = gettotalcost()
    asset = getassets()
    name = getName()
    all_result = list(zip(net_profit, operating_income, total_profit, total_cost, asset))
    print(all_result)
    X_tsne = manifold.TSNE(n_components=2, init='random', n_iter=30000, random_state=0, verbose=1).fit_transform(all_result)
    print(X_tsne)

    fig, ax = plt.subplots()
    plt.scatter(X_tsne[:,0],X_tsne[:,1])
    po_annotation = []
    for i in range(len(X_tsne)):
        # 标注点的坐标
        point_x = X_tsne[:,0]
        point_y = X_tsne[:,1]
        point, = plt.plot(point_x, point_y, 'o', c='darkgreen')
        plt.title('t-SNE Visualization')
        # 标注plt.annotate
        annotation = plt.annotate(name[i][0], xy=(X_tsne[i,0], X_tsne[i,1]), size=10)
        # 默认鼠标未指向时不显示标注信息
        annotation.set_visible(False)
        po_annotation.append([point, annotation])

    def on_move(event):
        visibility_changed = False
        for point, annotation in po_annotation:
            should_be_visible = (point.contains(event)[0] == True)

            if should_be_visible != annotation.get_visible():
                visibility_changed = True
                annotation.set_visible(should_be_visible)
        if visibility_changed:
            plt.draw()
    on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
    plt.title("t-SNE结果")
    plt.show()
    cursor.close() # 关闭游标
    connect.close()

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
    plt.xlabel("公司", fontsize=20)
    plt.ylabel("利润率", fontsize=20)
    plt.yticks(fontproperties='Times New Roman', size=10)
    plt.xticks(fontproperties='Times New Roman', size=10)
    for a, b, c in zip(no, profit_ratio, name_list):
        plt.text(a, b, c, ha='center', va='bottom', fontsize=10)
    plt.show()

def visual_assets_liability_ratio():
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
    cursor = connect.cursor()
    assets = getassets()
    liablity = getliability()
    equity = getequity()
    name = getName()
    e_ratio, l_ratio, a_ratio = [], [], []
    for i in assets:
        a_ratio.append(0.5)
    for i in divide(equity, assets):
        e_ratio.append(i/2)
    for j in divide(liablity, assets):
        l_ratio.append(j/2)
    zipped = list(zip(a_ratio,e_ratio,l_ratio))
    print(zipped[0])
    label=['资产', '负债', '权益']
    plt.pie(zipped[0], labels=label, autopct='%1.1f%%')
    plt.title("%s资产结构" % name[0])
    plt.show()

def visual_test(lst):
    sql = "SELECT Net_profit FROM _test_income_statement_202112 WHERE name=\'中集集团\' or name=\'ST沈机\' or name=\'冰轮环境\'"
    cursor.execute(sql)
    results_net_profit = cursor.fetchall()
    results_num_net_profit = []
    for i in results_net_profit:
        for j in i:
            results_num_net_profit.append(str2value(j))

    sql="SELECT Total_cost FROM _test_income_statement_202112 WHERE name=\'中集集团\' or name=\'ST沈机\' or name=\'冰轮环境\'"
    cursor.execute(sql)
    results_total_cost = cursor.fetchall()
    results_num_total_cost = []
    for i in results_total_cost:
        for j in i:
            results_num_total_cost.append(str2value(j))

    name_list = lst
    no = [1,2,3]
    profit_ratio = divide(results_num_net_profit, results_num_total_cost)
    print(profit_ratio)
    plt.bar(no, profit_ratio)
    plt.xlabel("公司", fontsize=20)
    plt.ylabel("利润率", fontsize=20)
    plt.yticks(fontproperties='Times New Roman', size=10)
    plt.xticks(fontproperties='Times New Roman', size=10)
    for a, b, c in zip(no, profit_ratio, name_list):
        plt.text(a, b, c, ha='center', va='bottom', fontsize=10)
    plt.show()

def visual_fix_assets_ratio():
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
    cursor = connect.cursor()
    assets = getassets()

#visual_test()