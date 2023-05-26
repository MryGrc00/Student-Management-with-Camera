 #database abstraction
from mysql.connector import connect

db=connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='student'
)

def getallrecord(table:str)->list:
    sql:str=f"SELECT * FROM `{table}`"
    cursor:object=db.cursor(dictionary=True)
    cursor.execute(sql)
    rows: list =cursor.fetchall()
    return rows
def getrecord(table:str, **kwargs)->list:
    keys: list= list(kwargs.keys())
    values: list= list(kwargs.values())
    sql:str=f"SELECT * FROM `{table}` WHERE `{keys[0]}`='{values[0]}'"
    cursor:object=db.cursor(dictionary=True)
    cursor.execute(sql)
    rows: dict =cursor.fetchone()
    return rows


def deleterecord(table:str, **kwargs)->int:
    keys: list= list(kwargs.keys())
    values: list= list(kwargs.values())
    sql:str=f"DELETE FROM `{table}` WHERE `{keys[0]}`='{values[0]}'"
    cursor:object=db.cursor()
    cursor.execute(sql)
    db.commit()
    rows_affected: int = cursor.rowcount
    cursor.close()
    return rows_affected

def addrecord(table:str, **kwargs)->int:
    keys: list= list(kwargs.keys())
    values: list= list(kwargs.values())
    #INSERT INTO `student`(``,``,``) vALUES('','','')
    flds:str="`,`".join(keys)
    data:str="','".join(values)
    sql: str=f"INSERT INTO `{table}`(`{flds}`) VALUES('{data}')"
    cursor:object=db.cursor()
    cursor.execute(sql)
    db.commit()
    rows_affected: int = cursor.rowcount
    cursor.close()
    return rows_affected
    
    
    


def updaterecord(table: str,**kwargs)->int:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    #UPDATE student SET lastname`='sample',firstname`='user' WHERE `idno`='0002'
    #key and value are joined together with a backtick`,equal=,sigle qoute''
    flds: list = list()
    for i in range(1,len(keys)):
        flds.append("`"+keys[i]+"`='"+values[i]+"'")
    fld: str = ",".join(flds)
    sql: str = f"UPDATE {table} SET {fld} WHERE `{keys[0]}`='{values[0]}'"
    cursor: object = db.cursor()
    cursor.execute(sql)
    db.commit()
    rows_affected: int = cursor.rowcount
    cursor.close()
    return rows_affected
    
    
    
    
def userlogin(table:str, **kwargs)->bool:
    keys: list= list(kwargs.keys())
    values: list= list(kwargs.values())
    sql: str= f"SELECT * FROM `{table}` WHERE`{keys[0]}`='{values[0]}' and `{keys[1]}`='{values[1]}'"
    cursor:object=db.cursor()
    cursor.execute(sql)
    row: dict = cursor.fetchone()
    cursor.close()
    return row





#testing getallrecord

#

