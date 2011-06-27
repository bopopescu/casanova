def executeSQL(qry):
    import MySQLdb  
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="jogador")
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
    
qry = "select * from jogador"    
rows = executeSQL(qry)
for row in rows:
    reg=""
    for col in row:  
        reg+= "%s," % col  
    #print reg