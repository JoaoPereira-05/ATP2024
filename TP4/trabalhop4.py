import random
def criarlista(N):
    return[random.randint(1,101)for num in range(N)]

def leLista(N):
    res = []
    while N>0:
        N=N-1
        num=int(input("Insere o número "))
        res.append(num)
    return res

def somaLista(lista):
   res=0
   for i in lista:
      res=res+i
   return res

def mediaLista(lista):
    res=0
    if len(lista)==0:
        res=0
    else:
        for i in lista:
            res=res+i
        return res/len(lista)

def maiorLista(lista):
    res=lista[0]
    for i in lista:
        if i>res:
            res=i
    return res

def menorLista(lista):
        res=lista[0]
        for i in lista[1:]:
            if i<res:
                res=i
        return res

def estaOrdenadaC(lista):
    i=1
    res="Sim"
    while i<len(lista):
        if lista[i]< lista[i-1]:
          res="Não"
        i=i+1
    return res
    
def estaOrdenadaD(lista):
    i=1
    res="Sim"
    while i<len(lista):
          if lista[i]> lista[i-1]:
            res="Não"
          i=i+1
    return res

def unicos2(lista,elem):
    res=-1
    i=0
    while i < len(lista) and res==-1:
        if lista[i]== elem:
            res=i
        i=i+1
    return res
 

opcao="r"
lista=[]
while opcao!="0":
    print("(1) Criar Lista")
    print("(2) Ler Lista")
    print("(3) Soma")
    print("(4) Média")
    print("(5) Maior")
    print("(6) Menor")
    print("(7) Esta ordenada por ordem crescente?")
    print("(8) Esta ordenada por ordem decrescente?")
    print("(9) Procura um elemento")
    print("(0) Sair")
    opcao=input("Escolhe a opção ")

    if opcao=="1":
        lista=criarlista(int(input("Quantos números? ")))
        print(lista)
    elif opcao=="2":
        lista=leLista(int(input("Quantos números tem a tua lista? ")))
        print(lista)
    elif opcao=="3":
        print(somaLista(lista))
    elif opcao=="4":
        print(mediaLista(lista))
    elif opcao=="5":
        print(maiorLista(lista))
    elif opcao=="6":
        print(menorLista(lista))
    elif opcao=="7":
        print(estaOrdenadaC(lista))
    elif opcao=="8":
        print(estaOrdenadaD(lista))
    elif opcao=="9":
        elem=int(input("Qual elemento? "))
        print(unicos2(lista,elem))
    elif opcao!="0":
        print("Opção inválida!")

print(f"Programa desligado.Lista final: {lista}")

