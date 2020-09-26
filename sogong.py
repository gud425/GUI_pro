 #-*- encoding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sqlite3 as sq

form_class = uic.loadUiType(r"C:\Users\gud425\Documents\Visual Studio 2015\Projects\sogong\sogong\untitled.ui")[0]
dbname="name_info.db"

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
  
        CreateTable()
        SelectData(self)
        self.plus_btn.clicked.connect(self.plus_btn_click)
        self.tableWidget.cellClicked.connect(self.table_click)
        self.find_btn.clicked.connect(self.find_btn_click)
        self.tableWidget.cellChanged.connect(self.change_table)
    def plus_btn_click(self):
        InsertData(self,self.text_name.toPlainText(),self.text_birth.toPlainText(),self.text_phone.toPlainText())
    def table_click(self,row,column):
        if column==4:
            DeleteData(self,row)
    def find_btn_click(self):
        if(self.text_find_name.toPlainText()== ""):
            SelectData(self)
        else:
            FindData(self,self.text_find_name.toPlainText())
    def change_table(self,row,column):
        if column==3:
            ChangeData(self,row)
def CreateTable():
    conn=sq.connect(dbname)
    cur=conn.cursor()
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name ='stu_info'"
    cur.execute(sql)
    rows = cur.fetchall()
    if not rows:        
        sql = "CREATE TABLE stu_info (idx INTEGER PRIMARY KEY, name TEXT, birth TEXT, phone TEXT)"
        cur.execute(sql)
        conn.commit()
    conn.close()

def InsertData(self,name,birth,phone):
    conn = sq.connect(dbname)
    cur = conn.cursor()
    sql = "INSERT INTO stu_info (name, birth, phone) VALUES (?,?,?)"
    cur.execute(sql, (name, birth, phone))
    conn.commit()
    conn.close()
    SelectData(self)

def SelectData(self):
    conn = sq.connect(dbname)
    cur = conn.cursor()
    sql = "SELECT * FROM stu_info"
    cur.execute(sql)
    rows = cur.fetchall()        
    conn.close()
    setTables(self,rows)

def setTables(self,row):
    count=len(row)
    self.tableWidget.setRowCount(count)
    for x in range(count):
        idx,name,birth,phone=row[x]
        self.tableWidget.setItem(x, 0, QTableWidgetItem(str(idx)))
        self.tableWidget.setItem(x, 1, QTableWidgetItem(name))
        self.tableWidget.setItem(x, 2, QTableWidgetItem(birth))
        self.tableWidget.setItem(x, 3, QTableWidgetItem(phone)) 
        self.tableWidget.setItem(x, 4, QTableWidgetItem("del"))   

def DeleteData(self,row):
    conn = sq.connect(dbname)
    cur = conn.cursor()
    idx = self.tableWidget.item(row, 0).text()
    sql = "DELETE FROM stu_info WHERE idx =?"
    cur.execute(sql, (idx))
    conn.commit()
    conn.close()
    SelectData(self)

def FindData(self, text):
    conn=sq.connect(dbname)
    cur=conn.cursor()
    sql="SELECT * FROM stu_info WHERE name like '%"+text+"%'"
    cur.execute(sql)
    conn.commit()
    rows = cur.fetchall()  
    conn.close()
    setTables(self,rows)

def ChangeData(self,row):
    conn=sq.connect(dbname)
    cur=conn.cursor()
    change=self.tableWidget.item(row,3).text()
    idx=self.tableWidget.item(row,0).text()
    sql="UPDATE stu_info SET phone=? WHERE idx=?"
    cur.execute(sql,(change,idx))
    conn.commit()
    conn.close() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

