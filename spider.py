from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pymysql
from pymysql.converters import escape_string
import time


def init():
    global browser
    browser = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

def getonecashflow(company):
    init()
    lst=[]
    browser.get('https://data.eastmoney.com/bbsj/xjll/'+company+'.html')
    print("正在获取数据")
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    for td in td_content:
        turn = td.text.replace('\n', '-')
        lst.append(turn)
    print(lst)
    print("数据采集完成")
    browser.quit()
    savetocashflow(lst, company)
    return lst

def getBalancesheet():
    init()
    lst=[]
    browser.get('https://data.eastmoney.com/bbsj/202112/zcfz.html')
    print("正在获取数据")
    hy = browser.find_element(By.ID, "filter_hy")
    ul = hy.find_element(By.CLASS_NAME, "filter_ul")
    specific = ul.find_elements(By.TAG_NAME, "li")
    for li in specific:
        li.click()
    time.sleep(2)
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    lst1 = []
    i = 1
    for td in td_content:
        if(td.text!=str(i)):
            if(td.text!='详细  数据'):
                lst1.append(td.text)
        else:
            i+=1

    gotopage = browser.find_element(By.CLASS_NAME, "gotopage")
    inputbox = gotopage.find_element(By.CLASS_NAME, "ipt")
    inputbox.click()
    inputbox.clear()
    inputbox.send_keys(2)
    submit = gotopage.find_element(By.CLASS_NAME, "btn")
    submit.click()

    time.sleep(2)
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    lst2 = []
    i = 51
    for td in td_content:
        if(td.text!=str(i)):
            if(td.text!='详细  数据'):
                lst2.append(td.text)
        else:
            i+=1
    lst = lst1+lst2
    print(lst)
    print("数据采集完成")
    browser.quit()
    savetobalancesheet(lst)
    return lst

def getIncomeStatement():
    init()
    lst = []
    browser.get('https://data.eastmoney.com/bbsj/202112/lrb.html')
    print("正在获取数据")
    hy = browser.find_element(By.ID, "filter_hy")
    ul = hy.find_element(By.CLASS_NAME, "filter_ul")
    specific = ul.find_elements(By.TAG_NAME, "li")
    for li in specific:
        li.click()
    time.sleep(2)
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    lst1 = []
    i = 1
    for td in td_content:
        if (td.text != str(i)):
            if (td.text != '详细  数据'):
                lst1.append(td.text)
        else:
            i += 1

    gotopage = browser.find_element(By.CLASS_NAME, "gotopage")
    inputbox = gotopage.find_element(By.CLASS_NAME, "ipt")
    inputbox.click()
    inputbox.clear()
    inputbox.send_keys(2)
    submit = gotopage.find_element(By.CLASS_NAME, "btn")
    submit.click()

    time.sleep(2)
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    lst2 = []
    i = 51
    for td in td_content:
        if (td.text != str(i)):
            if (td.text != '详细  数据'):
                lst2.append(td.text)
        else:
            i += 1
    lst = lst1 + lst2
    print(lst)
    print("数据采集完成")
    browser.quit()
    savetoincomestatement(lst)
    return lst

def getCashFlowStatement():
    init()
    lst = []
    browser.get('https://data.eastmoney.com/bbsj/202112/xjll.html')
    print("正在获取数据")
    hy = browser.find_element(By.ID, "filter_hy")
    ul = hy.find_element(By.CLASS_NAME, "filter_ul")
    specific = ul.find_elements(By.TAG_NAME, "li")
    for li in specific:
        li.click()
    time.sleep(2)
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    lst1 = []
    i = 1
    for td in td_content:
        if (td.text != str(i)):
            if (td.text != '详细  数据'):
                lst1.append(td.text)
        else:
            i += 1

    gotopage = browser.find_element(By.CLASS_NAME, "gotopage")
    inputbox = gotopage.find_element(By.CLASS_NAME, "ipt")
    inputbox.click()
    inputbox.clear()
    inputbox.send_keys(2)
    submit = gotopage.find_element(By.CLASS_NAME, "btn")
    submit.click()

    time.sleep(2)
    element = browser.find_element(By.CLASS_NAME, "dataview-body")
    td_content = element.find_elements(By.TAG_NAME, "td")
    lst2 = []
    i = 51
    for td in td_content:
        if (td.text != str(i)):
            if (td.text != '详细  数据'):
                lst2.append(td.text)
        else:
            i += 1
    lst = lst1 + lst2
    print(lst)
    print("数据采集完成")
    browser.quit()
    savetocashflowstatement(lst)

