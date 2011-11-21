from tectudo.comentarios import ComentariosDaMateria
from lxml import html as lhtml

def numberOfComment(materia):
    number = 0
    try:
        comentarios = ComentariosDaMateria(materia)
        response = comentarios.html()
        html = lhtml.fromstring(response)
        number = len(html.cssselect('li'))
    except:
        pass

    return number