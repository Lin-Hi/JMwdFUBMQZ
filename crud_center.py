from numpy.core.defchararray import lower
import pandas as pd
import psycopg2


def add_center(cur):
    s = input("Enter inserted columns: ")
    allcols = s.strip().split(' ')
    for i in range(len(allcols)):
        allcols[i] = allcols[i].replace("_", " ")
    cols = ""
    vals = ""
    colname = ["name"]
    for i in range(len(allcols)):
        if allcols[i] != "null":
            vals += "'" + allcols[i] + "'" + ","
            cols += colname[i] + ","
    if cols != "":
        vals = vals.rstrip(",")
        cols = cols.rstrip(",")
        cur.execute("insert into center (" + cols + ") values (" + vals + ")")


def select_center(cur):
    s = input("Enter select columns: ")
    if s != "*":
        allcols = s.strip().split(' ')
        cols = ""
        col_list = []
        for i in range(len(allcols)):
            if allcols[i] != "null":
                cols += allcols[i] + ","
                col_list.append(allcols[i])
        if cols != "":
            cols = cols.rstrip(",")
    else:
        col_list = ["name"]
        cols = "name"
    cons = input("Enter select constraints: ")
    if cons != 'n':
        colname = ["name"]
        combine = ""
        allconsvals = cons.strip().split(' ')
        for i in range(len(allconsvals)):
            allconsvals[i] = allconsvals[i].replace("_", " ")
        for i in range(len(allconsvals)):
            if allconsvals[i] != "null":
                combine += colname[i] + " = '" + allconsvals[i] + "' and "
        combine = combine.rstrip("and ")
        cur.execute("select " + cols + " from center where " + combine)
        rows = cur.fetchall()
        data = pd.DataFrame(rows, columns=col_list)
        data.to_csv('select_cons_center.csv')
        print(data)
    else:
        cur.execute("select " + cols + " from center")
        rows = cur.fetchall()
        data = pd.DataFrame(rows, columns=col_list)
        data.to_csv('select_center.csv')
        print(data)


def update_center(cur):
    s = input("Enter update columns: ")
    allcols = s.strip().split(' ')
    for i in range(len(allcols)):
        allcols[i] = allcols[i].replace("_", " ")
    cols = ""
    colname = ["name"]
    for i in range(len(allcols)):
        if allcols[i] != "null":
            cols += colname[i] + " = '" + allcols[i] + "',"
    if cols != "":
        cols = cols.rstrip(",")
    cons = input("Enter update constraints: ")
    if cons != 'n':
        combine = ""
        allconsvals = cons.strip().split(' ')
        for i in range(len(allconsvals)):
            allconsvals[i] = allconsvals[i].replace("_", " ")
        for i in range(len(allconsvals)):
            if allconsvals[i] != "null":
                combine += colname[i] + " = '" + allconsvals[i] + "' and "
        combine = combine.rstrip("and ")
        cur.execute("update center set " + cols + " where " + combine)
    else:
        cur.execute("update center set " + cols)


def delete_center(cur):
    s = input("Enter delete constraints: ")
    allcols = s.strip().split(' ')
    for i in range(len(allcols)):
        allcols[i] = allcols[i].replace("_", " ")
    cols = ""
    colname = ["name"]
    for i in range(len(allcols)):
        if allcols[i] != "null":
            cols += colname[i] + " = '" + allcols[i] + "' and "
    if cols != "":
        cols = cols.rstrip("and ")
        cur.execute("delete from center where " + cols)


if __name__ == '__main__':
    conn = psycopg2.connect("host=localhost dbname=cs307_2 user=checker password=123456")
    cur = conn.cursor()
    operation = input()
    while operation != "q":
        if lower(operation) == 'c':
            add_center(cur)
        if lower(operation) == 'r':
            select_center(cur)
        if lower(operation) == 'u':
            update_center(cur)
        if lower(operation) == 'd':
            delete_center(cur)
        operation = input()
    conn.commit()
    conn.close()