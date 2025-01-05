import sistema


def menu():
    print("""
---------- Menu ----------
        
(H) Help
(1) Publicação
(2) Análise
(3) Listar Autores 
(4) Import  
(0) Sair
""")
    return

def menu1():
    print("""
(1) Criar
(2) Consultar ID
(3) Consultar por filtros 
(4) Eliminar
(0) Voltar
""")

def menu13():
    print("""
----- Filtros -----
(1) Título
(2) Autor
(3) Afiliação 
(4) Palavra-Chave
(5) Data de Publicação 
(0) Voltar
""")

def menu2():
    print("""
----- Relatório de Estatísticas -----
(1) Frequência Keywords
(2) Palavras do Ano
(3) Publicações por Autor
(4) Quantidade de Publicações de Autor por Ano
(5) Publicações por Ano
(6) Publicações por mês
(0) Voltar
""")

def help():
    print("""
----------- HELP -----------
(1) Publicação
    (1.1) Criar uma Publicação
    (1.2) Consultar uma Publicação através de ID
    (1.3) Consultar Publicações (Título, Autor, Afiliação, Palavra-Chave, Data de Publicação)
    (1.4) Eliminar uma Publicação através de ID
(2) Análise
    (2.1) Frequência Keywords
    (2.2) Palavras do Ano
    (2.3) Publicações por Autor
    (2.4) Quantidade de Publicações de Autor por Ano
    (2.5) Publicações por Ano
    (2.6) Publicações por mês
(3) Listar todos os autores e todas as publicações por cada autor
(4) Importar Publicações, carregar base de dados
""")


database = []
database_file="ata_medica_papers.json"
database = sistema.carregarBD(database_file) 
print("Bem-Vindo! Ata médica carregada com sucesso.")
op = '1'
while op != '0':
    menu()
    op=input("Selecione uma opção: ").upper()
    if op == 'H':
        help()
    elif op == '1':
        op1 = '1'
        while op1 != '0':
            menu1()
            op1=input("Selecione uma opção: ")
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
                sistema.guardarBD("ata_medica_papers.json",database)
            elif op1 == '2':
                id = input("ID:")
                while not sistema.encontrarPub(database,id):
                    print("O ID nao existe")
                    id = input("ID:")
                print(sistema.pub(sistema.consultapID(database,id)))
                
            elif op1 == '3':
                op13 = '1'
                while op13 != '0':
                    menu13()
                    op13=input("Selecione uma opção")
                    if op13 == '1':
                        title = input("Título:")
                        print("Publicações:")
                        for pub in sistema.consultarPubTitulo(database,title):
                            print(f"  Título: {pub["title"]}")
                            if "publish_date" in pub.keys():
                                print(f"  Data: {pub["publish_date"]}")
                            print(f"  id: {pub["doi"][29:]}\n")
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
                    elif op13 == '3':
                        afil = input("Afilição:")
                        print("Publicações:")
                        for pub in sistema.consultarPubAfiliacao(database,afil):
                            print(f"  Título: {pub["title"]}")
                            if "publish_date" in pub.keys():
                                print(f"  Data: {pub["publish_date"]}")
                            print(f"  id: {pub["doi"][29:]}\n")
                    elif op13 == '4':
                        keyword = [input("Palavra-chave:")]
                        print("Publicações:")
                        for pub in sistema.consultarpKeyword(database,keyword):
                            print(f"  Título: {pub["title"]}")
                            if "publish_date" in pub.keys():
                                print(f"  Data: {pub["publish_date"]}")
                            print(f"  id: {pub["doi"][29:]}\n")
                    elif op13 == '5':
                        data = input("Data:")
                        print("Publicações:")
                        for pub in sistema.consultarpData(database,data):
                            print(f"  Título: {pub["title"]}")
                            if "publish_date" in pub.keys():
                                print(f"  Data: {pub["publish_date"]}")
                            print(f"  id: {pub["doi"][29:]}\n")
                    elif op13 != '0':
                        print("Opção não suportada.")
                    sistema.guardarBD(database_file,database)
            elif op1 == '4':
                id = input("ID:")
                while not sistema.encontrarPub(database,id) and sistema.encontrarPub(database,id)!=0:
                    print("O ID nao existe")
                    id = input("ID:")
                database=sistema.elimPub(database,id)
            elif op1 != '0':
                    print("Opção não suportada.")
            sistema.guardarBD(database_file,database)
    elif op == '2':
        op2 = '1'
        while op2 != '0':
            menu2()
            op2=input("Selecione uma opção")

            if op2 == '1':
                n=input("Número de resultados que deseja? ")
                sistema.distribGraficoComando(sistema.TopPalavrasChave(database,int(n)),"Frequência de palavras chave")
            elif op2 == '2':
                n=input("Número de resultados que deseja? ")
                ano= input("Ano: ")
                if ano not in sistema.anoscompalavras(database):
                    print("Esse ano não tem palavras chave")
                else:
                    sistema.distribGraficoComando(sistema.PalavraporAno(database,int(n))[ano],f"Frequência de palavras chave de {ano}")
            elif op2 == '3':
                n=input("Número de resultados que deseja? ")
                sistema.distribGraficoComando(sistema.PubporAutor(database,int(n)),f"Autores com mais publicações ")
            elif op2 == '4':
                autor=input("Nome do Autor: ")
                if autor not in sistema.listarautor(database):
                    print("Não existe esse autor")
                else:    
                    sistema.distribGraficoComando(sistema.AutorporAno(database,autor),f"Publicações por ano de {autor}")
            elif op2 == '5':
                sistema.distribGraficoComando(sistema.statsPubAno(database),"Publicações por ano")
            elif op2 == '6':
                ano=input("Ano: ")
                sistema.distribGraficoComando(sistema.statsPubMes(database,int(ano)),f"Publicações por mês de {ano}")
            elif op2 != '0':
                print("Opção não suportada.")
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

    elif op == '4':
        print(sistema.importar(database,input("Nome do ficheiro")))
    elif op != '0':
            print("Opção não suportada.")
    sistema.guardarBD(database_file,database)

print("Até à próxima!")