# Relatório técnico do projeto
## Data:2/01/2025
## Autores: Abel Filipe Rodrigues Pereira A105972, Dinis Pereira A107199, João Dinis Dias Pereira A107192

## Resumo

Neste relatório técnico vamos descrever a execução do projeto da cadeira de Algoritmos e Técnicas de Programação. 
Este relatório contém o procedimento efetuado na criação do código relativo às funções do processamento do *dataset*, interface de linha de comando e interface gráfica.



# Relatório técnico

## Análise do *dataset*

Para começar o trabalho foi primeiro necessário analisar o *dataset*. Analisamos a estrutura do *dataset* (dicionários, listas, strings) e tivemos de descobrir que campos eram obrigatórios). Para tal criamos uma função que ia a cada objeto do dataset e contava os campos que tem. 
```
#Análise de campos

def contarcampos(bd):
    distrib={}
    for d in bd:
        for c in d.keys():
            if c not in distrib:
                distrib[c] = 1
            else:
                distrib[ c] = distrib[ c] + 1
    return distrib

def contarcamposautor(bd):
    distrib={}
    for d in bd:
        for c in d["authors"]:
            for coisa in c.keys():
                if coisa not in distrib:
                    distrib[coisa] = 1
                else:
                    distrib[coisa] = distrib[coisa] + 1
    return distrib

print(contarcampos(database))
print(contarcamposautor(database))
```
```
{'abstract': 3595, 'keywords': 1017, 'authors': 3595, 'doi': 3595, 'pdf': 3533, 'publish_date': 1430, 'title': 3595, 'url': 3595}
{'name': 16408, 'affiliation': 9357, 'orcid': 766}
```
Daqui deduzimos os campos obrigatórios: abstract, authors, doi, title e url; e os não obrigatórios: keywords, pdf, publish_date, affiliation e orcid.

Depois de analisarmos o *dataset*, dividimos o trabalho em três partes o "sistema" que contém as funções de processamento do *dataset*, a interface de linha de comando e a interface gráfica que estão todos em ficheiros separados.

## Funções de processamento do *dataset*

De forma a reutilizar o código para as duas interfaces, criou-se um ficheiro chamado *sistema.py* onde se guardaram todas as funções que processam o *dataset*, desde de carregar/gravar os dados, obter as informações de uma publicação, obter os dados para as distribuições entre outras.

### 1. Carregamento e armazenamento de dados
Começamos por criar as funções de carregar e guardar o *dataset*:
``` 
def carregarBD(fnome):
    f= open(fnome, encoding='utf-8')
    base = json.load(f)
    return base

def guardarBD(fnome,bd): #MUDEI
    fout = open(fnome,"w", encoding='utf-8')
    json.dump(bd, fout, ensure_ascii=False, indent = 4 )
    fout.close()
``` 
### 2. Importação de Dados
Como muitas das funções baseiam-se no facto de haver campos obrigatórios, a função de importar verifica se estes campos estão presentes no ficheiro a importar. Se não, o ficheiro não poderá ser importado. As informações deste ficheiro são depois adicionadas ao *dataset*.
```
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
```
### 3. Criação de publicações
Para criar publicações fizemos funções que recebem os elementos da publicação dados pelo utilizador e depois constroem a estrutura de publicações com eles:

- Função que cria a *string* de keywords:
 ``` 
 def criarKeywords(keywords,palavra):
    if keywords=="":
        keywords=palavra
    else:
        keywords=keywords+", "+palavra
    return keywords
 ``` 
- Função que cria autores:

 ``` 
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
 ``` 
- Função que recebe todas as informações relativas à publicação e cria-a;
 ``` 
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
 ``` 
### 4. Consulta de Publicações:
#### 4.1 Filtros
De seguida tratamos das funções para encontrar uma publicação, e definimos como possíveis procuras os seguintes parâmetros:
 - ID - que nós definimos como os últimos números do DOI;
 ``` 
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
``` 
 - Nome do autor;
