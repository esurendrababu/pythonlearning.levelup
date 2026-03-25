#data base connectivity to python


# pip install python-mysql-connector
# pip3 install mysqp-connector-python



cursor.execute('create database new_db')
cursor.execute('show databases')
cursor.execute('create table emp(name varchar(30),salary bigint(30),id int(10))')
cursor.execute('show tables')
for table in cursor:
  print(table)



#insert one record
sqldata="insert into emp(name,salary,id)values(%s,%s,%s)"
record=("john",1000,1)
cursor.execute(sqldata,record)
conn.commit()





#inserting multiple records
sqldata=('insert into emp(name,salary,id)values(%s,%s,%s)')
records=[('Surendra',2000,2),
         ('Khaja',3000,3),
         ('subhani',4000,4)
         ]
cursor.executemany(sqldata,records)
conn.commit()

#Reading from the database
cursor.execute('select * from emp')
row=cursor.fetchall()
for i in row:
    print(i)

cursor.execute("select * from emp where name='Surendra'")
row=cursor.fetchall()
for i in row:
    print(i)

cursor.execute("update emp set name='mastan',salary=20000 where id=1")
conn.commit()
cursor.execute("delete from emp where id=3")
conn.commit()

cursor.execute("drop table emp")
conn.commit()
cursor.execute("drop databas new_db")
conn.commit()


# import mysql.connector
# conn=mysql.connector.connect(host='localhost',password='Mysql@123',user='root',database='new_db')
# cursor=conn.cursor()