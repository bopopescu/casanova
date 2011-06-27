# -*- coding: utf-8 -*-   
def executeSQL(qry):
    import MySQLdb  
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="futpedia")
    cur = db.cursor()  
    try:
        cur.execute(qry)  
        rows = cur.fetchall()   
    except MySQLdb.Error, e:  
        try:  
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])  
        except IndexError:  
            print "MySQL Error: %s" % str(e)  
    cur.close()  
    db.close()
    return rows


def show(sql):
    rows = executeSQL(sql)
    m=[[]]
    print len(rows)
    for row in rows:
        reg=""
        print row
        for col in row:  
            m[0].append(col)
            
    print m        

tables = """
show tables
"""

columns = """
show columns from tb_glb_futp_campeonato where type in ("varchar(255)", "longtext")
"""
fk = """

"""

show(tables)
