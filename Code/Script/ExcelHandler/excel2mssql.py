#coding=utf-8
__author__ = 'Administrator'

import xlrd
import pymssql

SQLHOST='172.18.183.176'

def readExcel(fileName,sheetName):
    bk = xlrd.open_workbook(fileName)
    sh = bk.sheet_by_name(sheetName)
    nrows=sh.nrows
    tableData=[]
    title=sh.row_values(0)
    for i in range(1,nrows):
        #this is a list
        row_data = sh.row_values(i)
        tableData.append(row_data)
    return title,tableData

def createTable(tableName, title, fieldsIndex, sqlString):
    conn = pymssql.connect(host=SQLHOST, user='sa', password='22216785', database='stat')
    cur = conn.cursor()
    cur.execute("IF OBJECT_ID('%s', 'U') IS NOT NULL  DROP TABLE %s"%(tableName,tableName))
    cur.execute('create table %s ( %s )'%(tableName,sqlString))
    conn.commit()
    pass

def dataPouring(tableName, data,fieldsIndex):
    many=[]
    for i in data:
        a=[]
        for index in fieldsIndex:
            a.append(i[index])
        many.append(tuple(a))

    conn = pymssql.connect(host=SQLHOST, user='sa', password='22216785', database='stat')
    cur=conn.cursor()
    #shit...this line cannot be generalized...
    cur.executemany("insert into "+tableName+" values (%s, %d)", many)
    conn.commit()

if __name__=='__main__':
    title,tabledata=readExcel(u"E:\\Graduation\\词汇分析结果\\1.xlsx",u"词汇分组")
    print title

    #figure out which field to import into the sqlserver
    cmd_str=raw_input("Specify Fields Index(white space to split):")
    fields=cmd_str.split(' ')
    fieldsIndex=[int(a) for a in fields]

    sql_string=raw_input("table Schema(id int, ...)")

    tableName=raw_input("Table Name:")
    createTable(tableName=tableName, title=title, fieldsIndex=fieldsIndex, sqlString=sql_string)
    dataPouring(tableName=tableName,data=tabledata,fieldsIndex=fieldsIndex)