``` 
 def consultarpAutor(bd,autor):
    res = []
    for d in bd:
        for a in d['authors']:
            if autor == a['name'].strip(". "):
                res.append(d)
    return res
``` 
 - Afiliação do autor;
 ``` 
def consultarPubAfiliacao(bd, affiliation): 
    res = []
    for post in bd:
        for elem in post.get("authors", []):
            if "affiliation" in elem.keys():
                afil = elem.get("affiliation").lower()
                if affiliation.lower() in afil:
                    if post not in res:
                        res.append(post)
    return res
```
 - Título;
 ``` 
def consultarPubTitulo(bd,titulo):
    res = []
    for post in bd:
        if post.get("title"):
            if titulo.lower() in post["title"].lower():
                res.append(post)
    return res
``` 
 - Palavras-chave esta função também separa palavras-chave que estejam conectadas por "/" ou "(" );
```
def consultarpKeyword(bd,palavras):
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
``` 
 - Data da publicação:
``` 
def consultarpData(bd,data):
    res = []
    for d in bd:
        publish_date = d.get('publish_date')          
        if publish_date and d["publish_date"]!="" and d["publish_date"][0]!=" ":
            publish_date = publish_date[-10:]
            if data == publish_date:
                res.append(d)
    return res
``` 
- A função em baixo foi criada para o caso de não se querer pesquisar por uma data específica, mas sim por uma parte data: por exemplo todas as publicações de 2024. A função recebe a base de dados, um índice baseado no formato da data (Ano-0, Mês-1, Dia-2) e o número do ano,mes ou dia que está pesquisar.
```
def searchbydate(bd,ind,num):
    res=[]
    if len(num)==1:
        num="0"+num
    for pub in bd:
        if "publish_date" in pub.keys():
            if len(pub["publish_date"].split("-"))-1>=ind:
                if pub["publish_date"].split("-")[ind]==num:
                    res.append(pub)
    return res
```

#### 4.2 Eliminar e consultar

Estas duas funções utilizam o ID e a função de encontrar por ID mencionados anteriormente, e depois remove ou retorna essa publicação, respetivamente:
``` 
def elimPub(bd,id):
    ind=encontrarPub(bd,id)
    bd.remove(bd[ind])
    return bd

def consultapID(bd,id):
    return bd[encontrarPub(bd,id)]
``` 

#### 4.3 Ordenar
Em adição a estas funções, criamos uma função que cria uma distribuição de autores pela frequência com que aparecem no *dataset* e outra uma que faz o mesmo paar palavras-chave. Elas são usada caso seja necessário ordenar uma lista de autores ou palavras-chave filtrada.
```
def ordenarMaisArtigos(bd,lista):
    frequencia = {}
    for d in bd:
        for autor in d["authors"]:
            if autor["name"] in lista:
                if autor["name"] in frequencia:
                    frequencia[autor["name"]] = frequencia[autor["name"]] + 1 
                else:
                    frequencia[autor["name"]] = 1
    return frequencia

def keywordsmaisvezes(bd,f_keywords,cond):
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
```
#### 4.4 Visualização
No final para visualizar todas as informações destas publicações todas, criamos uma função que lista todos os conteúdos presentes nelas.
```
def pub(post): 
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
```
### 5. Gráficos e estatísticas

A seguir foram criadas as funções que criam distribuições. As funções todas seguem um padrão:
- acedem a cada publicação; 
- verificam se o campo necessário se encontra lá; 
- criam uma distribuição baseada nos dados das publicações; 
- transformam a distribuição numa lista para a ordenar;
- finalmente alteram a lista para uma distribuição outra vez. 

Como exemplo esta função cria a distribuição de número de publicações por autor:
```
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
```

Esta outra função cria a distribuição do número de publicações de um autor específico, organizadas por ano. Como a data de uma publicação não é obrigatória, como visto na secção **Análise do *dataset***, é criado um campo "Sem data" para os que não tenham data:
```
def AutorporAno(bd,autor): 
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
```

Foram feitas as funções de mostrar gráficos:

- esta função pertence à interface de linha de comando, recebe uma distribuição, calculada por uma das funções acima, e um título e usa os valores para construir o gráfico. A função também usa o *plt.text()* para mostar os valores de cada coluna;
```
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
```
Para a interface gráfica decidimos incluir os gráficos dentro das janelas do *PySimpleGUI*. Para tal, foi necessário criar outra função de mostrar gráficos assim como outras funções auxiliares:

