import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#guardar
def guardarBD(fnome,bd): #MUDEI
    fout = open(fnome,"w", encoding='utf-8')
    json.dump(bd, fout, ensure_ascii=False, indent = 4 )
    fout.close()

#carregar bd
def carregarBD(fnome):
    f= open(fnome, encoding='utf-8')
    base = json.load(f)
    return base

#importar outro ficheiro
def importar(bd,ficheiro): #MUDADO
    f = open(ficheiro, 'r', encoding='utf-8')
    dados = json.load(f)
    campos = ["abstract", "authors", "doi", "title","url"]
    cond=True
    for d in dados:
        for campo in campos:
            if campo not in d.keys(): 
                cond = False
    if cond:
        for d in dados:
            if d not in bd:
                bd.append(d)
        return bd
    else: 
        return "Ficheiro não suportado"


#**criar uma pub**
def criarPub(bd, abstract, keywords, authors, doi, pdf, publish_date, title, url):
    post={}
    post["abstract"]= abstract
    if keywords!="":
        post["keywords"]= keywords
    post["authors"]= authors
    post["doi"]= doi
    if pdf!="":
        post["pdf"]= pdf
    if publish_date !="":
        post["publish_date"]= publish_date
    post["title"]= title
    post["url"]= url
    bd.append(post)
    return bd

#criar autor
def criarAutores(nome,afiliação,orcid):
    autor={}
    if nome!= None:
        autor["name"]= nome
    if afiliação!= None:
        autor["affiliation"]= afiliação
    if orcid !=None:
        autor["orcid"]= orcid
    if autor != {}:
        return autor
    
def criarKeywords(keywords,palavra):
    if keywords=="":
        keywords=palavra
    else:
        keywords=keywords+", "+palavra
    return keywords

#**encontrar pub por id**
def encontrarPub(bd,id):
    encontrado=False
    indice=0
    while indice<len(bd) and not encontrado:
        if bd[indice]["doi"][29:]==id:
            encontrado= True 
        else:
            indice=indice+1
    if not encontrado:
        return False
    else:
        return indice

#consultar esse id
def consultapID(bd,id):
    return bd[encontrarPub(bd,id)]

#eliminar a pub com esse id
def elimPub(bd,id):
    ind=encontrarPub(bd,id)
    bd.remove(bd[ind])
    return bd

#**DISTRIBUIÇÕES**
def anosexistentes(bd):
    res=[]
    for d in bd:
        if "publish_date" in d.keys():
            if d["publish_date"]!="" and d["publish_date"][0]!=" ":      
                if d["publish_date"][:4] not in res:
                    res.append(d["publish_date"][:4])
    res=sorted(res,key=lambda ano:int(ano),reverse=True)
    return res

def anoscompalavras(bd):
    res=[]
    for d in bd:
        if "publish_date" in d.keys() and "keywords" in d.keys() and d["publish_date"]!="" and d["publish_date"][0]!=" ":
            if d["publish_date"][:4] not in res:
                res.append(d["publish_date"][:4])
    res=sorted(res,key=lambda ano:int(ano),reverse=True)
    return res

def distribOrdena(d,ind):  
    lista=list(d.items())
    if ind==0:
        listaord = sorted(lista,key=fordena0,reverse=False)
    else:
        listaord = sorted(lista,key=fordena1,reverse=True)

    return listaord

def fordena0(par):
    return par[0]
def fordena1(par):
    return par[1]

#distrib do top de palavras
def TopPalavrasChave(bd,n):
    distrib={}
    for d in bd:
        lista= d.items()
        for campos in lista:
            if campos[0]== "keywords":
                palavras= campos[1].split(", ")
                for pal in palavras:
                    pal=pal.strip(".")
                    if pal in distrib:
                        distrib[pal] = distrib[pal] +1
                    else:
                        distrib[pal] = 1
    distrib=dict(distribOrdena(distrib,1)[:n])                  
    return distrib

#distrib de palavras por ano
def PalavraporAno(bd,n):
    distrib= {}
    distrib["Sem data"]={}

    for d in bd:
        if "publish_date" in d.keys() and d["publish_date"]!="" and d["publish_date"][0]!=" ":
            data = d["publish_date"].split("-")
            ano=data[0]

            if "keywords" in d.keys():
                if ano not in distrib.keys():
                    distrib[ano] = {}

                palavras= d["keywords"].split(", ")
                for pal in palavras:
                    pal=pal.strip(".")
                    if pal in distrib[ano]:
                        distrib[ano][pal] = distrib[ano][pal] +1
                    else:
                        distrib[ano][pal] = 1
        else:
            if "keywords" in d.keys():
                palavras= d["keywords"].split(", ")

                for pal in palavras:
                    pal=pal.strip(".")
                    if pal in distrib["Sem data"]:
                        distrib["Sem data"][pal] = distrib["Sem data"][pal] +1
                    else:
                        distrib["Sem data"][pal] = 1

    for ano,freq in distrib.items():
        distrib[ano]=dict(distribOrdena(freq,1)[:n])
    distrib=dict(distribOrdena(distrib,0))
    return distrib

