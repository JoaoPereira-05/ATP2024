

import matplotlib.pyplot as plt

def criarTabmeteo(d):
    res=[]
    while d >0:
        data=(int(input("Ano: ")),int(input("Mês: ")),int(input("Dia: ")))
        minima=(float(input("Temperatura mínima: ")))
        maxima=(float(input("Temperatura máxima: ")))
        pre=(float(input("Precipitação: ")))
        dia=(data,minima,maxima,pre)
        d=d-1
        res.append(dia)
    return res


def medias(tabMeteo):
    res = []
    for dia in tabMeteo:
        data,tempmin,tempmax,precipitacao = dia
        media=(tempmin+tempmax)/2
        res.append((data, media))
    return res

def guardaTabMeteo(t, fnome):
    f = open(fnome, "w")
    for dia in t:
        data,tempmin,tempmax,precipitacao = dia
        f.write(f"{data[0]}-{data[1]}-{data[2]}|{tempmin}|{tempmax}|{precipitacao}\n")
    f.close()
    return f

def carregaTabMeteo(fnome):
    res = []
    file = open(fnome, "r")
    for line in file:
        line = line[:-1] #line = line.strip()
        campos = line.split("|")
        data, min, max, pre = campos
        ano, mes ,dia = data.split("-")
        tuplo = ( (int(ano), int(mes), int(dia)),float(min),float(max),float(pre))
        res.append(tuplo)
    file.close()
    return res

def minMin(tabMeteo):
    minima=tabMeteo[0][2]
    for dia in tabMeteo:
        data, min, max, pre = dia
        if min < minima:
            minima=min
    return minima

def amplTerm(tabMeteo):
    res = []
    for dia in tabMeteo:
        data, min, max, pre = dia
        amp = max-min
        res.append((data,amp))
    return res 

def maxChuva(tabMeteo):
    res=(tabMeteo[0][0],tabMeteo[0][3])
    pre1= (tabMeteo[0][3])
    for dia in tabMeteo:
        data, min, max, pre = dia
        if pre>pre1:
            pre1=pre
            res=(data,pre1)
    return res

def diasChuvosos(tabMeteo, p):
    res=[]
    for dia in tabMeteo:
        data, min, max, pre = dia
        if pre>p:
            res.append((data,pre))
    return res


def maxPeriodoCalor(tabMeteo, p):
    Local_conse=0
    Global_conse=0
    for dia in tabMeteo:
        data, min, max, pre = dia
        if pre<p:
            Local_conse = Local_conse+1
        else:
            if Local_conse > Global_conse:
                Global_conse = Local_conse
            Local_conse=0
    if Local_conse > Global_conse:
                Global_conse = Local_conse
    return Global_conse


def grafTabMeteo(t):
    datas = [f"{ano}-{mes}-{dia}" for (ano,mes,dia),*_ in t]
    temps_min = [min for data,min,*_ in t]
    temps_max = [max for data,min,max,*_ in t]
    pluv = [pre for data,min,max,pre in t]

    plt.plot(datas,temps_min, label="Temp mínima", color="blue", marker=".")
    plt.plot(datas,temps_max,  label="Temp máxima", color="red", marker=".")
    plt.legend()
    plt.xlabel("Data")
    plt.ylabel("Temperatura  ºC")
    plt.title("Temperatura")
    plt.show()
    
    plt.bar(datas,pluv, label="Precipitação", color="g")
    plt.xlabel("Data")
    plt.ylabel("Precipitação mm")
    plt.title("Precipitação")
    plt.show()


opcao = 1
tabMeteo=[]
while opcao != '0':

    print(""" Menu:
            - 1: Criar uma tabela meteorológica;
            - 2: Guardar tabela num ficheiro;
            - 3: Carregar tabela de um ficheiro;
            - 4: Lista de temperaturas médias;
            - 5: Temperatura mínima mais baixa;
            - 6: Amplitude térmica de cada dia;
            - 7: Precipitação máxima;
            - 8: Dias com precipitação acima de um valor;
            - 9: Maior número de dias consecutivos com precipitação abaixo de um valor;
            - 10: Gráficos dos valores da tabela;
            - 0: Sair da aplicação""")
    
    opcao = input("Introduza uma opção: ")

    if opcao=="1":
        tabMeteo=criarTabmeteo(int(input("Número de dias: ")))
    elif opcao=="2":
        guardaTabMeteo(tabMeteo,input("Nome do ficheiro: "))
    elif opcao=="3":
        f=input("Nome do ficheiro: ")
        print(carregaTabMeteo(f))
        tabMeteo=carregaTabMeteo(f)
    elif opcao=="4":
        print(medias(tabMeteo))
    elif opcao=="5":
        print(minMin(tabMeteo))
    elif opcao=="6":
        print(amplTerm(tabMeteo))
    elif opcao=="7":
        print(maxChuva(tabMeteo))
    elif opcao=="8":
        print(diasChuvosos(tabMeteo,float(input("Precipitação mínima: "))))
    elif opcao=="9":
        print(maxPeriodoCalor(tabMeteo,float(input("Precipitação máxima: "))))
    elif opcao=="10":
        grafTabMeteo(tabMeteo)
    elif opcao!="0":
        print("Opção inválida!")


print("Menu fechado.")