- esta função cria um gráfico igual ao anterior, mas em vez de fazer um *plt.show()* cria uma *figure*;
```
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
```
- a função de desenhar, utiliza a figura criada pela função anterior e insere-a num *Canvas* ( um objeto do *PySimpleGUI* que permite inserir imagens). Se o *Canvas* já tiver uma figura, a função apaga a figura anterior e susbtitui-a.
```
def desenhar(canvas, figura):
    canvas_widget = FigureCanvasTkAgg(figura, canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(side='top', fill='both', expand=1)
    return canvas_widget
```

## Interface de linha de comando
### 1. **Carregar e Salvar Base de Dados**
- Utilizando as funções explicadas anteriormente na secção **Funções de processamento do *dataset*, peermite salvar todas as alterações feitas na base de dados em um arquivo no formato JSON ou carregar os dados existentes desse arquivo. Isso facilita o armazenamento e a continuidade do uso do sistema.
```
database = sistema.carregarBD("Projeto/ata_medica_papers.json") 
sistema.guardarBD("Projeto/ata_medica_papers.json",database)
```
### 2. **Gestão de Publicações**

- Inclui operações para:
  - **Criar publicações**: Adiciona uma nova entrada com detalhes como resumo, palavras-chave, autores, DOI, entre outros. Esta publicação é criada coma função *criarPub*, mencionada em cima e depois adicionada à base de dados.As alterações são imediatamente guardadas no ficheiro para, caso o utilizador feche a aplicação, não se perder as alterações feitas
```
if op1 == '1':
    abstract=input("Resumo: ")
    keywords=""
    npalavras=int(input("Quantas palavras-chave queres adicionar? "))
    while npalavras>0:
        keywords=sistema.criarKeywords(keywords,input("Palavra-chave: "))
        npalavras=npalavras-1
    authors=[]
    nautores=int(input("Quantas autores queres adicionar? "))
    while nautores>0:
        authors.append(sistema.criarAutores(input("Nome: "),input("Afiliação: "), input("orcid: ") ))
        nautores= nautores-1
    doi=input("Doi: ")
    pdf=input("Pdf: ")
    publish_date=f"{input("Ano: ")}-{input("Mês: ")}-{input("Dia: ")}"
    title=input("Título")
    url=input("Url")
    database=sistema.criarPub(database, abstract, keywords, authors, doi, pdf, publish_date, title, url)
    sistema.guardarBD("Projeto/ata_medica_papers.json",database)
```


  - **Consultar publicações**: Localiza uma publicação específica pelo ID, que foi definido como sendo os últimos números do DOI da publicação, retornando os detalhes completos usando a função *pub*.
  
  - **Eliminar publicações**: Remove uma publicação específica com base no ID usando a função *elimPub*.

 - **Filtros**
    Permite consultar publicações específicas com base em critérios como:
      - Nome de autor.
      - Título da publicação.
      - Afiliação do autor.
      - Data de publicação.
      - Palavras-chave associadas à publicação

    Estes filtros funcionam usando as funções de consulta já explicadas. Depois o programa lista o título, data e ID das publicações resultantes da pesquisa. O ID pode depois ser usado na opção de consulta de publicações para ver todos os detalhes.
    Exemplo da filtragem por autor:
```
    elif op13 == '2':
      autor=input("Nome do Autor: ")
      if autor not in sistema.listarautor(database):
          print("Não existe esse autor")
      else:   
          print("Publicações:")
          for pub in sistema.consultarpAutor(database,autor):
              print(f"  Título: {pub["title"]}")
              if "publish_date" in pub.keys():
                  print(f"  Data: {pub["publish_date"]}")
              print(f"  id: {pub["doi"][29:]}\n")
```
### 3. **Distribuições e Estatísticas**
- Realiza análises e cria gráficos sobre os dados disponíveis, como:
  - Determinar as palavras-chave mais frequentes em todas as publicações.
  - Calcular a frequência de palavras-chave por ano.
  - Contar o número de publicações por autor.
  - Analisar a frequência de publicações de um autor ao longo dos anos.
  - Obter estatísticas agregadas de publicações por ano ou por mês.