#distrib por autores
def PubporAutor(bd,n):
    distrib={}
    for d in bd:
        if "authors" in d.keys():
            for dic in (d["authors"]):
                if dic["name"] in distrib:
                    distrib[dic["name"]] = distrib[dic["name"]] +1
                else:
                    distrib[dic["name"]] = 1
    distrib=dict(distribOrdena(distrib,1)[:n]) 
    return distrib

#distrib por autores por ano
def AutorporAno(bd,autor): #mudado
    distrib={}
    for d in bd:
        for dic in (d["authors"]):
            if dic["name"].strip(". ") == autor:
                if "publish_date" in d.keys() and d["publish_date"]!="" and d["publish_date"][0]!=" ":
                    data = d["publish_date"].split("-")
                    ano=data[0]
                    if ano in distrib:
                        distrib[ano] = distrib[ano] +1
                    else:
                        distrib[ano]= 1
                else:
                    if "Sem data" not in distrib.keys():
                        distrib["Sem data"]=1
                    else:
                        distrib["Sem data"]= distrib["Sem data"]+1

    distrib=dict(distribOrdena(distrib,0))
    return distrib

#distrib por ano
def statsPubAno(bd):
    distrib={}
    distrib["Sem data"]=0
    for d in bd:
        if "publish_date" in d.keys() and d["publish_date"]!="" and d["publish_date"][0]!=" ":
            data = d["publish_date"].split("-")
            ano=data[0]
            if ano in distrib:
                distrib[ano] = distrib[ano] +1
            else:
                distrib[ano] = 1
        else:
            distrib["Sem data"]= distrib["Sem data"]+1
    distrib=dict(distribOrdena(distrib,0))
    return distrib

#distrib por mes
def statsPubMes(bd,ano):
    distrib={}
    for d in bd:
        if "publish_date" in d.keys() and d["publish_date"]!="" and d["publish_date"][0]!=" ":
            data = d["publish_date"].split("-")
            mes=data[1]
            if int(data[0])==ano:

                if mes in distrib:
                    distrib[mes] = distrib[mes] +1
                else:
                    distrib[mes] = 1
    distrib=dict(distribOrdena(distrib,0))
    res={}
    for mes,valor in distrib.items():    
        for num,desig in [("01","Janeiro"),("02","Fevereiro"),("03","Março"),("04","Abril" ),("05","Janeiro"),("06","Junho"),("07","Julho"),("08","Agosto"),("09","Outubro"),("10","Novembro"),("12","Dezembro")]:    
            if mes==num:
                res[desig]=valor
    return res

