# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:46:38 2022

@author: ARITRA MONDAL
"""


import random
import time
from tkinter import *
import matplotlib.pyplot as plt
import os

# *****************************
import mysql.connector as msql

hst = "localhost"
usr = "root"
pas = "admin"

db = 'sortdb'
tb = 'sortData'

def insertdata(v1, v2, v3):
    con = msql.connect(host = hst, user = usr, passwd = pas, database = db)
    
    if con.is_connected() == False: print("Connection Failed")
    else:
        cur = con.cursor()
        q = "INSERT INTO " + tb + " VALUES(" + v1 + ", " + v2 + ", " + v3 + ")"
        cur.execute(q)
        con.commit()   
        print(cur.rowcount, "record(s) inserted") 
        
        cur.execute("SELECT * FROM " + tb)    
        rs = cur.fetchall()   
        for data in rs: print(data)    
        print(cur.rowcount, "record(s) in table")     
        
        con.close()

def createTable():    
    con = msql.connect(host = hst, user = usr, passwd = pas, database = db)
    
    if con.is_connected() == False: print("Connection Failed")
    else:
        cur = con.cursor()  
        cur.execute("SHOW TABLES")    
        result = cur.fetchall()  
        if (tb,) in result: pass
        else:
            q = "CREATE TABLE " + tb + " (d1 VARCHAR(20), d2 VARCHAR(20), d3 VARCHAR(20))"
            cur.execute(q)
            con.commit()
            cur.execute("SHOW TABLES")    
            result = cur.fetchall()  
            if (tb,) in result: print('Table CREATED')
        
        con.close()

def createDB():
    con = msql.connect(host = hst, user = usr, passwd = pas)

    if con.is_connected() == False: print("Connection Failed")
    else:
        cur = con.cursor()            
        cur.execute("SHOW DATABASES") 
        result = cur.fetchall()   
        if (db,) in result: pass
        else:
            cur.execute("CREATE DATABASE " + db)
            cur.execute("SHOW DATABASES")  
            result = cur.fetchall()  
            if (db,) in result: print('Database CREATED')
            createTable()        
        con.close()
# *****************************

c = 0
x1, y1 =[], []
x2, y2 = [], []
x3, y3 = [], []
x4, y4 = [], []
plot_count = 0
window = Tk()
action = 0
n = 0
#t = Text(root)



window.title("Search_Sort")
window.config(padx = 50, pady = 50, bg = "#F8CE9D")

def refresh():
    global x1, x2, x3, x4
    x1, x2, x3, x4 = [], [], [], []
    global y1, y2, y3, y4
    y1, y2, y3, y4 = [], [], [], []
    global n 
    n = 0
    global action
    action = 0
    Button_graph.config(state = DISABLED)
    e.delete(0, 'end')
    e1.delete(0, 'end')
    e2.delete(0, 'end')
    #plt.clf()
    canvas1 = Canvas(width = 500, height = 500, bg = "#F8CE9D",  highlightthickness = 0)
    canvas1.grid(column = 14, row = 1)
    time_value.config(text = "")
    time_taken.config(text = "")
    
def put_image(window):
    canvas = Canvas(width = 480, height = 480, bg = "#F8CE9D",  highlightthickness = 0)
    img1 = PhotoImage(file = "G.png")
    window.img1 = img1
    canvas.create_image((5, 5), image= img1, anchor='nw')
    canvas.grid(column = 14, row = 1)
    

#------Plotting graph-----------#
def graph(x, y, sn):
    plt.title("No of elements vs time taken for ") 
    plt.ylabel("Time in (s)")
    plt.xlabel("No of elements") 
    plt.grid(True, color = 'k')
    if sn == 1:
        plt.plot(x, y, linewidth = 5, color = 'g', marker = '^', markeredgecolor = 'r')
    elif sn == 2:
        plt.plot(x, y, linewidth = 5, color = 'y', marker = '^', markeredgecolor = 'r')
    elif sn == 3:
        plt.plot(x, y, linewidth = 5, color = 'purple', marker = '^', markeredgecolor = 'r')
    elif sn == 4:
        plt.plot(x, y, linewidth = 5, color = 'brown', marker = '^', markeredgecolor = 'r')
        
    global c
    c += 1    
    plt.savefig("G.png")
    img1 = PhotoImage(file = "G.png")
    put_image(window)
    

  

#----Sorting_Algorithms----------#

#----------Quick Sort---------------#
def split(a, lt, rt):
    lc = lt
    while True:
        if lc == lt and lc == rt:
            break
        elif lc == lt:
            if a[lc] <= a[rt]:
                rt -= 1
            elif a[lc] > a[rt]:
                a[lc], a[rt] = a[rt], a[lc]
                lc = rt
        elif lc == rt:
            if a[lc] >= a[lt]:
                lt += 1
            elif a[lc] < a[lt]:
                a[lc], a[lt] = a[lt], a[lc]
                lc = lt
    return lc            




def quick_sort(a, beg, end):
    if beg < end:
        pi = split(a, beg, end)
        quick_sort(a, beg, pi - 1)
        quick_sort(a, pi + 1, end)


def sort1():
    global action
    action += 1
    global n, n1, n2
    if action == 1:
        n = int(e.get())
    elif action == 2:
        n = int(e1.get())
    elif action == 3:
        n = int(e2.get())
   
    a = []
    global x1
    x1.append(n)
    for i in range(n):
        v = random.randint(1, n)
        a.append(v)
        
    beg, end = 0, n - 1
    t1 = time.time()
    quick_sort(a, beg, end)
    t2 = time.time()
    time_value.config(text = str(t2 - t1))
    time_taken.config(text = "Time Taken(in sec) to sort : ")
    global y1
    y1.append(t2 - t1)
   
    if len(x1) == 3:
        Button_graph.config(state = NORMAL)
        for i in y1:
            time_value.config(text = str(i))
        
   
    

#-----Merge Sort-----------#
def merge_sort(a, beg, end):
    mid = 0
    if beg < end:
        mid = (beg + end) // 2
        merge_sort(a, beg, mid)
        merge_sort(a, mid + 1, end)
        merge1(a, beg, mid, mid + 1, end)

def merge1(a, b, c, d, e):
    i = b
    n1 = c
    j = d
    n2 = e
    t = []
    while i <= n1 and j <= n2:
        if a[i] <= a[j]:
            t.append(a[i])
            i = i + 1
        else:
            t.append(a[j])
            j = j + 1

    
    while i <= n1:
        t.append(a[i])
        i += 1

    while j <= n2:
        t.append(a[j])
        j += 1
     
    a[b : e + 1] = t
        

def sort2():
    global action
    action += 1
    if action == 1:
        n = int(e.get())
    elif action == 2:
        n = int(e1.get())
    elif action == 3:
        n = int(e2.get())
   
    a = []
    global x2
    x2.append(n)
    for i in range(n):
        v = random.randint(1, n)
        a.append(v)
        
    beg, end = 0, n - 1
    t1 = time.time()
    merge_sort(a, beg, end)
    t2 = time.time()
    time_value.config(text = str(t2 - t1))
    time_taken.config(text = "Time Taken(in sec) to sort : ")
    global y2
    y2.append(t2 - t1)
    if len(x2) == 3:
       Button_graph.config(state = NORMAL)
       for i in y2:
           time_value.config(text = str(i))
       

#-------------Heap Sort-----------# 
def swap(li, i, j):
    li[i], li[j] = li[j], li[i]

def siftDown(li, i, upper):
    while True:
        l, r = i*2 + 1, i*2 + 2
        if max(l, r) < upper:
            if li[i] >= li[l] and li[r]:
                break
            elif li[l] > li[r]:
                swap(li, i, l)
                i = l
            elif li[r] > li[i]:
                swap(li, i, r)
                i = r
        elif l < upper:
            if li[l] > li[i]:
                swap(li, i, l)
                i = l
            else:
                break
        elif r < upper:
            if li[r] > li[i]:
                swap(li, i, r)
                i = r
            else:
                break
        else:
            break
def heapsort(li):
    for i in range((len(li) - 2) // 2, -1, -1):
        siftDown(li, i, len(li))
    
    for i in range(len(li) - 1, 0, -1):
        swap(li, 0, i)
        siftDown(li, 0, i)
        

def sort3():
    global action
    action += 1
    if action == 1:
        n = int(e.get())
    elif action == 2:
        n = int(e1.get())
    elif action == 3:
        n = int(e2.get())
    a = []
    global x3
    x3.append(n)
    for i in range(n):
        v = random.randint(1, n)
        a.append(v)
    
    for i in range(n):
        v = random.randint(1, n)
        a.append(v)
        
    
    t1 = time.time()
    heapsort(a)
    t2 = time.time()
    time_value.config(text = str(t2 - t1))
    time_taken.config(text = "Time Taken(in sec) to sort : ")   
    global y3
    y3.append(t2 - t1)
    if len(x3) == 3:
       Button_graph.config(state = NORMAL)
       for i in y3:
           time_value.config(text = str(i))

#---------TimSort---------------#
MINIMUM= 32
  
def find_minrun(n): 
  
    r = 0
    while n >= MINIMUM: 
        r |= n & 1
        n >>= 1
    return n + r 
  
def insertion_sort(array, left, right): 
    for i in range(left+1,right+1):
        element = array[i]
        j = i-1
        while element<array[j] and j>=left :
            array[j+1] = array[j]
            j -= 1
        array[j+1] = element
    return array
              
def merge(array, l, m, r): 
  
    array_length1= m - l + 1
    array_length2 = r - m 
    left = []
    right = []
    for i in range(0, array_length1): 
        left.append(array[l + i]) 
    for i in range(0, array_length2): 
        right.append(array[m + 1 + i]) 
  
    i=0
    j=0
    k=l
   
    while j < array_length2 and  i < array_length1: 
        if left[i] <= right[j]: 
            array[k] = left[i] 
            i += 1
  
        else: 
            array[k] = right[j] 
            j += 1
  
        k += 1
  
    while i < array_length1: 
        array[k] = left[i] 
        k += 1
        i += 1
  
    while j < array_length2: 
        array[k] = right[j] 
        k += 1
        j += 1
  
def tim_sort(array): 
    n = len(array) 
    minrun = find_minrun(n) 
  
    for start in range(0, n, minrun): 
        end = min(start + minrun - 1, n - 1) 
        insertion_sort(array, start, end) 
   
    size = minrun 
    while size < n: 
  
        for left in range(0, n, 2 * size): 
  
            mid = min(n - 1, left + size - 1) 
            right = min((left + 2 * size - 1), (n - 1)) 
            merge(array, left, mid, right) 
  
        size = 2 * size 

def sort4():
    global action
    action += 1
    if action == 1:
        n = int(e.get())
    elif action == 2:
        n = int(e1.get())
    elif action == 3:
        n = int(e2.get())
    a = []
    global x4
    x4.append(n)
    for i in range(n):
        v = random.randint(1, n)
        a.append(v)
    
    t1 = time.time()
    tim_sort(a)
    t2 = time.time()
    time_value.config(text = str(t2 - t1))
    time_taken.config(text = "Time Taken(in sec) to sort : ")
    global y4
    y4.append(t2 - t1)
    if len(x4) == 3:
       Button_graph.config(state = NORMAL)
       for i in y4:
           time_value.config(text = str(i))

    
def linear():
    
    
    global c
    c += 1
    
    if c > 1:
        time_value.config(text = "")
    
    
    n = int(e.get())
    #print(type(n))
    
    
    a = []
    
    for i in range(n):
        a.append(i)
    
    

    v = random.choice(a)
    
    t1 = time.time()
    for i in range(len(a)):
        if a[i] == v:
            #value_found.config(text = "Value found!!")
            t2 = time.time()
            time_value.config(text = str(t2 - t1))
            time_taken.config(text = "Time Taken(in sec) : ")
            break
    
  
def binary():
    global c
    c += 1
    
    if c > 1:
        time_value.config(text = "")
    
    n = int(e.get())
    
    a = []
    
    for i in range(n):
        v = random.randint(1, n)
        a.append(v)
        
   
    val = random.choice(a)
    
    beg, end = 0, n - 1
    
    a.sort()
    
    t1 = time.time()
    
    while beg <= end:
        mid = (beg + end) // 2
        if a[mid] == val:
            #value_found.config(text = "Value found!!")
            t2 = time.time()
            time_value.config(text = str(t2 - t1))
            time_taken.config(text = "Time Taken(in sec) : ")
            break
        elif a[mid] > val:
            end = mid - 1
         
        elif a[mid] < val:
            beg = mid + 1
    
  

def graph_button():
    global x1, x2
    if len(x1) == 3:
        graph(x1, y1, 1)
    elif len(x2) == 3:
        graph(x2, y2, 2)
    elif len(x3) == 3:
        graph(x3, y3, 3)
    elif len(x4) == 3:
        graph(x4, y4, 4)

def OK():
    Button_Sort1.config(state = NORMAL)
    Button_Sort2.config(state = NORMAL)
    Button_Sort3.config(state = NORMAL)
    Button_Linear.config(state = NORMAL)
    Button_Binary.config(state = NORMAL)
    
    val1 = e.get()
    val2 = e1.get()
    val3 = e2.get()
    
    createDB()
    insertdata(val1, val2, val3)
    

# Button to display time required for searching

canvas = Canvas(width = 500, height = 500, bg = "#F8CE9D", highlightthickness = 0)
img = PhotoImage(file = "Image.png")
canvas.create_image(250, 250, image = img)
canvas.grid(column = 4, row = 1, columnspan = 10)

input_size = Label(text="Size of list :", font=("Arial", 15), bg = "#F8CE9D", fg = "#3C256C" )
input_size.grid(column = 6, row = 2)

gap1 = Label(text = "           ", bg = "#F8CE9D")
gap1.grid(column = 6, row = 3)

e = Entry(width = 10, bg = "#36946F")
e.grid(column = 7, row = 2)
e.focus()


Button_Linear = Button(text = "Linear Search", command = linear, width = 15, bg = "#34BAD4", state = DISABLED)
Button_Linear.grid(column = 7, row = 4)

# Gap b/w linear and Binary buttons
gap = Label(text = "           ", bg = "#F8CE9D")
gap.grid(column = 7, row = 5)




Button_Binary = Button(text = "Binary Search", command = binary,  width = 15, bg = "#34BAD4", state = DISABLED)
Button_Binary.grid(column = 7, row = 6)

gap_refresh = Label(text = "           ", bg = "#F8CE9D")
gap_refresh.grid(column = 7, row = 7)

#-----------------Refresh Button------------#
Button_refresh = Button(text = "Refresh", command = refresh,  width = 15, bg = "#34BAD4")
Button_refresh.grid(column = 7, row = 8)

"""
Button_OK = Button(text = "OK",   width = 25, bg = "#34BAD4")
Button_OK.grid(column = 7, row = 11)
"""

gap4 = Label(text = "           ", bg = "#F8CE9D")
gap4.grid(column = 7, row = 9)

time_value = Label(text = "", font = ("Arial", 15), bg = "#F8CE9D")
time_value.grid(column = 7, row = 10)

gap3 = Label(text = "           ", bg = "#F8CE9D")
gap3.grid(column = 6, row = 8)

gap_new = Label(text = "           ", bg = "#F8CE9D")
gap_new.grid(column = 6, row = 9)

time_taken = Label(text = "", font = ("Arial", 15),  bg = "#F8CE9D", fg = "#3C256C")
time_taken.grid(column = 6, row = 10)
 


Button_Sort1 = Button(text = "Quick Sort", command = sort1,  width = 15, bg = "#34BAD4", state = DISABLED)
Button_Sort1.grid(column = 6, row = 4)

gap1 = Label(text = "           ", bg = "#F8CE9D")
gap1.grid(column = 6, row = 5)

Button_Sort2 = Button(text = "Merge Sort", command = sort2,  width = 15, bg = "#34BAD4", state = DISABLED)
Button_Sort2.grid(column = 6, row = 6)

Button_Sort3 = Button(text = "Tim Sort", command = sort4,  width = 15, bg = "#34BAD4", state = DISABLED)
Button_Sort3.grid(column = 8, row = 4)

gap2 = Label(text = "           ", bg = "#F8CE9D")
gap2.grid(column = 8, row = 5)

Button_Sort4 = Button(text = "Heap Sort", command = sort3,  width = 15, bg = "#34BAD4", state = DISABLED)
Button_Sort4.grid(column = 8, row = 6)

refresh_graph_gap = Label(text = "           ", bg = "#F8CE9D")
refresh_graph_gap.grid(column = 8, row = 7)

Button_graph = Button(text = "Graph", command = graph_button,  width = 15, bg = "#34BAD4", state =  DISABLED)
Button_graph.grid(column = 8, row = 8)

gap5 = Label(text = "         ", bg = "#F8CE9D")
gap5.grid(column = 9, row = 4)

gap6 = Label(text = "                    ", bg = "#F8CE9D")
gap6.grid(column = 10, row = 4)    

gap7 = Label(text = "               ", bg = "#F8CE9D")
gap7.grid(column = 11, row = 4)    

gap8 = Label(text = "                            ", bg = "#F8CE9D")
gap8.grid(column = 12, row = 4)    

gap8 = Label(text = "                            ", bg = "#F8CE9D")
gap8.grid(column = 13, row = 1)    

"""
gap_second_entry = Label(text = " ", bg = "#F8CE9D")
gap_second_entry.grid(column = 8, row = 2)
 """
e1 = Entry(width = 10, bg = "#36946F")
e1.grid(column = 9, row = 2)
 
gap_third_entry = Label(text = "   ", bg = "#F8CE9D")
gap_third_entry.grid(column = 10, row = 2)
 
e2 = Entry(width = 10, bg = "#36946F")
e2.grid(column = 11, row = 2)

gap_OK = Label(text = "   ", bg = "#F8CE9D")
gap_OK.grid(column = 12, row = 2)

Button_OK = Button(text = "OK",  command = OK,   width = 15, bg = "#34BAD4")
Button_OK.grid(column = 13, row = 2)

window.mainloop()
