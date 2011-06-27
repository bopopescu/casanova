# -*- coding: utf-8 -*-   
import urllib2
#import xml.etree.ElementTree as etree
from lxml import etree



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

def grabClasse(sql):
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

def grabAtributos(sql):
    
    import re
    sql = sql.replace("\n","").replace("\t","")
    pat = re.compile('SELECT([A-Za-z_,. \']*)FROM([A-Za-z_., 0-9=]*)')
    result = pat.search(sql)
    l = result.group(1).replace(" ","").replace("'","").split(",")
    atributos=[]
    for entry in l:
        atributos.append(re.split("AS", entry))
        
    return atributos

def openOntology(ontology):
    req = urllib2.Request(ontology)
    response = urllib2.urlopen(req)    
    content = response.read()
    import pdb; pdb.set_trace()
    
    parser = etree.XMLParser(resolve_entities=True)    
    xml = etree.XML(content,parser)
    return xml


def getVocabularioFromOntology(ontology):
    ontology = openOntology(ontology)
    import pdb; pdb.set_trace()
    datatypeProperty = '{http://www.w3.org/2002/07/owl#}DatatypeProperty'
    objectProperty = '{http://www.w3.org/2002/07/owl#}ObjectProperty'
    objectClass = '{http://www.w3.org/2002/07/owl#}Class'
    ontologyVocabulario = 'http://www.semanticweb.org/ontologies/2010/5/futebol.owl'
    vocabulario = []
    for element in ontology.getchildren():
        if (element.tag == datatypeProperty) or (element.tag == objectProperty) or (element.tag == objectClass):
            item = element.items()[0][1]
            voc = item.split("#")
            if voc[0]=='':
                voc[0]=ontologyVocabulario
            voc[0]="<%s:%s>valor</%s:%s>" % (voc[0],voc[1],voc[0],voc[1])
            vocabulario.append(voc)
    return vocabulario

def qrdConvert(sql, ontology):
    vocabulario = getVocabularioFromOntology(ontology)
    attributos = grabAtributos(sql)
    #classe = grabClasse(sql)
    
    
    #print vocabulario


    rows = executeSQL(sql)
    for row in rows:
        reg=""
        for col in row:  
            reg+= "%s," % col  
        #print reg
        
        
    return sql

    
    

ontology = "http://semantica.globo.com/ontologia/futebol"

sql = """
SELECT campeonato.campeonato_id AS 'id',
	   campeonato.campeonato_txt AS 'label',
	   campeonato.descricao_lob AS 'descricao'
  FROM tb_glb_futp_campeonato AS Campeonato limit 1
"""

sql = qrdConvert(sql,ontology)
#print sql