def desenhar(canvas, figura):
    canvas_widget = FigureCanvasTkAgg(figura, canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(side='top', fill='both', expand=1)
    return canvas_widget

def distribGrafico(d, titulo):
    valores = list(d.values())
    labels = list(d.keys())

    cores_nomeadas = list(mcolors.CSS4_COLORS.keys())
    random.shuffle(cores_nomeadas)
    cores_personalizadas = cores_nomeadas[:len(labels)]

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.barh(labels, valores, color=cores_personalizadas)
    ax.set_title(titulo)
    
    for ind, value in enumerate(valores):
        plt.text(value, ind,str(value))
        plt.tight_layout()
    return fig

#Gráficos da linha de comando
def distribGraficoComando(d, titulo):
    valores = list(d.values())
    labels = list(d.keys())

    cores_nomeadas = list(mcolors.CSS4_COLORS.keys())
    random.shuffle(cores_nomeadas)
    cores_personalizadas = cores_nomeadas[:len(labels)]

    
    plt.barh(labels, valores, color=cores_personalizadas)
    plt.title(titulo)
    for ind, value in enumerate(valores):
        plt.text(value, ind,str(value))
        plt.tight_layout()
    plt.show()

#**listar o nome do autor**
def listarautor(bd): #MUDADO
    res = []
    for d in bd:
        for a in d['authors']:
            nome = a['name'].strip(". ")
            if nome not in res:
                res.append(nome)
    return res

def ordenarMaisArtigos(bd,lista): #NOVO
    frequencia = {}
    for d in bd:
        for autor in d["authors"]:
            if autor["name"] in lista:  # Verifica se o autor está na lista fornecida
                if autor["name"] in frequencia:
                    frequencia[autor["name"]] = frequencia[autor["name"]] + 1  # Incrementa a contagem se já existir
                else:
                    frequencia[autor["name"]] = 1
    return frequencia

#**FILTRO**

#Filtro Autor
def consultarpAutor(bd,autor):
    res = []
    for d in bd:
        for a in d['authors']:
            if autor == a['name'].strip(". "):
                res.append(d)
    return res

def listarautor_pub(bd,lista): #EXCLUSIVO COMANDO
    autores = []
    for nome in lista:
        autores.append((nome,consultarpAutor(bd,nome)))
    return dict(autores)

      
#Filtro Titulo
def consultarPubTitulo(bd,titulo): #EXCLUSIVA DO COMANDO
    res = []
    for post in bd:
        if post.get("title"):
            if titulo.lower() in post["title"].lower():
                res.append(post)
    return res

#Filtro Afilicao
def consultarPubAfiliacao(bd, affiliation): #MUDADO
    res = []
    for post in bd:
        for elem in post.get("authors", []):
            if "affiliation" in elem.keys():
                afil = elem.get("affiliation").lower()
                if affiliation.lower() in afil:
                    if post not in res:
                        res.append(post)
    return res

#Filtro Data
def consultarpData(bd,data):
    res = []
    for d in bd:
        publish_date = d.get('publish_date')#mudar para o caso de atualizar porque na 3242 tem um caso a parte            
        if publish_date and d["publish_date"]!="" and d["publish_date"][0]!=" ":
            publish_date = publish_date[-10:]
            if data == publish_date:
                res.append(d)
    return res

def ordenarData(lista,cond):
    lista = sorted(lista, key=lambda pub: (pub.get("publish_date") is None, pub.get("publish_date")))
    if cond == True:
        lista.reverse()
    return lista


def searchbydate(bd,ind,num):#permite pesquisar por uma parte da data(ex:todas as pubs de 2024)
    res=[]
    if len(num)==1:
        num="0"+num
    for pub in bd:
        if "publish_date" in pub.keys():
            if len(pub["publish_date"].split("-"))-1>=ind:
                if pub["publish_date"].split("-")[ind]==num:
                    res.append(pub)
    return res

#Filtro KeyWord
def consultarpKeyword(bd,palavras): #MUDADO
    res = []
    for pal in palavras:
        for d in bd:
            keywords = d.get('keywords')
            if keywords:
                keywords = keywords.lower().split(", ")
                for elem in keywords:
                    for i,letra in enumerate(elem):
                        if letra == "/" or letra == "(":
                            elem = elem[0:i]
                    if pal.lower() == elem and d not in res:
                        res.append(d)
    return res

#TABELA COM AS KEYWORDS
def listarKeyword(bd):
    res = []
    lista_aux = []
    for d in bd:
        if "keywords" in d.keys():
            keywords = d['keywords'].split(",")
            for elem in keywords:
                for i,letra in enumerate(elem):
                    if letra == "/" or letra == "(":
                        elem = elem[0:i]
                elem2 = elem.upper().strip().strip(".")
                if elem2 not in lista_aux:
                    lista_aux.append(elem2)
                    res.append(elem.strip())
    return res

def keywordsmaisvezes(bd,f_keywords,cond): # perguntar ao abel?? MUDADO
    contador = {}
    original = {}
    for d in bd:
        if "keywords" in d.keys():
            keywords = d['keywords'].split(",")
            for elem in keywords:
                for i,letra in enumerate(elem):
                    if letra == "/" or letra == "(":
                        elem = elem[0:i]
                elem2 = elem.upper().strip(". ")
                if elem2 in contador:
                    contador[elem2] = contador[elem2] + 1
                else:
                    contador[elem2] = 1
                    original[elem2] = elem.strip()

    filtered_keywords = {kw.upper(): kw for kw in f_keywords}
    contador = {key: contador[key] for key in filtered_keywords.keys() if key in contador}
    original = {key: original[key] for key in filtered_keywords.keys() if key in original}
    ordenado = sorted(contador.items(), key = lambda x: x[1], reverse = cond)
    res = [original[palavra] for palavra,_ in ordenado]
    return res


#BUSCAR POR TITULO
def buscarPostPorTitulo(db, titulo):
    for post in db:
        if post['title'] == titulo:
            return post
        
def pub(post): #NOVA
    detalhes = []
    detalhes.append(f"Título: {post['title']}\n")
    detalhes.append(f"Resumo: {post['abstract'].strip('Resumo Introdução:')}\n")
    if post.get('keywords'):
        detalhes.append(f"Palavras-Chave: {post['keywords']}\n")
    if post.get("publish_date"):
        detalhes.append(f"Data: {post['publish_date']}\n")
    else:
        detalhes.append("Data: Desconhecida\n")
    for autor in post['authors']:
        detalhes.append(f"Autor: {autor['name']}")
        if autor.get('affiliation'):
            detalhes.append(f"Afiliações: {autor['affiliation']}\n")
        else:
            detalhes.append("Afiliações: Desconhecidas.\n")
    detalhes.append(f"DOI: {post['doi']}\n")
    if post.get("pdf"):
        detalhes.append(f"PDF: {post['pdf']}\n")
    else:
        detalhes.append("PDF: Não existe\n")
    if post.get("url"):
        detalhes.append(f"URL: {post['url']}")
    else:
        detalhes.append("URL: Não existe\n")    

    return "\n".join(detalhes)

