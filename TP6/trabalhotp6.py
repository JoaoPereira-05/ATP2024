
def criarturma():
    t=[]
    print("Turma criada")
    return t

def inseriraluno(turma):
    nome = input("Nome do aluno: ")
    id = input("Id do aluno: ")
    nota = [int(input("Nota do TPC: ")),int(input("Nota do Projeto: ")),int(input("Nota do teste: "))]
    al = (nome,id,nota)
    turma.append(al)
    print("Aluno inserido")
    return turma

def listarturma(turma):
        print(f"---------------Turma------------------")
        for al in turma:
            nome,id,nota=al
            print(f"Nome: {nome} Id: {id} Nota de TPC: {nota[0]} Nota de Projeto: {nota[1]} Nota de Teste: {nota[2]}")


def consultaraluno(iden,turma):
    if existealuno(iden,turma):
        for al in turma:
            nome,id,nota=al
            if id== iden:
                i=0
                print(f"""
                        Nome: {nome} 
                        Id: {id} 
                        Nota de TPC: {nota[0]} 
                        Nota de Projeto: {nota[1]} 
                        Nota de Teste: {nota[2]}""")
    else:
        print("Não existe um aluno com esse id")

def existealuno(iden,turma):
    cond = False
    for aluno in turma:
        if aluno[1] == iden:
            cond = True
    return cond

def guardarturma(fnome,turma):
    f= open(fnome, "w")
    i=0
    for al in turma:
        nome,id,nota=al
        f.write(f"{nome}|{id}|{nota[0]}|{nota[1]}|{nota[2]}\n")
    f.close()



def carregarturma(fnome):
    f=open(fnome, "r")
    turma=[]
    for linha in f:
        campos= linha.split("|")
        aluno= (campos[0],campos[1],[int(campos[2]),int(campos[3]),int(campos[4])])
        turma.append(aluno)
    f.close()
    return turma


opcao = 1
turma=[]
while opcao != '0':

    print(""" Menu:
            - 1: Criar uma turma;
            - 2: Inserir um aluno na turma;
            - 3: Listar a turma;
            - 4: Consultar um aluno por id;
            - 5: Guardar a turma em ficheiro;
            - 6: Carregar uma turma dum ficheiro;
            - 0: Sair da aplicação""")
    
    opcao = input("Introduza uma opção: ")

    if opcao=="1":
        turma=criarturma()
    elif opcao=="2":
        turma=inseriraluno(turma)
    elif opcao=="3":
        listarturma(turma)
    elif opcao=="4":
        consultaraluno(input("Id: "),turma)
    elif opcao=="5":
        guardarturma(input("Nome do ficheiro: "),turma)
    elif opcao=="6":
        turma=carregarturma(input("Nome de ficheiro: "))
        print(turma)

    elif opcao!="0":
        print("Opção inválida!")


print("Menu fechado.")
