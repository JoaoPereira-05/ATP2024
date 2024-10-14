def listar(cin):
    i=0
    for sala in cin:
        nlugares, Vendidos, filme, nome= sala
        print(f"Sala: {nome} | Filme: {filme}")
        i=i+1
  
def disponivel(cin, nfilme, lugar):
    cond=False
    for sala in cin:
        nlugares, Vendidos, filme, nome= sala
        if filme == nfilme:
            if lugar not in Vendidos:
                cond=True
    return cond

def vendebilhete( cin, nfilme, lugar ):
    if disponivel(cin, nfilme, lugar):
        for sala in cin:
            nlugares, Vendidos, filme, nome= sala
            if filme == nfilme:
                Vendidos.append(lugar)
    return cin

def listardisponibilidades( cin ):
    i=0
    for sala in cin:
        nlugares, Vendidos, filme, nome= sala
        print(f"Sala:{nome} | Filme: {filme} | Lugares disponíveis: {nlugares-len(Vendidos)}")
        i=i+1

def existeSala( cin, salap ):
    cond=False
    for sala in cin:
        if salap[3]==sala[3]:
            cond=True
    return cond

def inserirSala( cin, sala ):
    if not existeSala( cin, sala ):
        cin.append(sala)
    return cin


def removeSala(cin, nomep):
    for sala in cin:
        nlugares, Vendidos , filme, nome= sala
        if nomep == nome:
            if Vendidos ==[]:
                cin.remove(sala)
            else:
                print("Não se pode retirar esta sala, já existem bilhetes vendidos.")
    return cin


def libertaLugar(cin, nomep, lugar):
    for sala in cin:
        nlugares, Vendidos , filme, nome= sala
        if nomep == nome:
            if lugar in Vendidos:
                Vendidos.remove(lugar)
                print("Bilhete devolvido")
            else:
                print("Esse lugar não estava ocupado")
    return  cin



opcao = 1
cinema=[]
while opcao != '0':

    print(""" Menu:
            (0) Sair
            (1) Reset
            (2) Inserir sala      
            (3) Listar o cinema
            (4) Ver se lugar específico está disponível
            (5) Comprar bilhete
            (6) Ver lugares disponíveis
            (7) Remover sala
            (8) Devolver bilhete        
            """)
    opcao = input("Introduza uma opção: ")

    if opcao=="1":
        cinema=[]
    elif opcao=="2":
        sala=(int(input("Quantos lugares: ")),[],input("Filme: "),input("Nome da sala: "))
        if existeSala(cinema, sala):
            print("Sala já existe.")
        else:
            cinema=inserirSala(cinema,sala)
    elif opcao=="3":
        if cinema==[]:
            print("Cinema vazio")
        else:
            listar(cinema)
    elif opcao=="4":
        if cinema==[]:
            print("Cinema vazio")
        else:
            print(disponivel(cinema,input("Filme? "),int(input("Lugar? "))))
    elif opcao=="5":
        if cinema==[]:
            print("Cinema vazio")
        else:
            filme, lugar = input("Filme? "), int(input("Lugar? "))
            if disponivel(cinema, filme,lugar):
                print("Compra efetuada")
            else:
                print("Lugar já ocupado")
            cinema=vendebilhete(cinema,filme,lugar)
    elif opcao=="6":
        if cinema==[]:
            print("Cinema vazio")
        else:
            listardisponibilidades(cinema)
    elif opcao=="7":
        if cinema==[]:
            print("Cinema vazio")
        else:
            cinema=removeSala(cinema,input("Nome da sala: "))
    elif opcao=="8":
        if cinema==[]:
            print("Cinema vazio")
        else:
            cinema=libertaLugar(cinema,input("Nome da sala: "),int(input("Lugar? ")))

    elif opcao!="0":
        print("Opção inválida!")


print("Menu fechado.")
