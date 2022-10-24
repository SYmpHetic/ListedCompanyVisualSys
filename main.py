import tkinter
from tkinter import *
import pymysql
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter
import spider
from PIL import ImageTk
from PIL import Image
import tkinter.messagebox as msgbox
import ARMA
import visual

connect = pymysql.connect(host='localhost', user='root', db='financial_statement', charset="utf8")
cursor = connect.cursor()


def str2value(valueStr):
    valueStr = str(valueStr)
    idxOfYi = valueStr.find('亿')
    idxOfWan = valueStr.find('万')
    if idxOfYi != -1 and idxOfWan != -1:
        return int(float(valueStr[:idxOfYi])*1e8 + float(valueStr[idxOfYi+1:idxOfWan])*1e4)+1
    elif idxOfYi != -1 and idxOfWan == -1:
        return int(float(valueStr[:idxOfYi])*1e8)+1
    elif idxOfYi == -1 and idxOfWan != -1:
        return int(float(valueStr[idxOfYi+1:idxOfWan])*1e4)+1
    elif idxOfYi == -1 and idxOfWan == -1:
        return int(float(valueStr))+1

def get_img(filename, width, height):
    im = Image.open(filename).resize((width, height))
    im = ImageTk.PhotoImage(im)
    return im


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('财务报表数据可视化系统')
        self.root.geometry('1280x720')
        self.root.resizable(False, False)
        self.startPageshow()
        self.root.mainloop()

    def background(self):
        self.canvas_root = tkinter.Canvas(self.root, width=1280, height=720)
        self.im_root = get_img('preview.png', 1280, 720)
        self.canvas_root.create_image(640, 360, image=self.im_root)
        self.canvas_root.place(x=0, y=0, relwidth=1, relheight=1)


    def startPageshow(self):
        self.background()
        self.title = Label(self.root, text='财务报表数据可视化系统', font=('华文新魏', 32), width=20, height=5)
        self.title.pack()
        self.btnstart = Button(self.root, text='开始', command=lambda: [self.title.destroy(), self.btnstart.destroy(),
                                                                      self.mainPageshow()], width=20, height=3)
        self.btnstart.place(x=555, y=400)

    def mainPageshow(self):
        self.background()
        self.title = Label(self.root, text='财务报表数据可视化系统主菜单', font=('华文新魏', 20), width=25, height=5)
        self.title.pack()
        self.btncollect = Button(self.root, text='采集数据', width=20, height=3, command=lambda:[self.title.destroy(), self.btncollect.pack_forget(), self.btnshow.pack_forget(), self.btnvisual.pack_forget(), self.btnpredict.pack_forget(),
                                                                      self.getdataPage()])
        self.btncollect.place(x=555, y=240)
        self.btnshow = Button(self.root, text='数据导出', width=20, height=3, command=lambda:[self.title.destroy(),self.btncollect.pack_forget(), self.btnshow.pack_forget(), self.btnvisual.pack_forget(), self.btnpredict.pack_forget(),
                                                                      self.showdataPage()])
        self.btnshow.place(x=555, y=320)
        self.btnvisual = Button(self.root, text='数据可视化', width=20, height=3, command=lambda:[self.title.destroy(),self.btncollect.pack_forget(), self.btnshow.pack_forget(), self.btnvisual.pack_forget(), self.btnpredict.pack_forget(),
                                                                      self.visualPage()])
        self.btnvisual.place(x=555, y=400)
        self.btnpredict = Button(self.root, text='数据预测', width=20, height=3, command=lambda:[self.title.destroy(),self.btncollect.pack_forget(), self.btnshow.pack_forget(), self.btnvisual.pack_forget(), self.btnpredict.pack_forget(),
                                                                      self.predictPage()])
        self.btnpredict.place(x=555, y=480)
        self.btnExit = Button(self.root, text='退出', width=20, height=3,
                                 command=lambda: [self.root.destroy()])
        self.btnExit.place(x=555, y=560)

    def getdataPage(self):
        self.background()
        self.title = Label(self.root, text='采集数据', font=('华文新魏', 20), width=25, height=5)
        self.title.pack()
        self.btnspiderbalance = Button(self.root, text='爬取资产负债表', width=15, height=3, command=lambda: [spider.getBalancesheet()])
        self.btnspiderbalance.place(x=580, y=300)
        self.btnspidercash = Button(self.root, text='爬取现金流量表', width=15, height=3, command=lambda: [self.chooseCashflow()] )
        self.btnspidercash.place(x=580, y=400)
        self.btnspiderincome = Button(self.root, text='爬取利润表', width=15, height=3, command=lambda: [spider.getIncomeStatement(), spider.savetoincomestatement(), msgbox.showinfo("成功", "利润表采集完成")])
        self.btnspiderincome.place(x=580, y=500)
        self.btnback = Button(self.root, text='返回', width=15, height=3, command=lambda: [self.title.destroy(), self.btnspiderincome.pack_forget(), self.btnspidercash.pack_forget(), self.btnspiderbalance.pack_forget(), self.btnback.pack_forget(),
                                                                      self.mainPageshow()])
        self.btnback.place(x=580, y=600)

    def showdataPage(self):
        self.background()
        self.title = Label(self.root, text='查看报表数据', font=('华文新魏', 20), width=25, height=5)
        self.title.pack()
        self.btnexporttoexcel = Button(self.root, text='导出到文件', width=15, height=3, command=lambda: [self.chooseexcel()]) # msgbox.showinfo("成功", "成功输出到excel")
        self.btnexporttoexcel.place(x=580, y=250)
        self.btnback = Button(self.root, text='返回', width=15, height=3,
                              command=lambda: [self.title.destroy(),
                                               self.btnback.pack_forget(),
                                               self.mainPageshow()])
        self.btnback.place(x=580, y=450)

    def visualPage(self):
        self.background()
        self.title = Label(self.root, text='报表数据可视化', font=('华文新魏', 20), width=25, height=5)
        self.title.pack()
        self.btnIncomeRatio = Button(self.root, text='比较利润率', width=20, height=3, command=lambda:[self.choose2()])
        self.btnIncomeRatio.place(x=580, y=250)
        self.btnAssetsLibRatio = Button(self.root, text='资产负债比', width=20, height=3, command=lambda:[self.choose()])
        self.btnAssetsLibRatio.place(x=580, y=350)
        self.btntSNE = Button(self.root, text='t-SNE降维', width=20, height=3, command=lambda: [self.choosetsne()])
        self.btntSNE.place(x=580, y=450)
        self.btnback = Button(self.root, text='返回', width=20, height=3, command=lambda: [self.title.destroy(), self.btnIncomeRatio.pack_forget(),
                                                                                         self.btnAssetsLibRatio.pack_forget(), self.btntSNE.pack_forget(),
                                                                                         self.btnback.pack_forget(), self.mainPageshow()])
        self.btnback.place(x=580, y=550)

    def predictPage(self):
        self.background()
        self.title = Label(self.root, text='数据预测', font=('华文新魏', 20), width=25, height=5)
        self.title.pack()
        self.btnPredictCashFlow = Button(self.root, text='预测季度现金流', width=20, height=3, command=lambda:[self.choosepre()])
        self.btnPredictCashFlow.place(x=580, y=300)
        self.btnback = Button(self.root, text="返回", width=20, height=3, command=lambda:[self.title.destroy(), self.btnPredictCashFlow.pack_forget(),
                                                                                        self.btnback.pack_forget(), self.mainPageshow()])
        self.btnback.place(x=580, y=400)

    def choosetsne(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择-tSNE降维')
        child['height'] = 450
        child['width'] = 400
        child.resizable(0, 0)
        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        CheckVar3 = IntVar()
        CheckVar4 = IntVar()
        CheckVar5 = IntVar()
        C1 = Checkbutton(child, text="净利润", variable=CheckVar1, onvalue=1, offvalue=0, height=5, width=20)
        C2 = Checkbutton(child, text="营业收入", variable=CheckVar2, onvalue=1, offvalue=0, height=5, width=20)
        C3 = Checkbutton(child, text="税前利润", variable=CheckVar3, onvalue=1, offvalue=0, height=5, width=20)
        C4 = Checkbutton(child, text="总成本", variable=CheckVar4, onvalue=1, offvalue=0, height=5, width=20)
        C5 = Checkbutton(child, text="资产", variable=CheckVar5, onvalue=1, offvalue=0, height=5, width=20)
        C1.place(x=100,y=0)
        C2.place(x=100,y=80)
        C3.place(x=100,y=160)
        C4.place(x=100,y=240)
        C5.place(x=100,y=320)
        btny = Button(child, text="确定", command=lambda: visual.visual_income())
        btny.place(x=100, y=400)
        btnn = Button(child, text="取消", command=lambda: child.destroy())
        btnn.place(x=300, y=400)

    def chooseCashflow(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择-采集现金流')
        child.geometry('300x100')
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        btn1 = Button(child, text="采集现金流量表", command=lambda: [spider.getCashFlowStatement()])
        btn1.pack()
        btn2 = Button(child, text="采集单公司历史现金流量表", command=lambda: [self.chooseCompany(), child.destroy()])
        btn2.pack()

    def chooseCashflow2(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择-导出现金流量表')
        child['height'] = 100
        child['width'] = 200
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        btn1 = Button(child, text="现金流量表", command=lambda: [self.exportdatatoexcel("Cashflow_statement_202112","_test_Cashflow_statement_202112"),
                                                            msgbox.showinfo("成功", "成功输出到excel")])
        btn1.place(x=50, y=20)
        btn2 = Button(child, text="单公司历史现金流量表", command=lambda: [self.chooseCompany2(), child.destroy()])
        btn2.place(x=20, y=70)

    def chooseCompany(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择公司-采集现金流')
        child['height'] = 150
        child['width'] = 500
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        label = tkinter.Label(child, text='请输入要采集的公司编号:')
        label.place(x=1, y=17)
        # 弹出输入对话框请获取相应的值
        digit_str = tkinter.StringVar()
        entry = tkinter.Entry(child, textvariable=digit_str)
        entry.place(x=250, y=17)
        btny = Button(child, text="确定", command=lambda: spider.getonecashflow(entry.get()))
        btny.place(x=100, y=100)
        btnn = Button(child, text="取消", command=lambda :child.destroy())
        btnn.place(x=400, y=100)

    def chooseCompany2(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择公司-导出现金流量表')
        child['height'] = 150
        child['width'] = 500
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        label = tkinter.Label(child, text='请输入要导出的公司编号:')
        label.place(x=1, y=17)
        # 弹出输入对话框请获取相应的值
        digit_str = tkinter.StringVar()
        entry = tkinter.Entry(child, textvariable=digit_str)
        entry.place(x=250, y=17)
        btny = Button(child, text="确定", command=lambda:[self.exportdatatoexcel("Cashflow_statement_"+entry.get(), "_test_Cashflow_statement_"+entry.get(),
                                                                              msgbox.showinfo("成功", "成功输出到excel"))])
        btny.place(x=100, y=100)
        btnn = Button(child, text="取消", command=lambda :child.destroy())
        btnn.place(x=400, y=100)

    def choosepre(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择公司-预测现金流')
        child['height'] = 150
        child['width'] = 500
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        label = tkinter.Label(child, text='请输入要预测的公司编号:')
        label.place(x=1, y=17)
        # 弹出输入对话框请获取相应的值
        digit_str = tkinter.StringVar()
        entry = tkinter.Entry(child, textvariable=digit_str)
        entry.place(x=250, y=17)
        btny = Button(child, text="确定", command=lambda: [ARMA.doit(entry.get())])
        btny.place(x=100, y=100)
        btnn = Button(child, text="取消", command=lambda: child.destroy())
        btnn.place(x=400, y=100)

    def chooseexcel(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择导出数据')
        child['height'] = 200
        child['width'] = 200
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        btn1 = Button(child, text="资产负债表", width=8, command=lambda:[self.exportdatatoexcel("Balance_sheet_202112", "_test_Balance_sheet_202112"), msgbox.showinfo("成功", "成功输出到excel")])
        btn1.place(x=80, y=30)
        btn2 = Button(child, text="利润表", width=8, command=lambda:[self.exportdatatoexcel("Income_statement_202112", "_test_Income_statement_202112"), msgbox.showinfo("成功", "成功输出到excel")])
        btn2.place(x=80, y=90)
        btn3 = Button(child, text="现金流量表", width=8, command=lambda:self.chooseCashflow2())
        btn3.place(x=80, y=150)

    # def showalldata(self):
    #     sql = "SELECT * FROM `_test_income_statement_202112`"
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     results_num = []
    #     for i in range(0,48):
    #         for j in range(0,13):
    #             results_num.append(results[i][j])
    #     self.text = Text(self.root, width=300)
    #     self.text.insert(END, '股票代码\t\t股票简称\t\t净利润(元)\t\t净利润同比(%)\t\t营业总收入(元)\t\t营业总收入同比(%)\t\t营业支出\t\t销售费用\t\t管理费用\t\t财务费用\t\t营业总支出\t\t营业利润\t\t利润总额\n')
    #     count = 0
    #     for i in results_num:
    #         self.text.insert(END, i)
    #         self.text.insert(END, '\t\t')
    #         count += 1
    #         if(count == 13):
    #             self.text.insert(END, '\n')
    #             count = 0;
    #     self.text.pack()

    # def visualdata(self):
    #     sql = "SELECT `Total_profit` FROM `_test_income_statement_202112`"
    #     cursor.execute(sql)
    #     results = cursor.fetchall()
    #     result_num = []
    #     for i in range(0, 48):
    #         result_num.append(str2value(results[i][0]))
    #     a = np.linspace(1, 48, 48)
    #     plt.plot(a, result_num)
    #     plt.show()

    def exportdatatoexcel(self, file_name, database_name):
        sql = "SELECT * FROM `"+database_name+"`"
        cursor.execute(sql)
        results = cursor.fetchall()
        fields = cursor.description
        excel = xlsxwriter.Workbook('./data/'+file_name+'.xlsx')
        sheet = excel.add_worksheet('sheet1')
        for field in range(0, len(fields)):
            sheet.write(0, field, fields[field][0])
        i = 1
        j = 0
        for i in range(1, len(results) + 1):
            for j in range(0, len(fields)):
                sheet.write(i, j, u'%s' % results[i- 1][j])
        excel.close()

    def choose(self):
        child = tkinter.Tk()
        # 弹出对话框的title
        child.title('选择公司-资产负债比')
        child['height'] = 150
        child['width'] = 500
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        label = tkinter.Label(child, text='请输入要查看的公司名:',)
        label.place(x=1, y=17)
        # 弹出输入对话框请获取相应的值
        digit_str = tkinter.StringVar()
        entry = tkinter.Entry(child, textvariable=digit_str)
        entry.place(x=250, y=17)
        btny = Button(child, text="确定", command=lambda: [visual.visual_assets_liability_ratio(), self.root.destory()])
        btny.place(x=100,y=100)
        btnn = Button(child, text="取消", command=lambda: child.destroy())
        btnn.place(x=400, y=100)

    def choose2(self):
        child = tkinter.Tk()
        lst=[]
        # 弹出对话框的title
        child.title('选择公司-比较利润率')
        child['height'] = 200
        child['width'] = 500
        child.resizable(0, 0)
        # 设置弹出对话的框的标签值
        label = tkinter.Label(child, text='请输入要查看的公司名:', font=('黑体', 12))
        label.place(x=1, y=17)
        # 弹出输入对话框请获取相应的值
        digit_str = tkinter.StringVar()
        entry = tkinter.Entry(child, font=('黑体', 12), textvariable=digit_str)
        entry.place(x=250, y=17)
        btny = Button(child, text="确定", command=lambda:[visual.visual_test(lst),child.destroy()])
        btny.place(x=100, y=100)
        btnc = Button(child, text="继续选择",command=lambda:[lst.append(entry.get()),Label(child, text="已选择的公司有："+",".join(lst)).place(x=20,y=140)])
        btnc.place(x=250, y=100)
        btnn = Button(child, text="取消",command=lambda:child.destroy())
        btnn.place(x=400, y=100)




app = GUI()