As análises e gráficos utilizam as funções presentes na secção **5. Gráficos e estatísticas** das **Funções de processamento do *dataset***. O código também analisa caso sejam postos autores não existentes, anos onde não existem palavras-chave e etc., de forma a garantir que o programa não dá erro.

Exemplo do gráfico da frequência de palavras-chave num determinado ano:
```
elif op2 == '2':
    n=input("Número de resultados que deseja? ")
    ano= input("Ano: ")
    if ano not in sistema.anoscompalavras(database):
        print("Esse ano não tem palavras chave")
    else:
        sistema.distribGraficoComando(sistema.PalavraporAno(database,int(n))[ano],f"Frequência de palavras chave de {ano}")
```
### 4.**Listagem de autores**

Utilizando funções de consulta e listagem mencionadas em **Funções de processamento do *dataset***. Os autores são listados em ordem alfabética, com as informações características das suas publicações por baixo do nome. Para facilitar visualização, eles aparecem paginados 5 a 5.
```
elif op == '3':
    resp="P"
    n=4
    i=0
    autoresord=sorted(sistema.listarautor(database))
    while resp!="S":
        while i<n:
            print(autoresord[i])
            print("Publicações:")
            for pub in sistema.consultarpAutor(database,autoresord[i].strip(". ")):
                print(f"  Título: {pub["title"]}")
                if "publish_date" in pub.keys():
                    print(f"  Data: {pub["publish_date"]}")
                print(f"  id: {pub["doi"][29:]}\n")
            i=i+1
        i=n
        n=n+5
        resp=input("""\n
                Próxima página (5): Press(P)
                (Sair: Press(S))
                Resp: """)
        while resp not in["P","S"]:
            print("Resposta inválida")
            resp=input("""\n
                Próxima página (5): Press(P)
                (Sair: Press(S))
                Resp: """)
```
## Interface gráfica

A interface gráfica do programa permite ao utilizador criar, pesquisar e atualizar publicações de uma forma bastante mais interativa que a linha de comando de forma a ser mais fácil ao utilizador realizar estas tarefas. 


### Filtros

Uma das aplicações mais importantes deste programa é a capacidade de permitir ao utilizador pesquisar publicações baseado em informações dadas. Estes filtros incluem título, afiliação, autores, palavras-chave e data. 

Para fazer estes filtros criou-se um dicionário que guarda os valores dos filtros;
```
post_filtro = database
filtro={
    "titulo":"",
    "autor":"",
    "afil":"",
    "ano":"",
    "mes":"",
    "dia":"",
    "keywords": []
    }
```
Cada vez que um filtro é utilizado os valores do objeto filtro são atualizados. O programa deteta sempre que algum caractere foi escrito, de forma a permitir uma pesquisa dinâmica. Exemplos:
```
    if event == "-TITLE-":
        filtro["titulo"]=values["-TITLE-"].strip().lower()

    if event == "-AFIL-":
        filtro["afil"]=values["-AFIL-"].strip().lower()
```

#### Autores e palavras-chave

