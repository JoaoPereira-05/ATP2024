import PySimpleGUI as sg
import sistema
import sisco
import datetime

tema = {
    'BACKGROUND': '#EAEAEA',
    'TEXT': '#004E89',
    'INPUT': '#FFFFFF',
    'TEXT_INPUT': '#5E5E5E',
    'SCROLL': '#A8D5BA',
    'BUTTON': ('#FFFFFF', '#8EC6C5'),
    'PROGRESS': ('#FFFFFF', '#004E89'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

sg.theme_add_new("Projeto", tema)
sg.theme("Projeto")

database = []
database = sistema.carregarBD("ata_medica_papers.json") 

cond_t,cond_d = True,True

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
selected_keywords = []

listaautores = sistema.listarautor(database)

#PARTE GRAFICOSS
anos=sistema.anosexistentes(database)
anospal=sistema.anoscompalavras(database)

frame_filtros = sg.Frame('Filtros', [
                        [   [sg.Text("Afiliação:",font=('Helvetica', 11)),sg.Input(key='-AFIL-', size=(50, 1),font=('Georgia', 11), visible= True,enable_events=True)],
                            [sg.Button("Autor", key="-AUTHORS-",font=('Open Sans', 11), enable_events=True),
                                sg.InputText(key="-AUTORSELECTED-", size=(52, 1),font=('Georgia', 11),enable_events=True,disabled=True),
                                sg.Button("X", key="-CLEARAUTOR-", enable_events=True)],
                            [sg.Text("Ano:",font=('Georgia', 11)),sg.Combo([""]+[str(x) for x in range(2000,2025)],key="-ANO-", size=(5, 1),enable_events=True),
                                sg.Text("Mês:",font=('Georgia', 11)),sg.Combo([""]+[str(x) for x in range(1,13)],key="-MES-", size=(5, 1),enable_events=True),
                                sg.Text("Dia:",font=('Georgia', 11)),sg.Combo([""]+[str(x) for x in range(1,32)],key="-DIA-", size=(5, 1),enable_events=True)],
                            [sg.Button("Keyword", key="-KEYWORD-",font=('Open Sans', 11), enable_events=True),
                                sg.InputText(key="-KEYWORDSELECTED-", size=(49, 1),font=('Georgia', 11),enable_events=True,disabled=True),
                                sg.Button("X", key="-CLEARKEYWORD-", enable_events=True)],
                            [sg.Push(),sg.Button("Limpar Filtros",font=('Open Sans', 11))]
                        ]
                    ],key= "-FILTROS-", font=('Helvetica', 13), relief=sg.RELIEF_GROOVE, visible = False)

frame_pesquisa = sg.Frame("Pesquisa",[
                        [sg.Text("Título:",font=('Helvetica', 11)),sg.Input(key='-TITLE-',font=('Georgia', 11), size=(50, 1), visible= True,enable_events=True),
                        sg.Button("Filtros",font=('Open Sans', 11))],                
                        [sg.Button("Guardar Pesquisa", font=('Open Sans', 11), size=(15, 1)),
                        sg.Button("Criar Publicação", font=('Open Sans', 11), size=(15, 1))]

                ],font=('Helvetica', 13), relief=sg.RELIEF_GROOVE)

layout = [
    [sg.Menu([["ADMIN"]], font=("Source Sans Pro", 10))],
    [sg.Text("Database", font=('Roboto', 14)), 
     sg.Button('Importar', size=(12, 1), font=('Roboto', 12), border_width=2),
     sg.Button('Armazenamento de Dados', font=('Roboto', 12), border_width=2), 
     sg.Push(), 
     sg.Text('PROJETO MAGIK', font=('Montserrat', 30)), 
     sg.Push()],
    [sg.TabGroup([
        [
            sg.Tab('Pesquisa e Gestão', [
                [frame_pesquisa, frame_filtros],
                [sg.Listbox(values=[post['title'] for post in post_filtro], size=(160, 25), key='-RESULTS-', font=('Georgia', 11), enable_events=True,expand_x=True,expand_y=True),
                 sg.Button(" ↕️ ", font=('Helvetica', 18), size=(1, 1))]

            ]),
            sg.Tab('Relatórios Gráficos', [
                [sg.Button("Publicações por ano", font=('Open Sans', 12)), 
                 sg.Button("Publicações por mês de um determinado ano", font=('Open Sans', 12)),
                 sg.Button("Autores com mais publicações", font=('Open Sans', 12))],
                [sg.Button("Publicações de um autor por anos", font=('Open Sans', 12)),
                 sg.Button("Frequência de palavras-chave", font=('Open Sans', 12)),
                 sg.Button("Frequência de palavras-chave de um determinado ano", font=('Open Sans', 12))],
                [sg.Canvas(key='-CANVAS-')]
            ], element_justification="center")
        ]
    ], size=(1920, 1080), font=('Source Sans Pro', 14))]
]



window = sg.Window('PROJETO MAGIK', layout, resizable=True, size=(1920, 1080),finalize=True)

stop_main = False
current_canvas = None

while not stop_main:
    event, values = window.read()
    

    if event == sg.WINDOW_CLOSED:
        stop_main = True
    
    if event == "Filtros":
        filtros_visible = not window['-FILTROS-'].visible
        window['-FILTROS-'].update(visible=filtros_visible)

    if event == " ↕️ ":
            layout_ord = [
                [sg.Text("Ordenar por:",font=('Source Sans Pro', 13))],
                [sg.Button("Título",font=('Open Sans', 11))],
                [sg.Button("Data",font=('Open Sans', 11))]
            ]
            ord_window = sg.Window("Ordenar", layout_ord, modal= True)
            
            ord_stop = False
            while not ord_stop:
                event_ord, values_ord = ord_window.read()

                if event_ord == sg.WINDOW_CLOSED:
                    ord_stop = True
            
                elif event_ord == 'Título':
                    cond_t = not cond_t
                    window['-RESULTS-'].update(sorted([post['title'] for post in post_filtro], reverse= cond_t))
                    ord_stop = True

                elif event_ord == 'Data':
                    cond_d = not cond_d
                    window["-RESULTS-"].update([post['title'] for post in sistema.ordenarData(post_filtro,cond_d)])
                    ord_stop = True
            ord_window.close()

#Filtros

    if event == "-KEYWORD-":
        keywords = sistema.listarKeyword(database)

        layout_kw = [
            [sg.InputText("", key="-PQKEY-",font=('Georgia', 11),size=(44,1), enable_events=True), sg.Text("🔍",font = ("Helvetica",12),pad = (0,0))],
            [sg.Text("Selecione keywords:", font=('Source Sans Pro', 13))],
            [sg.Listbox(values=keywords, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events= True,font=('Georgia', 11), size=(43, 10), key='KEYWORD'), sg.Button(" ↕️ ",font = ("Helvetica",14),size=(1, 1))],
            [sg.Text("Palavras Selecionadas:", font=('Source Sans Pro', 13))],
            [sg.InputText(key="-PALAVRAS-", size=(44, 1),font=('Georgia', 11), readonly= True)],
            [sg.Button("Confirmar",font=('Open Sans', 11)), sg.Button("Sair",font=('Open Sans', 11))]
        ]
        window_kw = sg.Window("KEYWORDS", layout_kw, font=("Helvetica", 10), modal = True)
        pqkeywords = None
        stop_kw = False
        cond_alf, cond_oco = True, False

        while not stop_kw:
            event_kw, values_kw = window_kw.read()
            
            if event_kw == sg.WINDOW_CLOSED or event_kw == "Sair":
                stop_kw = True

            elif event_kw == " ↕️ ":
                layout_ord_kw = [
                    [sg.Text("Ordenar por:",font=('Source Sans Pro', 12))],
                    [sg.Button("Ordem Alfabética",font=('Open Sans', 10))],
                    [sg.Button("Ocorrência", font=('Open Sans', 10))]
                ]
                ord_kw_window = sg.Window("Ordenar", layout_ord_kw, modal= True)
                                
                ord_kw_stop = False

                while not ord_kw_stop:
                    event_ord_kw, values_ord_kw = ord_kw_window.read()

                    if event_ord_kw == sg.WINDOW_CLOSED:
                        ord_kw_stop = True
                    
                    if event_ord_kw == "Ordem Alfabética":
                        cond_alf = not cond_alf
                        if pqkeywords:
                            window_kw['KEYWORD'].update(values=sorted(pqkeywords, reverse= cond_alf))
                        else:
                            window_kw['KEYWORD'].update(values=sorted(keywords,reverse= cond_alf))
                        ord_kw_stop= True

                    if event_ord_kw == 'Ocorrência':
                        cond_oco = not cond_oco
                        if pqkeywords:
                            keywords2 = sistema.keywordsmaisvezes(database,pqkeywords,cond_oco)
                            window_kw['KEYWORD'].update(values=keywords2)
                        else:
                            keywords2 = sistema.keywordsmaisvezes(database,keywords,cond_oco)
                            window_kw['KEYWORD'].update(values=keywords2)
                        ord_kw_stop = True
                ord_kw_window.close()
            
            elif event_kw == "-PQKEY-":
                search_key = values_kw["-PQKEY-"].lower()
                pqkeywords = [key for key in keywords if search_key in key.lower()]
                window_kw['KEYWORD'].update(values=pqkeywords)

            elif event_kw == "Confirmar":
                selected_keywords = values_kw['KEYWORD']
                filtro["keywords"]=values_kw['KEYWORD']
                window['-KEYWORDSELECTED-'].update(", ".join(selected_keywords))
                stop_kw = True

            elif values_kw['KEYWORD']:
                window_kw['-PALAVRAS-'].update(", ".join(values_kw['KEYWORD']))
            else:
                window_kw['-PALAVRAS-'].update("")
        window_kw.close() 
        
    if event == "-AUTHORS-":
        layout_aut = [
            [sg.InputText("", key="-PQAUTOR-",font=('Georgia', 11),size=(36,1),enable_events=True),sg.Text("🔍",font = ("Helvetica",12),pad = (0,0))],
            [sg.Text("Selecione um autor:", font=('Source Sans Pro', 13))],
            [sg.Listbox(values=listaautores,font=('Georgia', 11), size=(35, 10), key='-AUTOR-'),sg.Button(' ↕️ ', size= (1,1), font=('Helvetica', 14))],
            [sg.Button("Confirmar",font=('Open Sans', 11)), sg.Button("Sair",font=('Open Sans', 11))],
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
                    [sg.Text("Ordenar por:",font=('Source Sans Pro', 12))],
                    [sg.Button("Ordem Alfabética",font=('Open Sans', 10))],
                    [sg.Button("Frequência",font=('Open Sans', 10))]
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

    if event == "-TITLE-":
        filtro["titulo"]=values["-TITLE-"].strip().lower()

    if event == "-AFIL-":
        filtro["afil"]=values["-AFIL-"].strip().lower()

    if event == "-CLEARAUTOR-":
        window["-AUTORSELECTED-"].update("")
        filtro["autor"]=""

    if event == "-CLEARKEYWORD-":
        window["-KEYWORDSELECTED-"].update("")
        filtro["keywords"]=[]

    if event == "-ANO-":
        filtro["ano"]=values["-ANO-"]

    if event == "-MES-":
        filtro["mes"]=values["-MES-"]

    if event == "-DIA-":
        filtro["dia"]=values["-DIA-"]

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

#Resultados de pesquisa, atualizar e criar

    if event == '-RESULTS-':
        selected_title = values['-RESULTS-']
        if selected_title:
            post = sistema.buscarPostPorTitulo(database,selected_title[0])
            layout_detalhes = [
                [sg.Text("Detalhes da Publicação", font=('Source Sans Pro', 13), justification="center"),
                    sg.Push(),
                    sg.Button('Atualizar Publicação', font=('Open Sans', 11))],
                [sg.Multiline(sistema.pub(post),font=("Georgia",11), size=(80, 20), disabled= True,key="-PUBDETALHES-")],
                [sg.Button("Fechar",font=('Open Sans', 11))]
            ]
            window_detalhes = sg.Window("Detalhes da Publicação", layout_detalhes,modal=True)

            stop_detalhes = False
            while not stop_detalhes:
                event_detalhes, _ = window_detalhes.read()
                if event_detalhes in (sg.WINDOW_CLOSED, "Fechar"):
                    stop_detalhes = True
                    
                elif event_detalhes=='Atualizar Publicação':
                    pub={}
                    for key ,value in post.items():
                        pub[key]=value

                    if not pub.get("keywords"):
                        pub["keywords"]=""

                    layout2 = [
                                [sg.Text("Título(*):", font=('Helvetica', 11)), sg.InputText(pub["title"],key="-TITULO-",size=(74,1),font=('Georgia', 11),disabled=True)],
                                [sg.Text("Resumo(*):",font=('Helvetica', 11))], 
                                [sg.Multiline(default_text=pub["abstract"],font=('Georgia', 11),key="-RESUMO-",size=(None,5))],
                                [sg.Text("Palavras-chave:",font=('Helvetica', 11))], 
                                [sg.InputText(key="-PALAVRAS-",font=('Open Sans', 11),size=(58, 2)), sg.Button("Adicionar palavra",font=('Open Sans', 11))],
                                [sg.Multiline(default_text=pub["keywords"],font=('Georgia', 11), key= "-PsCHAVE-",size=(65, 2), disabled= True),sg.Button("Remover palavra",font=('Open Sans', 11))],
                                [sg.Text("Data de publicação:",font=('Helvetica', 11))],
                                [sg.Input(pub.get("publish_date"),key="-DATASELECTED-",font=('Open Sans', 11),disabled=True,size=(12,1))],
                                [sg.Text("Autor(*):",font=('Helvetica', 11))],
                                [sg.Combo(values=[autor["name"] for autor in pub["authors"]],font=('Georgia', 11),key="-AUTORES-",readonly=True,size=(37,1))],
                                [sg.Button("Adicionar autor",font=('Open Sans', 11)),sg.Button("Modificar autor",font=('Open Sans', 11)),sg.Button("Remover autor",font=('Open Sans', 11))],
                                [sg.Text("doi(*):",font=('Helvetica', 11)), sg.InputText(pub["doi"],key="-DOI-",font=('Georgia', 11),disabled=True,size=(75,1))],
                                [sg.Text("pdf:",font=('Helvetica', 11)), sg.InputText(pub.get("pdf"),key="-PDF-",font=('Georgia', 11),disabled=True,size=(75,1))],
                                [sg.Text("url(*):",font=('Helvetica', 11)), sg.InputText(pub.get("url"),key="-URL-",font=('Georgia', 11),disabled=True,size=(75,1))],
                                [sg.Button("Atualizar",font=('Open Sans', 11)), sg.Button("Cancelar",font=('Open Sans', 11)),sg.Push(),sg.Text("* Campo obrigatório",font=('Helvetica', 11))]
                            ]
                    window_atualizar=sg.Window("Atualizar publicação", layout2, font=("Helvetica", 16),modal=True)
                    stop_atualizar = False
                    while not stop_atualizar:
                        event_at, values_at = window_atualizar.read()
                            
                        if event_at == sg.WINDOW_CLOSED or event_at == "Cancelar":
                            stop_atualizar=True

                        else:
                            pub["abstract"] = values_at["-RESUMO-"]

                            if event_at=="Adicionar palavra" and values_at["-PALAVRAS-"]!="":
                                pub["keywords"]=sistema.criarKeywords(pub["keywords"],values_at["-PALAVRAS-"])
                                window_atualizar["-PALAVRAS-"].update("")
                                window_atualizar["-PsCHAVE-"].update(pub["keywords"])
                                    
                            if event_at=="Remover palavra":
                                if "keywords" not in pub.keys():
                                    sg.Popup("Esta publicação não tem palavras-chave.")
                                else:
                                    layoutpal=[[sg.Listbox(values=pub["keywords"].split(", "),font=('Georgia', 11),key="-PALREMOVE-",size=(35,10),select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                                    [sg.Button("Confirmar",font=('Open Sans', 11)),sg.Button("Sair",font=('Open Sans', 11))]]

                                    window_rempal=sg.Window("Remover palavras",layoutpal,font=("Helvetica", 16),modal=True)
                                    stop_rempal=False
                                    while not stop_rempal:
                                        event_rempal, values_rempal = window_rempal.read()

                                        if event_rempal == sg.WINDOW_CLOSED or event_rempal == "Sair":
                                            stop_rempal=True
                                            window_rempal.close()
                                        elif event_rempal =="Confirmar":
                                            current_pals=pub["keywords"].split(", ")
                                            novaspals=[]
                                            for pal in current_pals:
                                                if pal not in values_rempal["-PALREMOVE-"]:
                                                    novaspals.append(pal)

                                            keywords=""
                                            for pal in novaspals:
                                                keywords=sistema.criarKeywords(keywords,pal)

                                            pub["keywords"]=keywords
                                            window_atualizar["-PsCHAVE-"].update(pub["keywords"])
                                            window_rempal["-PALREMOVE-"].update(keywords.split(", "))

                            if event_at=="Adicionar autor":
                                layout_naut=[[sg.Text("Nome:",font=('Helvetica', 11)),sg.Input("",font=('Georgia', 11),key="-NOVONOME-")],
                                            [sg.Text("Afiliação:",font=('Helvetica', 11)),sg.Multiline("",key="-NOVAAFIL-",font=('Georgia', 11),size=(36,4))],
                                            [sg.Text("Orcid:",font=('Helvetica', 11)),sg.Input("",font=('Georgia', 11),key="-NOVOORCID-")],
                                            [sg.Button("Confirmar",font=('Open Sans', 11)),sg.Button("Sair",font=('Open Sans', 11))]]
                                window_naut=sg.Window("Adicionar Autor",layout_naut, font=("Helvetica", 16),modal=True)

                                stop_naut=False
                                while not stop_naut:
                                    event_naut, values_naut = window_naut.read()
                                    
                                    if event_naut == sg.WINDOW_CLOSED or event_naut == "Sair":
                                        stop_naut=True
                                    elif event_naut == "Confirmar" and values_naut["-NOVONOME-"]!="":
                                        pub["authors"].append(sistema.criarAutores(values_naut["-NOVONOME-"],values_naut["-NOVAAFIL-"],values_naut["-NOVOORCID-"]))
                                        stop_naut = True
                                        window_atualizar["-AUTORES-"].update(values=[autor["name"] for autor in pub["authors"]])

                                window_naut.close()

                            if event_at== "Modificar autor" and not values_at["-AUTORES-"]:
                                sg.Popup("Não selecionaste um autor")
                            elif event_at== "Modificar autor":
                                for autor in pub["authors"]:
                                    if autor["name"] == values_at["-AUTORES-"]:
                                        autmod=autor

                                layout_mod=[[sg.Text("Nome:",font=('Helvetica', 11)),sg.Input(autmod["name"],font=('Georgia', 11),key="-NOMEMOD-",disabled=True)],
                                            [sg.Text("Afiliação:",font=('Helvetica', 11)),sg.Multiline(autmod.get("affiliation"),font=('Georgia', 11),key="-AFILMOD-",size=(36,4))],
                                            [sg.Text("Orcid:",font=('Helvetica', 11)),sg.Input(autmod.get("orcid"),font=('Georgia', 11),key="-ORCIDMOD-")],
                                            [sg.Button("Confirmar",font=('Open Sans', 11)),sg.Button("Sair",font=('Open Sans', 11))]]
                                window_mod=sg.Window("Modificar autor",layout_mod, font=("Helvetica", 16),modal=True)

                                stop_mod=False
                                while not stop_mod:
                                    event_mod, values_mod = window_mod.read()
                            
                                    if event_mod == sg.WINDOW_CLOSED or event_mod == "Sair":
                                        stop_mod=True
                    
                                    elif event_mod=="Confirmar":

                                        if values_mod["-AFILMOD-"]!="":
                                            autmod["affiliation"]=values_mod["-AFILMOD-"]

                                        if values_mod["-ORCIDMOD-"]!="":
                                            autmod["orcid"]=values_mod["-ORCIDMOD-"]

                                        for autor in pub["authors"]:
                                            if autor["name"] == values_mod["-NOMEMOD-"]:
                                                for key,value in autmod.items():
                                                    autor[key]=value
                                        stop_mod=True
                                window_mod.close()

                            if event_at=="Remover autor" and not values_at["-AUTORES-"]:
                                sg.Popup("Não selecionaste um autor")
                            elif event_at=="Remover autor":
                                for autor in pub["authors"]:
                                    if autor["name"] == values_at["-AUTORES-"]:
                                        pub["authors"].remove(autor)
                                window_atualizar["-AUTORES-"].update(values=[autor["name"] for autor in pub["authors"]])

                            if event_at=="Atualizar":
                                if not pub.get("publish_date"):
                                    pub["publish_date"]= f" — Atualizado em {str(datetime.datetime.today()).split()[0]}"
                                else:
                                    pub["publish_date"]= pub["publish_date"] + f" — Atualizado em {str(datetime.datetime.today()).split()[0]}"
                                
                                stop_atualizar=True

                                for key ,value in pub.items():
                                    post[key]=value
                                window_detalhes["-PUBDETALHES-"].update(sistema.pub(post))
                                
                                listaautores = sistema.listarautor(database)
                                anos=sistema.anosexistentes(database)
                                anospal=sistema.anoscompalavras(database)
                    
                    window_atualizar.close()
                    
            window_detalhes.close() 
            
        else:
            sg.popup("Nenhum titulo foi selecionado")
    
    if event == 'Criar Publicação':
        layout1 = [
                    [sg.Text("Título(*):", font=('Helvetica', 11)), sg.InputText(key="-TITULO-",size=(76 ,1),font=('Georgia', 11))],
                    [sg.Text("Resumo(*):",font=('Helvetica', 11))], 
                    [sg.Multiline(font=('Georgia', 11),key="-RESUMO-",size=(None,5))],
                    [sg.Text("Palavras-chave:",font=('Helvetica', 11))], 
                    [sg.InputText(key="-PCHAVE-",font=('Georgia', 11),size=(52, 2)), sg.Button("Adicionar palavra",font=('Open Sans', 11))],
                    [sg.Multiline("",font=('Georgia', 11), key= "-PsCHAVE-",size=(65, 2), disabled= True),sg.Button("Remover palavra",font=('Open Sans', 11))],
                    [sg.Text("Data de publicação:",font=('Helvetica', 11))],
                    [sg.Button("Escolher data",font=('Open Sans', 11)),sg.Input("",key="-DATASELECTED-",readonly=True,font=('Georgia', 11),size=(10,1)),sg.Button("Remover data",font=('Open Sans', 11))],
                    [sg.Text("Autor(*):",font=('Helvetica', 11))],
                    [sg.Combo(values=[],font=('Helvetica', 11),key="-AUTORES-",readonly=True,size=(41,1))],
                    [sg.Button("Adicionar autor",font=('Open Sans', 11)),sg.Button("Modificar autor",font=('Open Sans', 11)),sg.Button("Remover autor",font=('Open Sans', 11))],
                    [sg.Text("doi(*):",font=('Helvetica', 11)), sg.InputText(key="-DOI-",font=('Georgia', 11),size=(77,1))],
                    [sg.Text("pdf:",font=('Helvetica', 11)), sg.InputText(key="-PDF-",font=('Georgia', 11),size=(77,1))],
                    [sg.Text("url(*):",font=('Helvetica', 11)), sg.InputText(key="-URL-",font=('Georgia', 11),size=(77,1))],
                    [sg.Button("Criar",font=('Open Sans', 11)), sg.Button("Cancelar",font=('Open Sans', 11)),sg.Push(),sg.Text("* Campo obrigatório",font=('Helvetica', 11))]
        ]

        window_npub = sg.Window("Nova publicação",layout1,font="Helvetica",modal=True)
        new_keywords=""
        data=""
        autores=[]
        user={
            "abstract":"",
            "keywords":"",
            "authors":[],
            "doi":"",
            "url":"",
            "pdf":"",
            "publish_date":"",
            "title":""
        }
        stop_npub = False
        while not stop_npub:
            event_npub, values_npub = window_npub.read()
            
            if event_npub == sg.WINDOW_CLOSED or event_npub == "Cancelar":
                stop_npub = True

            else:

                user["abstract"] = values_npub["-RESUMO-"]

                if event_npub=="Adicionar palavra" and values_npub["-PCHAVE-"]!="":

                    new_keywords=sistema.criarKeywords(new_keywords,values_npub["-PCHAVE-"])
                    window_npub["-PCHAVE-"].update("")
                    window_npub["-PsCHAVE-"].update(new_keywords)
                    
                    user["keywords"]=new_keywords
                
                if event_npub=="Remover palavra":
                    layoutpal=[[sg.Listbox(values=user["keywords"].split(", "),key="-PALREMOVE-",font=('Georgia', 11),size=(35,10),select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                    [sg.Button("Confirmar",font=('Open Sans', 11)),sg.Button("Sair",font=('Open Sans', 11))]]

                    window_rempal=sg.Window("Palavras-chave",layoutpal,font=("Helvetica", 16),modal=True)
                    stop_rempal=False
                    while not stop_rempal:
                        event_rempal, values_rempal = window_rempal.read()

                        if event_rempal == sg.WINDOW_CLOSED or event_rempal == "Sair":
                            stop_rempal=True
                            window_rempal.close()
                        elif event_rempal =="Confirmar":
                            current_pals=user["keywords"].split(", ")
                            novaspals=[]
                            for pal in current_pals:
                                if pal not in values_rempal["-PALREMOVE-"]:
                                    novaspals.append(pal)

                            keywords=""
                            for pal in novaspals:
                                keywords=sistema.criarKeywords(keywords,pal)

                            user["keywords"]=keywords
                            window_npub["-PsCHAVE-"].update(user["keywords"])
                            window_rempal["-PALREMOVE-"].update(keywords.split(", "))

                if event_npub=="Adicionar autor":
                    layout_naut=[[sg.Text("Nome:",font=('Helvetica', 11)),sg.Input("",font=('Georgia', 11),key="-NOVONOME-")],
                                [sg.Text("Afiliação:",font=('Helvetica', 11)),sg.Multiline("",key="-NOVAAFIL-",font=('Georgia', 11),size=(36,4))],
                                [sg.Text("Orcid:",font=('Helvetica', 11)),sg.Input("",font=('Georgia', 11),key="-NOVOORCID-")],
                                [sg.Button("Confirmar",font=('Open Sans', 11)),sg.Button("Sair",font=('Open Sans', 11))]]
                    
                    window_naut=sg.Window("Adicionar Autor",layout_naut, font=("Helvetica", 16),modal=True)

                    stop_naut=False
                    while not stop_naut:
                        event_naut, values_naut = window_naut.read()
                        
                        if event_naut == sg.WINDOW_CLOSED or event_naut == "Sair":
                            stop_naut=True
                        elif event_naut == "Confirmar" and values_naut["-NOVONOME-"]!="":
                            autores.append(sistema.criarAutores(values_naut["-NOVONOME-"],values_naut["-NOVAAFIL-"],values_naut["-NOVOORCID-"]))
                            user["authors"]=autores
                            stop_naut = True
                            window_npub["-AUTORES-"].update(values=[autor["name"] for autor in user["authors"]])

                    window_naut.close()
                    
                if event_npub== "Modificar autor" and not values_npub["-AUTORES-"]:
                    sg.Popup("Não selecionaste um autor")
                elif event_npub== "Modificar autor":
                    for autor in user["authors"]:
                        if autor["name"] == values_npub["-AUTORES-"]:
                            autmod=autor

                    layout_mod=[[sg.Text("Nome:",font=('Helvetica', 11)),sg.Input(autmod["name"],font=('Georgia', 11),key="-NOMEMOD-",disabled=True)],
                                [sg.Text("Afiliação:",font=('Helvetica', 11)),sg.Multiline(autmod.get("affiliation"),font=('Georgia', 11),key="-AFILMOD-",size=(36,4))],
                                [sg.Text("Orcid:",font=('Helvetica', 11)),sg.Input(autmod.get("orcid"),font=('Georgia', 11),key="-ORCIDMOD-")],
                                [sg.Button("Confirmar",font=('Open Sans', 11)),sg.Button("Sair",font=('Open Sans', 11))]]
                    window_mod=sg.Window("Modificar autor",layout_mod, font=("Helvetica", 16),modal=True)

                    stop_mod=False
                    while not stop_mod:
                        event_mod, values_mod = window_mod.read()
                
                        if event_mod == sg.WINDOW_CLOSED or event_mod == "Sair":
                            stop_mod=True
        
                        elif event_mod=="Confirmar":
                            if values_mod["-NOMEMOD-"]=="":
                                sg.Popup("Campo nome obrigatório")
                            else:
                                autmod["name"]=values_mod["-NOMEMOD-"]
                            if values_mod["-AFILMOD-"]!="":
                                autmod["affiliation"]=values_mod["-AFILMOD-"]
                            if values_mod["-ORCIDMOD-"]!="":
                                autmod["orcid"]=values_mod["-ORCIDMOD-"]
                            for autor in user["authors"]:
                                if autor["name"] == values_mod["-NOMEMOD-"]:
                                    for key,value in autmod.items():
                                        autor[key]=value
                            stop_mod=True
                    window_mod.close()

                if event_npub=="Remover autor" and not values_npub["-AUTORES-"]:
                    sg.Popup("Não selecionaste um autor")

                elif event_npub=="Remover autor":
                    for autor in user["authors"]:
                        if autor["name"] == values_npub["-AUTORES-"]:
                            user["authors"].remove(autor)
                    window_npub["-AUTORES-"].update(values=[autor["name"] for autor in user["authors"]])

                user["doi"] = values_npub["-DOI-"]
                user["pdf"] = values_npub["-PDF-"]

                if event_npub =="Escolher data":
                    layout_data = [
                    [sg.Text("Selecione uma Data:",font=('Helvetica', 11))],
                    [sg.CalendarButton("Escolher Data", target="-DATA-", format="%Y-%m-%d",font=('Open Sans', 11), key= "CALENDARIO")],
                    [sg.InputText("", key="-DATA-", size=(20, 1),font=('Geogia', 11), readonly=True)],
                    [sg.Button("Confirmar",font=('Open Sans', 11)), sg.Button("Cancelar",font=('Open Sans', 11))],
                    ]
                    window_data = sg.Window("Calendário", layout_data, modal=True)

                    data_stop = False
                    while not data_stop:
                        event_data, values_data = window_data.read()

                        if event_data in (sg.WINDOW_CLOSED, "Cancelar"):
                            data_stop = True
                        elif event_data == "Confirmar":
                            user["publish_date"] = values_data["-DATA-"]
                            data_stop = True
                            window_npub["-DATASELECTED-"].update(values_data["-DATA-"])
                    window_data.close()

                if event_npub=="Remover data":
                    user["publish_date"]=""
                    window_npub["-DATASELECTED-"].update("")
                
                user["title"]=values_npub["-TITULO-"]
                user["url"]= values_npub["-URL-"]

                if event_npub == "Criar":
                    if user["title"]=="" or user["authors"]==[] or user["doi"]=="" or user["abstract"]=="" or user["url"]=="":
                        sg.Popup("Preencha todos os campos obrigatórios!")
                    else:
                        database=sistema.criarPub(database, user["abstract"], user["keywords"], user["authors"], user["doi"], user["pdf"], user["publish_date"], user["title"], user["url"])
                        listaautores = sistema.listarautor(database)
                        anos=sistema.anosexistentes(database)
                        anospal=sistema.anoscompalavras(database)
                        post_filtro = database
                        stop_npub=True
        window["-RESULTS-"].update([post["title"] for post in post_filtro])
        window_npub.close()
                           
    elif event == 'Importar':
        layout_imp = [
            [sg.Text("Selecione o ficheiro JSON:", size=(20, 1),font=('Helvetica', 11))], 
            [sg.Input(key="-FILE-", enable_events=True, size=(40, 1),pad=(None,0),), 
            sg.FileBrowse(button_text="🔍", size=(4, 1),pad=(0,0),font=('Helvetica', 9),file_types=((('Ficheiros JSON', '*.json'),)))],
            [sg.Button("Importar", key="-IMPORT-",font=('Open Sans', 11)), sg.Button("Sair",font=('Open Sans', 11))]
        ]

        window_imp = sg.Window("Importar Ficheiro JSON", layout_imp, modal= True)

        stop_imp = False
        while not stop_imp:
            event_imp, values_imp = window_imp.read()

            if event_imp == sg.WINDOW_CLOSED or event_imp == "Sair":
                stop_imp = True
            
            if event_imp == "-IMPORT-":
                ficheiro = values_imp["-FILE-"]
                if ficheiro:
                    resultado = sistema.importar(database, ficheiro)
                    if resultado != "Ficheiro não suportado":
                        database = sistema.importar(database, ficheiro)
                        post_filtro = database
                        window["-RESULTS-"].update([post["title"] for post in post_filtro])
                        stop_imp = True
                        listaautores = sistema.listarautor(database)
                        anos=sistema.anosexistentes(database)
                        anospal=sistema.anoscompalavras(database)

                    else:
                        sg.popup_error("Por favor, selecione um ficheiro válido!", title="Erro")
                else:
                    sg.popup_error("Por favor, selecione um ficheiro válido!", title="Erro")

        window_imp.close()

    elif event == "Armazenamento de Dados":
        sistema.guardarBD("ata_medica_papers.json",database)

    elif event == "Guardar Pesquisa":
        layout_gp = [
            [sg.Text("Escolha o nome do ficheiro:",font=('Helvetica', 11))],
            [sg.InputText(key="-FNOME-",font=('Geogia', 11), size=(40,1))],
            [sg.Text("Escolha a pasta para guardar o ficheiro:",font=('Helvetica', 11))],
            [sg.InputText(key="-PASTA-", enable_events=True,font=('Geogia', 11),size=(36,1),pad=(None,0)), sg.FolderBrowse("🔍", size=(4,0),font=('Helvetica', 9), pad=(0,0))],
            [sg.Button("Guardar",font=('Open Sans', 11)), sg.Button("Cancelar",font=('Open Sans', 11))]
        ]
        
        window_gp = sg.Window("Guardar Pesquisa", layout_gp, modal= True)

        stop_gp = False
        while not stop_gp:
            event_gp, values_gp= window_gp.read()

            if event_gp == sg.WINDOW_CLOSED or event_gp ==  "Cancelar":
                stop_gp = True

            if event_gp == "Guardar":
                nome_ficheiro = values_gp["-FNOME-"]
                pasta = values_gp["-PASTA-"]
                
                if pasta == "":
                    sg.popup("Por favor, selecione uma pasta válida.")
               
                else:
                    caminho_completo = pasta + "/" + nome_ficheiro + ".json"
                    sistema.guardarBD(caminho_completo, post_filtro)
                    stop_gp = True
        window_gp.close()

    elif event == "ADMIN":
        
        layout_login = [
            [sg.Text('''
    ''')],
            [sg.InputText('Nome de Utilizador',font=('Helvetica', 11), key='UTILIZADOR', text_color='grey', enable_events=True)],
            [sg.InputText('Palavra-Passe',font=('Helvetica', 11), key='PASSWORD', text_color='grey', enable_events=True)],
            [sg.Button('Entrar',font=('Open Sans', 11)), sg.Button('Sair',font=('Open Sans', 11))]
        ]

        window_login = sg.Window("LOGIN ADMIN", layout_login, resizable=False, size=(400,200), element_justification='center', finalize=True, modal=True)

        fundo_ut = 'Nome de Utilizador'
        fundo_ativo_ut = True
        fundo_ps = 'Palavra-Passe'
        fundo_ativo_ps = True

        stop_login = False
        abrir = None
        while not stop_login:
            event_login,values_login = window_login.read()

            if event_login in (sg.WINDOW_CLOSED,"Sair"):
                stop_login = True

            if event_login == 'UTILIZADOR':
                if fundo_ativo_ut:
                    window_login['UTILIZADOR'].update('', text_color='black')
                    fundo_ativo_ut = False
                elif not values_login['UTILIZADOR']:
                    window_login['UTILIZADOR'].update(fundo_ut, text_color='grey')
                    fundo_ativo_ut = True

            if event_login == 'PASSWORD':
                if fundo_ativo_ps:
                    window_login['PASSWORD'].update('', text_color='black', password_char='*')
                    fundo_ativo_ps = False
                elif not values_login['PASSWORD']:
                    window_login['PASSWORD'].update(fundo_ps, text_color='grey', password_char='')
                    fundo_ativo_ps = True

            if event_login == 'Entrar':
                admin = values_login['UTILIZADOR']
                password = values_login['PASSWORD']
                if admin == "Admin" and password == "Admin":
                    stop_login = True
                    abrir = True
                else:
                    falhou = [
                        [sg.Text('Nome de utilizador ou palavra passe inválida!')],
                        [sg.Button('Tentar Novamente')], [sg.Button('Sair')]
                    ]
                    window_falhou = sg.Window("FALHA", falhou, resizable=False, size=(400,200), element_justification='center', finalize=True,modal= True)

                    event_falhou,values_falhou = window_falhou.read()

                    if event_falhou == 'Tentar Novamente':
                        window_falhou.close()
                    elif event_falhou == 'Sair' or event_falhou == sg.WIN_CLOSED:
                        window_falhou.close()
                        stop_login = False
                        abrir = False
        window_login.close()
        
        if abrir:
            layout_menu = [
                [sg.Button("Publicações", key="-PUBS-", size=(20,1))],
                [sg.Button("Análise", key="-ANALISE-", size=(20,1))],
                [sg.Button("Listar Autores", key="-LISTARAUTOR-", size=(20,1))],
                [sg.Button("Import", key="-IMPORT-", size=(20,1))],
                [sg.Button("Guardar", key="-GUARDAR-", size=(20,1))],
                [sg.Button("Voltar", key="-VOLTAR-", size=(20,1))]
            ]

            layout_admin = [
                [sg.Frame("", layout_menu, font=("Helvetica", 12), pad=(10, 10), size=(180, 670), border_width=0),
                sg.VerticalSeparator(),
                sg.Column([
                    [sg.Frame("HELP", [
                        [sg.Column([
                            [sg.Text(sisco.ajuda(), key="-FRAME2_TEXT-", auto_size_text=True)]],
                            scrollable=True, vertical_scroll_only=True, size=(1200, 670))]
                ], border_width=0)]
                ])
                ]
            ]

            window_admin = sg.Window("Projeto Magic - Menu", layout_admin, size=(1920, 1080),resizable= True, modal= True)

            stop_admin = False

            while not stop_admin:
                event_admin, values_admin = window_admin.read()
                if event_admin == sg.WINDOW_CLOSED:
                    stop_admin = True
                if event_admin == "-PUBS-":
                    klik = sisco.publicacoes(window_admin, database)
                    if klik == "-CRIAR-":
                        sisco.criarPub_InterfaceGraf(window_admin, database)
                    if klik == "-CONS_ID-":
                        sisco.consulta_por_id_interface(window_admin, database)
                if event_admin == "-ANALISE-":
                    sisco.analise_interface(window_admin, database)
                if event_admin == "-LISTARAUTOR-":
                    sisco.lista_autores_interface(window_admin, database)
                if event_admin == "-IMPORT-":
                    sisco.interface_importar(window_admin,database)
                if event_admin == "-GUARDAR-":
                    sisco.interface_guardar(window_admin, database)
                if event_admin == "-VOLTAR-":
                    stop_admin = True
                    
            window_admin.close()

#Parte dos gráficos    

    if event == "Publicações por ano":
        if current_canvas:
            current_canvas.get_tk_widget().pack_forget()
        fig = sistema.distribGrafico(sistema.statsPubAno(database), "Publicações por Ano")
        current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)

    if event == "Publicações por mês de um determinado ano":
            layout2 = [
                [sg.Text("Selecione um ano:", font=('Source Sans Pro', 13))],
                [sg.Listbox(values=anos, size=(13, 7), key="-ANO-",font=('Georgia', 11))],
                [sg.Button("Confirmar",font=('Open Sans', 11)), sg.Button("Sair",font=('Open Sans', 11))],
            ]
            window2 = sg.Window("Anos", layout2, font=("Helvetica", 16),resizable=True, modal = True)
                            
            stop2 = False
            while not stop2:
                event2, values2= window2.read()
                if event2 == sg.WINDOW_CLOSED or event2 == "Sair":
                    stop2 = True
                if event2 == "Confirmar":
                    if values2["-ANO-"]:
                        ano=values2["-ANO-"][0]
                        if current_canvas:
                            current_canvas.get_tk_widget().pack_forget()
                        fig = sistema.distribGrafico(sistema.statsPubMes(database,int(ano)),f"Publicações por mês de {ano}")
                        current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)
                    else:
                        sg.Popup("Não selecionaste um ano")
            window2.close()

    if event == "Autores com mais publicações":
        if current_canvas:
            current_canvas.get_tk_widget().pack_forget()
        fig = sistema.distribGrafico(sistema.PubporAutor(database,20), "Autores com mais publicações")
        current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)

    if event== "Publicações de um autor por anos":
        layout3 = [
            [sg.InputText("", key="-PQAUTOR2-",font=('Georgia', 11),size=(36,1),enable_events=True),sg.Text("🔍",font = ("Helvetica",12),pad = (0,0))],
            [sg.Text("Selecione um autor:", font=('Source Sans Pro', 13))],
            [sg.Listbox(values=listaautores,font=('Georgia', 11), size=(35, 10), key='-AUTOR2-'),sg.Button(' ↕️ ', size= (1,1), font=('Helvetica', 14))],
            [sg.Button("Confirmar",font=('Open Sans', 11)), sg.Button("Sair",font=('Open Sans', 11))],
        ]    
        window3 = sg.Window("Autores", layout3, font=("Helvetica", 16),resizable=True, modal = True)

        pqautor2=""                
        stop3 = False
        cond_alf, cond_frq = True, False

        while not stop3:
            event3, values3= window3.read()
            if event3 == sg.WINDOW_CLOSED or event3 == "Sair":
                stop3 = True
            if event3 == "Confirmar":
                if values3["-AUTOR2-"]:
                    autor=values3["-AUTOR2-"][0]
                    if current_canvas:
                        current_canvas.get_tk_widget().pack_forget()
                    fig = sistema.distribGrafico(sistema.AutorporAno(database,autor),f"Publicações por ano de {autor}")
                    current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)
                else:
                    sg.Popup("Não selecionaste um autor")

            if event3 == "-PQAUTOR2-":
                search_aut2 = values3["-PQAUTOR2-"].lower()
                pqautor2 = [aut for aut in listaautores if search_aut2 in aut.lower()]
                window3['-AUTOR2-'].update(values=pqautor2)

            if event3 == " ↕️ ":
                layout_ord_autor2 = [
                    [sg.Text("Ordenar por:",font=('Source Sans Pro', 12))],
                    [sg.Button("Ordem Alfabética",font=('Open Sans', 10))],
                    [sg.Button("Frequência",font=('Open Sans', 10))]
                ]
                ord_autor_window2 = sg.Window("Ordenar", layout_ord_autor2, modal= True)
                                
                ord_autor_stop2 = False
                while not ord_autor_stop2:
                    event_ord_autor2, values_ord_autor2 = ord_autor_window2.read()

                    if event_ord_autor2 == sg.WINDOW_CLOSED:
                        ord_autor_stop2 = True
                                    
                    if event_ord_autor2 == 'Ordem Alfabética':
                        cond_alf = not cond_alf
                        if pqautor2:
                            window3['-AUTOR2-'].update(sorted(pqautor2, reverse= cond_alf))
                        else:
                            window3['-AUTOR2-'].update(sorted(listaautores, reverse= cond_alf))
                        ord_autor_stop2 = True

                    if event_ord_autor2 == 'Frequência':
                        cond_frq = not cond_frq
                        if pqautor2:
                            window3["-AUTOR2-"].update([autor for autor,_ in sorted(sistema.ordenarMaisArtigos(database,pqautor2).items(), key = lambda x: x[1], reverse = cond_frq)])
                        else:
                            window3["-AUTOR2-"].update([autor for autor,_ in sorted(sistema.ordenarMaisArtigos(database,listaautores).items(), key = lambda x: x[1], reverse = cond_frq)])
                        ord_autor_stop2 = True
                ord_autor_window2.close()
        window3.close()

    if event== "Frequência de palavras-chave de um determinado ano":
        layout4 = [
            [sg.Text("Selecione um ano:", font=('Source Sans Pro', 13))],
            [sg.Listbox(values=anospal, size=(13, 7), key="-ANO-",font=('Georgia', 11))],
            [sg.Button("Confirmar",font=('Open Sans', 11)), sg.Button("Sair",font=('Open Sans', 11))],
        ]       
        window4 = sg.Window("Anos", layout4, font=("Helvetica", 16),resizable=True, modal = True)
                        
        stop4 = False
        while not stop4:
            event4, values4= window4.read()
            if event4 == sg.WINDOW_CLOSED or event4 == "Sair":
                stop4 = True
            if event4 == "Confirmar":
                if values4["-ANO-"]:
                    ano=values4["-ANO-"][0]
                    if current_canvas:
                        current_canvas.get_tk_widget().pack_forget()
                    fig = sistema.distribGrafico(sistema.PalavraporAno(database,20)[ano],f"Frequência de palavras chave de {ano}")
                    current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)
                else:
                    sg.Popup("Não selecionaste um ano")
                stop4 = True
        window4.close()
    if event== "Frequência de palavras-chave":
            if current_canvas:
                current_canvas.get_tk_widget().pack_forget()
            fig = sistema.distribGrafico(sistema.TopPalavrasChave(database,20), "Frequência de palavras chave")
            current_canvas = sistema.desenhar(window['-CANVAS-'].Widget, fig)

sistema.guardarBD("ata_medica_papers.json",database)

window.close()  