def savetocashflow(lst, company):
    i = 0
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset='utf8')
    cursor = connect.cursor()
    sql="Create table cash_flow_"+company+"(date varchar(255),net_cash_flow varchar(255),net_cash_flow_comp varchar(255),oper_cash_flow varchar(255),oper_cash_flow_ratio varchar(255),sell_cash_flow varchar(255),sell_cash_flow_ratio varchar(255),invest_cash_flow varchar(255),invest_cash_flow_ratio varchar(255),invest_profit varchar(255),invest_profit_ratio varchar(255),fix_assets_cash_flow varchar(255),fix_assets_cash_flow_ratio varchar(255),finance_cash_flow varchar(255),finance_cash_flow_ratio varchar(255),public_date varchar(255))"
    cursor.execute(sql)
    for i in range(0, 28):
        sql = "insert into cash_flow_"+company+"(date,net_cash_flow,net_cash_flow_comp,oper_cash_flow,oper_cash_flow_ratio," \
              "sell_cash_flow,sell_cash_flow_ratio,invest_cash_flow,invest_cash_flow_ratio,invest_profit," \
              "invest_profit_ratio,fix_assets_cash_flow,fix_assets_cash_flow_ratio,finance_cash_flow," \
              "finance_cash_flow_ratio,public_date)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\','%s\'," \
              "\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" \
                  % (escape_string(lst[i * 16]), escape_string(lst[i * 16 + 1]), escape_string(lst[i * 16 + 2]),
                     escape_string(lst[i * 16 + 3]), escape_string(lst[i * 16 + 4]), escape_string(lst[i * 16 + 5]),
                     escape_string(lst[i * 16 + 6]), escape_string(lst[i * 16 + 7]), escape_string(lst[i * 16 + 8]),
                     escape_string(lst[i * 16 + 9]), escape_string(lst[i * 16 + 10]), escape_string(lst[i * 16 + 11]),
                     escape_string(lst[i * 16 + 12]), escape_string(lst[i * 16 + 13]), escape_string(lst[i * 16 + 14]),
                     escape_string(lst[i * 16 + 15]))
        print(sql)
        cursor.execute(sql)
    connect.commit()

def savetocashflowstatement(lst):
    i = 0
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset='utf8')
    cursor = connect.cursor()
    for i in range(0, 63):
        sql = "insert into cashflow_statement_202112(No,Name,Net_cashflow ,Cashflow_Comp,Operating_cashflow,Op_ratio,Invest_cashflow,Invest_ratio,Finance_cashflow,Finance_ratio,Public_date)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\','%s\',\'%s\',\'%s\',\'%s\')" \
                  % (escape_string(lst[i * 11]), escape_string(lst[i * 11 + 1]), escape_string(lst[i * 11 + 2]),
                     escape_string(lst[i * 11 + 3]), escape_string(lst[i * 11 + 4]), escape_string(lst[i * 11 + 5]),
                     escape_string(lst[i * 11 + 6]), escape_string(lst[i * 11 + 7]), escape_string(lst[i * 11 + 8]),
                     escape_string(lst[i * 11 + 9]), escape_string(lst[i * 11 + 10]))
        print(sql)
        cursor.execute(sql)
    connect.commit()

def savetoincomestatement(lst):
    i = 0
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset='utf8')
    cursor = connect.cursor()
    for i in range(0, 63):
            sql = "insert into _test_income_statement_202112(No,Name,Net_profit,Porfit_Comp,Operating_income,Income_Comp,Operating_cost,Selling_cost,Admin_cost,Financial_cost,Total_cost,Operating_profit,Total_profit,Public_date)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\','%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" \
                  % (escape_string(lst[i * 14]), escape_string(lst[i * 14 + 1]), escape_string(lst[i * 14 + 2]),
                     escape_string(lst[i * 14 + 3]),
                     escape_string(lst[i * 14 + 4]), escape_string(lst[i * 14 + 5]), escape_string(lst[i * 14 + 6]),
                     escape_string(lst[i * 14 + 7]),
                     escape_string(lst[i * 14 + 8]), escape_string(lst[i * 14 + 9]), escape_string(lst[i * 14 + 10]),
                     escape_string(lst[i * 14 + 11]),
                     escape_string(lst[i * 14 + 12]), escape_string(lst[i * 14 + 13]))
            print(sql)
            cursor.execute(sql)
    connect.commit()


def savetobalancesheet(lst):
    i = 0
    connect = pymysql.connect(host='localhost', user='root', db='financial_statement',
                              charset='utf8')
    cursor = connect.cursor()
    for i in range(0, 63):
        sql = "insert into _test_balance_sheet_202112(No,Name,cash ,account_receivable ,inventory ,assets ,assets_comp," \
              "account_payable ,Deposit_received ,liability ,liability_comp ,AL_ratio ,equity ,public_date )values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\','%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" \
              % (escape_string(lst[i * 14]), escape_string(lst[i * 14 + 1]), escape_string(lst[i * 14 + 2]),
                 escape_string(lst[i * 14 + 3]),
                 escape_string(lst[i * 14 + 4]), escape_string(lst[i * 14 + 5]), escape_string(lst[i * 14 + 6]),
                 escape_string(lst[i * 14 + 7]),
                 escape_string(lst[i * 14 + 8]), escape_string(lst[i * 14 + 9]), escape_string(lst[i * 14 + 10]),
                 escape_string(lst[i * 14 + 11]),
                 escape_string(lst[i * 14 + 12]), escape_string(lst[i * 14 + 13]))
        print(sql)
        cursor.execute(sql)
    connect.commit()


#savetocashflow(list)