No caso dos autores e palavras-chave, uma *Listbox* abre para permitir a escolha de um autor ou palavras-chave específicas, tal como a ordenação por ordem alfabética ou frequência. O código em baixo, pertencente ao filtro de autores, demonstra como ele recebe os *inputs* dos eventos gerados pelo utilizador e com funções explicadas previamente ordena a lista de autores existente. O código para o filtro de palavras-chave funciona de uma maneira igual.
```
if event == "-AUTHORS-":
        layout_aut = [
            [sg.InputText("", key="-PQAUTOR-",enable_events=True)],
            [sg.Text("Selecione um autor:", font=("Helvetica", 16))],
            [sg.Listbox(values=listaautores, size=(30, 10), key='-AUTOR-'),sg.Button(' ↕️ ', size= (1,1), font=('Helvetica', 16))],
            [sg.Button("Confirmar"), sg.Button("Sair")],
        ]  
        window_aut = sg.Window("Autores", layout_aut, font=("Helvetica", 16),resizable=True, modal = True)
                        
        stop_aut = False
        cond_alf, cond_frq = True, False
        pqautor = None

        while not stop_aut:
            event_aut, values_aut= window_aut.read()
            if event_aut == sg.WINDOW_CLOSED or event_aut == "Sair":
                stop_aut = True
            
            if event_aut == "-PQAUTOR-":
                search_aut = values_aut["-PQAUTOR-"].lower()
                pqautor = [aut for aut in listaautores if search_aut in aut.lower()]
                window_aut['-AUTOR-'].update(values=pqautor)
            
            if event_aut == " ↕️ ":
                layout_ord_autor1 = [
                    [sg.Text("Ordenar por:")],
                    [sg.Button("Ordem Alfabética")],
                    [sg.Button("Frequência")]
                ]
                ord_autor_window1 = sg.Window("Ordenar", layout_ord_autor1, modal= True)
                                
                ord_autor_stop1 = False
                while not ord_autor_stop1:
                    event_ord_autor1, values_ord_autor1 = ord_autor_window1.read()

                    if event_ord_autor1 == sg.WINDOW_CLOSED:
                        ord_autor_stop1 = True
                                    
                    if event_ord_autor1 == 'Ordem Alfabética':
                        cond_alf = not cond_alf
                        if pqautor:
                            window_aut['-AUTOR-'].update(sorted(pqautor, reverse= cond_alf))
                        else:
                            window_aut['-AUTOR-'].update(sorted(listaautores, reverse= cond_alf))
                        ord_autor_stop1 = True

                    if event_ord_autor1 == 'Frequência':
                        cond_frq = not cond_frq
                        if pqautor:
                            window_aut["-AUTOR-"].update([autor for autor,_ in sorted(sistema.ordenarMaisArtigos(database,pqautor).items(), key = lambda x: x[1], reverse = cond_frq)])
                        else:
                            window_aut["-AUTOR-"].update([autor for autor,_ in sorted(sistema.ordenarMaisArtigos(database,listaautores).items(), key = lambda x: x[1], reverse = cond_frq)])
                        ord_autor_stop1 = True
                ord_autor_window1.close()

            if event_aut == "Confirmar":
                if values_aut["-AUTOR-"]:
                    author = values_aut["-AUTOR-"][0]
                    stop_aut = True
                    filtro["autor"] = values_aut["-AUTOR-"][0]
                    window["-AUTORSELECTED-"].update(values_aut["-AUTOR-"][0])
                else:
                    sg.Popup("Não selecionaste um autor")
        window_aut.close()
```
#### Data:
No caso da data de publicação, a interface gráfica permite uma pesquisa por um ano, mês ou dia específico usando a função *searchbydate* explicada anteriormente. Portanto existe um filtro para ano, mês e dia:
```    
    if event == "-ANO-":
        filtro["ano"]=values["-ANO-"]

    if event == "-MES-":
        filtro["mes"]=values["-MES-"]

    if event == "-DIA-":
        filtro["dia"]=values["-DIA-"]
```
#### Filtragem
Usando as funções mostradas anteriormente na secção **4.1 Filtros**, das Funções de processamento do *dataset*, o programa filtra a base de dados sucessivamente por cada valor no dicionário. Assim, pode-se usar múltiplos filtros ao mesmo tempo o que permite uma pesquisa mais precisa.

```
    if event in ["-CLEARAUTOR-","-CLEARKEYWORD-","-KEYWORD-","-AUTHORS-","-TITLE-","-AFIL-","-ANO-","-MES-","-DIA-"]:
        post_filtro=database
        if filtro["titulo"]!="":
            post_filtro = [post for post in post_filtro if filtro["titulo"] in post["title"].lower()]
        if filtro["autor"]!="":
            post_filtro = sistema.consultarpAutor(post_filtro, filtro["autor"])
        if filtro["afil"]!="":
            post_filtro = sistema.consultarPubAfiliacao(post_filtro, filtro["afil"])
        if filtro["ano"]!="":
            post_filtro = sistema.searchbydate(post_filtro,0, filtro["ano"])
        if filtro["mes"]!="":
            post_filtro = sistema.searchbydate(post_filtro,1, filtro["mes"])        
        if filtro["dia"]!="":
            post_filtro = sistema.searchbydate(post_filtro,2, filtro["dia"])
        if filtro["keywords"]!=[]:
            post_filtro = sistema.consultarpKeyword(post_filtro, filtro["keywords"])

        window["-RESULTS-"].update(values=[post["title"] for post in post_filtro]) 
```
#### Apagar filtros

