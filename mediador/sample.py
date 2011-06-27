# -*- coding: utf-8 -*-
questions = {'quantos': 'select count(0)', 'qual': 'select *', 'quem': 'select *'}

classes = { 
'jogador' : ('tb_glb_futp_pessoa' , 'tb_glb_futp_funcao' ),
'tecnico' : ('tb_glb_futp_pessoa' , 'tb_glb_futp_funcao' , 'tb_glb_futp_posicao' ),
'goleiro' : ('tb_glb_futp_pessoa' , 'tb_glb_futp_funcao' , 'tb_glb_futp_posicao' ),
'atacante' : ('tb_glb_futp_pessoa' , 'tb_glb_futp_funcao' , 'tb_glb_futp_posicao' ),
'lateral' : ('tb_glb_futp_pessoa' , 'tb_glb_futp_funcao' , 'tb_glb_futp_posicao' ),
'meia' : ('tb_glb_futp_pessoa' , 'tb_glb_futp_funcao' , 'tb_glb_futp_posicao' ),
}

atributos = {
'gols' : ('tb_glb_futp_gol' , 'tb_glb_futp_participa', 'tb_glb_futp_pessoa' , 'tb_glb_futp_funcao', 'tb_glb_futp_jogo' )
}
    
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

def grabQuestion(msg):
    tokens = msg.split()
    for q in tokens:
        for qs in questions:
            if q == qs:
                return qs
    return "não encontrou um question marker como (quantos, quem, qual)"

def grabClasses(msg):
    tokens = msg.split()
    grabclasses=[]
    for q in tokens:
        for qs in classes:
            if q == qs:
                #for i in qs:
                try:
                    grabclasses.index(qs)
                except:
                    grabclasses.append(qs)
                    
    if grabclasses:
        return grabclasses
    else:                    
        return "não encontrou nenhuma classe (jogador, campeonato, estadio)"

def grabAtributos(msg,classes):
    tokens = msg.split()
    grabatributos=[]
    for q in tokens:
        for qs in atributos:
            if q == qs:
                #for i in qs:
                try:
                    grabatributos.index(qs)
                except:
                    grabatributos.append(qs)

    if grabclasses:
        return grabclasses
    else:                    
        return "não encontrou nenhuma classe (jogador, campeonato, estadio)"


def qryDraw(msg):
    print msg
    
    question = grabQuestion(msg)
    print question
    
    classes = grabClasses(msg)
    print classes
    
    atributos = grabAtributos(msg,classes)
    print atributos    
    
    #instancia = grabInstancia(msg)
    #print instancia    
    
    return msg

qry = qryDraw("quantos gols fez o jogador romario no campeonato carioca")

# rows = executeSQL(qry)
# for row in rows:
#     reg=""
#     for col in row:  
#         reg+= "%s," % col  
#     #print reg