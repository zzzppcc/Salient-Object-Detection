import xlrd

def open_xls(file):
    f = xlrd.open_workbook(file)
    return f
def getsheet(f):
    return f.sheets()

def get_Allrows(f,sheet):
    table=f.sheets()[sheet]
    return table.nrows

def getFile(file,shnum):
    datavalue = []
    f=open_xls(file)
    table=f.sheets()[shnum]
    num=table.nrows
    for row in range(num):
        rdata=table.row_values(row)
        datavalue.append(rdata)
    return datavalue

def getshnum(f):
    x=0
    sh=getsheet(f)
    for sheet in sh:
        x+=1
    return x