De forma a não ter de apagar os filtros manualmente, também existem funções que permitem apagar certos filtros, como autores e palavras-chave, ou simplesmente apagar todos os filtros.
```
    if event == "-CLEARAUTOR-":
        window["-AUTORSELECTED-"].update("")
        filtro["autor"]=""

    if event == "-CLEARKEYWORD-":
        window["-KEYWORDSELECTED-"].update("")
        filtro["keywords"]=[]

    if event == "Limpar Filtros":
        post_filtro = database
        window["-RESULTS-"].update([post["title"] for post in post_filtro])
        window["-TITLE-"].update("")
        window["-AFIL-"].update("")
        window["-AUTORSELECTED-"].update("")
        window["-KEYWORDSELECTED-"].update("")
        window["-ANO-"].update("")
        window["-MES-"].update("")
        window["-DIA-"].update("")

        filtro["titulo"]=""
        filtro["autor"]=""
        filtro["afil"]=""
        filtro["ano"]=""
        filtro["mes"]=""
        filtro["dia"]=""
        filtro["keywords"]=[]
```
## Consultar, criar e atualizar publicação

Estas funcionalidades são as mais essenciais numa aplicação de gestão de publicações, mas como são funcionalidades interligadas, decidimos construir a interface para estas de forma similar, de modo a facilitar o seu uso. 

Ao desenhar a função de criar, tivemos de ter em conta que o utilizador não é perfeito e que se pode enganar. Isto é especialmente verdade no caso dos autores e palavras-chave onde o utilizador pode ter de criar longas listas de nomes, afiliações e palavras. 
Assim, um dos maiores objetivos era facilitar a visualização de toda a informação e permitir a alteração dessa informação mesmo depois de inserida.

Portanto a função de criar abre uma janela que contêm todos os campos de uma publicação. No caso do resumo foi inserida uma *Multiline* devido ao tamanho deste campo. Nos autores e keywords foi inserido um *Combobox* e  uma *Multiline*, respetivamente, que permitem a visualização de todos os autores e palavras-chave, assim como botões que permitem a adição, remoção e modificação destas informações.


O código e *layout* da função de atualizar é quase idêntico pois estas funcionalidades são bastante parecidas. As principais diferenças são o facto de os campos já estarem preenchidos (porque a publicação já existe) e alguns campos não poderem ser alterados: título, doi, pdf, url e os nome dos autores.
Ao campo data adiciona-se a data na qual a publicação foi atualizada, de acordo com o *dataset*. Exemplo do *dataset*:
```
"publish_date": "2022-03-07 — Atualizado em 2022-03-07",
"title": "Carcinoma Lobular Pleomorfico Invasivo da Mama Masculina: Um Diagnóstico Raro com Correlação Radio-Patológica",
```

## Gráficos

A criação dos gráficos é feita da mesma maneira que na linha de comando, utilizando as funções que criam distribuições já mencionadas. Neste caso para melhorar a visualização usou-se um *Canvas*, um objeto que permite a integração de gráficos do *Matplotlib* dentro de janelas de *PySimpleGUI*.
Gráficos existentes:
- Publicações por ano;
- Publicações por mês de um determinado ano;
- Autores com mais publicações;
- Publicações de um autor por anos;
- Frequência de palavras-chave;
- Frequência de palavras-chave de um determinado ano.

Exemplo do gráfico das publicações por ano:
```
if event == "Publicações por ano":
    if current_canvas:
        current_canvas.get_tk_widget().pack_forget()
    fig = sistema.distribGrafico(sistema.statsPubAno(database), "Publicações por Ano")
    current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)
```
## Importar, exportar e guardar

 Para estas três funcionalidades simplesmente recorremos às funções de importar e guardar definidas na secção de **Funções de Processamento do *dataset*** , sendo que para exportar foi reutilizada a função de guardar, dando o utilizador o caminho onde guardar a pesquisa efetuada.





















