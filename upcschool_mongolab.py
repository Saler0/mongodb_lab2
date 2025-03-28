# coding=utf-8
from example import Example
from model1 import Model1
from model2 import Model2
from model3 import Model3
from querys import Querys
import datetime
import sys
from pymongo import MongoClient



def show_options(new):
    print("Choose the option you want to execute:")
    print("\t -1 - Example")
    print("\t 0 - Exit")
    print("\t 1 - Model 1")
    print("\t 2 - Model 2")
    print("\t 3 - Model 3")

new = True
show_options(new)
op = int(input())

np = 48000 # empleados
nc = 2000 # compañias

while op != 0:
    if op == -1:
        n = int(input("Insert the number of documents to create:"))
        ex = Example()
        ex.data_generator(n)
    elif op == 1:
        print("iniciado la creacion de documentos...")
        m = Model1()
        m.data_generator(np,nc)
        print("se termino de insertar los documentos...")
        print("haciendo querys...")
        q = Querys()
        q.querys(op)
        print("fn de las querys...")
    elif op == 2:
        print("iniciado la creacion de documentos...")
        m = Model2()
        m.data_generator(np,nc)
        print("se termino de insertar los documentos...")
        print("haciendo querys...")
        q = Querys()
        q.querys(op)
        print("fn de las querys...")
    elif op == 3:
        print("iniciado la creacion de documentos...")
        m = Model3()
        m.data_generator(np,nc)
        print("se termino de insertar los documentos...")
        print("haciendo querys...")
        q = Querys()
        q.querys(op)
        print("fn de las querys...")
    else:
        print ("Exitting ...")
        sys.exit()

    show_options(new)
    op = int(input())