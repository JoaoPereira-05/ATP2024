import PySimpleGUI as sg
import sistema

def ajuda():
    return ("""
    Publicação:
        Criar uma Publicação:
        - Para criar uma nova publicação, insira todos os detalhes relevantes, como título, autor, palavras-chave e data de publicação. 
        - O sistema irá adicionar a publicação à base de dados, garantindo que todos os campos sejam preenchidos corretamente.

        Consultar uma Publicação através de ID:
        - Utilize o ID único de uma publicação existente para recuperar detalhes completos sobre ela, incluindo título, autor, afiliação, palavras-chave, e data de publicação.

        Consultar Publicações:
        - Esta opção permite realizar pesquisas sobre as publicações existentes. É possível filtrar por título, autor, afiliação, palavras-chave ou data de publicação. 
        - Você também pode ordenar os resultados de diferentes formas, como por data ou título.

        Eliminar uma Publicação através de ID:
        - Caso queira remover uma publicação da base de dados, basta fornecer o ID correspondente. 
        - Tenha cuidado ao eliminar publicações, pois é uma ação é irreversível.

    Análise:
        Frequência de Keywords:
        - Esta funcionalidade permite analisar a frequência das palavras-chave usadas nas publicações da base de dados. 
        - Ideal para encontrar as palavras mais recorrentes e entender tendências no conteúdo das publicações.

        Palavras do Ano:
        - O sistema irá identificar as palavras que mais apareceram ao longo do ano, oferecendo uma visão das tendências e áreas mais discutidas.

        Publicações por Autor:
        - Exibe o número total de publicações feitas por cada autor. 
        - Você pode ordenar a lista para ver quais autores mais contribuíram para o banco de dados.

        Quantidade de Publicações de Autor por Ano:
        - Aqui, você pode ver o número de publicações feitas por cada autor ao longo dos anos. 
        - Essa análise ajuda a entender a evolução da produção científica de cada autor.

        Publicações por Ano:
        - Mostra o número total de publicações feitas em cada ano. 
        - Pode ser útil para observar tendências anuais e entender o ritmo de publicações ao longo do tempo.

        Publicações por Mês:
        - Similar à análise de publicações por ano, mas focada no mês. 
        - Ajuda a identificar padrões mensais de publicação, como picos de atividade em determinados meses.

    Listar Todos os Autores e Todas as Publicações por Autor:
    - Exibe uma lista detalhada de todos os autores registrados no sistema e as publicações associadas a cada um deles. 
    - Esta função é útil para obter uma visão geral da produção científica de todos os autores presentes no banco de dados.

    Importar Publicações:
    - Permite carregar publicações de uma base de dados externa ou arquivo CSV. 
    - Basta selecionar o arquivo e o sistema irá importar automaticamente as publicações para o banco de dados.
    - Tenha a certeza de que o arquivo está no formato adequado para evitar erros na importação.

-------------------------------
Para mais informações, consulte a documentação do sistema ou entre em contato com o suporte técnico. projetomagik@suporte.com
    """)

def publicacoes(window_admin, bd):
    layout = [
        [sg.Button("Criar", key="-CRIAR-", size=(20, 1)),
         sg.Button("Consultar ID", key="-CONS_ID-", size=(20, 1))],
        [sg.Button("Consultar Filtro", key="-CONS_FILTRO-", size=(20, 1))]
    ]

    janela_publicacoes = sg.Window("Gestão de Publicações", layout, modal=True)

    stop2 = False
    klik = None

    while not stop2:
        event, values = janela_publicacoes.read()
        if event == sg.WINDOW_CLOSED:
            stop2 = True
            return window_admin
        elif event in ["-CRIAR-", "-CONS_ID-", "-CONS_FILTRO-"]:
            klik = event
            stop2 = True

    janela_publicacoes.close()

    if klik == "-CONS_FILTRO-":
        consultar_filtro(bd)

    return klik


def consultar_filtro(bd):
    layout_filtro = [
        [sg.Text("Filtro:"),
         sg.Combo(["Titulo", "Autor", "Afiliação", "Keyword", "Data Pub"], key="-FILTRO-", size=(20, 1), enable_events=True)],
        [sg.Multiline(size=(80, 20), key="-RESULTADO-", disabled=True)],
        [sg.Button("Fechar")]
    ]

    janela_filtro = sg.Window("Consultar Filtro", layout_filtro, modal=True)

    stop = False

    while not stop:
        event, values = janela_filtro.read()

        if event == sg.WINDOW_CLOSED or event == "Fechar":
            stop = True

        elif event == "-FILTRO-":
            filtro = values["-FILTRO-"]
            resultado = []

            if filtro == "Titulo":
                titulo = sg.popup_get_text("Digite o título:")
                if titulo:
                    resultado = sistema.consultarPubTitulo(bd, titulo)
            elif filtro == "Autor":
                autor = sg.popup_get_text("Digite o nome do autor:")
                if autor:
                    resultado = sistema.consultarpAutor(bd, autor)
            elif filtro == "Afiliação":
                afiliacao = sg.popup_get_text("Digite a afiliação:")
                if afiliacao:
                    resultado = sistema.consultarPubAfiliacao(bd, afiliacao)
            elif filtro == "Keyword":
                keyword = sg.popup_get_text("Digite a palavra-chave:")
                if keyword:
                    resultado = sistema.consultarpKeyword(bd, [keyword])
            elif filtro == "Data Pub":
                data = sg.popup_get_text("Digite a data (YYYY-MM-DD):")
                if data:
                    resultado = sistema.consultarpData(bd, data)

            if resultado:
                janela_filtro["-RESULTADO-"].update(
                    "\n\n".join([formatar_conteudo(r) for r in resultado])
                )
            else:
                janela_filtro["-RESULTADO-"].update("Nenhum resultado encontrado.")

    janela_filtro.close()


def formatar_conteudo(conteudo):
    """Formata o conteúdo para exibição legível."""
    return (
        f"**Título:** {conteudo.get('title', 'N/A')}\n"
        f"**Resumo:** {conteudo.get('abstract', 'N/A')}\n"
        f"**Palavras-chave:** {conteudo.get('keywords', 'N/A')}\n"
        f"**Data de Publicação:** {conteudo.get('publish_date', 'N/A')}\n"
        f"**Autores:**\n" +
        "\n".join(
            f"  - {autor['name']} ({autor.get('affiliation', 'Sem afiliação')})"
            for autor in conteudo.get("authors", [])
        ) + "\n"
    )

def criarPub_InterfaceGraf(window_admin, bd):
    
    layout = [
        [sg.Text("Título(*):", font=('Helvetica', 11)), sg.InputText(key="-TITULO-",size=(76 ,1),font=('Georgia', 11))],
        [sg.Text("Resumo(*):", font=('Helvetica', 11))], 
        [sg.Multiline(font=('Georgia', 11), key="-RESUMO-", size=(None, 5))],
        [sg.Text("Palavras-chave:", font=('Helvetica', 11))], 
        [sg.InputText(key="-PCHAVE-", font=('Georgia', 11), size=(52, 2)), sg.Button("Adicionar palavra", font=('Open Sans', 11))],
        [sg.Multiline("", font=('Georgia', 11), key="-PsCHAVE-", size=(65, 2), disabled=True), sg.Button("Remover palavra", font=('Open Sans', 11))],
        [sg.Text("Data de publicação:", font=('Helvetica', 11))],
        [sg.Button("Escolher data", font=('Open Sans', 11)), sg.Input("", key="-DATASELECTED-", readonly=True, font=('Georgia', 11), size=(10, 1)), sg.Button("Remover data", font=('Open Sans', 11))],
        [sg.Text("Autor(*):", font=('Helvetica', 11))],
        [sg.Combo(values=[], font=('Helvetica', 11), key="-AUTORES-", readonly=True, size=(41, 1))],
        [sg.Button("Adicionar autor", font=('Open Sans', 11)), sg.Button("Modificar autor", font=('Open Sans', 11)), sg.Button("Remover autor", font=('Open Sans', 11))],
        [sg.Text("doi(*):", font=('Helvetica', 11)), sg.InputText(key="-DOI-", font=('Georgia', 11), size=(77, 1))],
        [sg.Text("pdf:", font=('Helvetica', 11)), sg.InputText(key="-PDF-", font=('Georgia', 11), size=(77, 1))],
        [sg.Text("url(*):", font=('Helvetica', 11)), sg.InputText(key="-URL-", font=('Georgia', 11), size=(77, 1))],
        [sg.Button("Criar", font=('Open Sans', 11)), sg.Button("Cancelar", font=('Open Sans', 11)), sg.Push(), sg.Text("* Campo obrigatório", font=('Helvetica', 11))]
    ]
    
    window_criar_pub = sg.Window("Criar Publicação", layout, font="Helvetica", modal=True)
    
    new_keywords = ""
    data = ""
    autores = []
    user = {
        "abstract": "",
        "keywords": "",
        "authors": [],
        "doi": "",
        "url": "",
        "pdf": "",
        "publish_date": "",
        "title": ""
    }

    while True:
        event, values = window_criar_pub.read()

        if event in (sg.WINDOW_CLOSED, "-CANCELAR-PUB-"):
            window_criar_pub.close()
            return window_admin  

        user["abstract"] = values["-RESUMO-"]

        if event == "Adicionar palavra" and values["-PCHAVE-"] != "":
            new_keywords = sistema.criarKeywords(new_keywords, values["-PCHAVE-"])
            window_criar_pub["-PCHAVE-"].update("")
            window_criar_pub["-PsCHAVE-"].update(new_keywords)
            user["keywords"] = new_keywords

        if event == "Remover palavra":
            layout_pal = [
                [sg.Listbox(values=user["keywords"].split(", "), key="-PALREMOVE-", font=('Georgia', 11), size=(35, 10), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
                [sg.Button("Confirmar", font=('Open Sans', 11)), sg.Button("Sair", font=('Open Sans', 11))]
            ]
            window_rempal = sg.Window("Palavras-chave", layout_pal, font=("Helvetica", 16), modal=True)
            stop_rempal = False
            while not stop_rempal:
                event_rempal, values_rempal = window_rempal.read()
                if event_rempal in (sg.WINDOW_CLOSED, "Sair"):
                    stop_rempal = True
                    window_rempal.close()
                elif event_rempal == "Confirmar":
                    current_pals = user["keywords"].split(", ")
                    novaspals = [pal for pal in current_pals if pal not in values_rempal["-PALREMOVE-"]]
                    keywords = ",".join(novaspals)
                    user["keywords"] = keywords
                    window_criar_pub["-PsCHAVE-"].update(user["keywords"])
                    window_rempal["-PALREMOVE-"].update(keywords.split(", "))

        if event == "Adicionar autor":
            layout_naut = [
                [sg.Text("Nome:", font=('Helvetica', 11)), sg.Input("", font=('Georgia', 11), key="-NOVONOME-")],
                [sg.Text("Afiliação:", font=('Helvetica', 11)), sg.Multiline("", key="-NOVAAFIL-", font=('Georgia', 11), size=(36, 4))],
                [sg.Text("Orcid:", font=('Helvetica', 11)), sg.Input("", font=('Georgia', 11), key="-NOVOORCID-")],
                [sg.Button("Confirmar", font=('Open Sans', 11)), sg.Button("Sair", font=('Open Sans', 11))]
            ]
            window_naut = sg.Window("Adicionar Autor", layout_naut, font=("Helvetica", 16), modal=True)

            stop_naut = False
            while not stop_naut:
                event_naut, values_naut = window_naut.read()
                if event_naut in (sg.WINDOW_CLOSED, "Sair"):
                    stop_naut = True
                elif event_naut == "Confirmar" and values_naut["-NOVONOME-"] != "":
                    autores.append(sistema.criarAutores(values_naut["-NOVONOME-"], values_naut["-NOVAAFIL-"], values_naut["-NOVOORCID-"]))
                    user["authors"] = autores
                    window_criar_pub["-AUTORES-"].update(values=[autor["name"] for autor in user["authors"]])
                    stop_naut = True
            window_naut.close()

        if event == "Modificar autor" and not values["-AUTORES-"]:
            sg.Popup("Não selecionaste um autor")
        elif event == "Modificar autor":
            for autor in user["authors"]:
                if autor["name"] == values["-AUTORES-"]:
                    autmod = autor
                    layout_mod = [
                        [sg.Text("Nome:", font=('Helvetica', 11)), sg.Input(autmod["name"], font=('Georgia', 11), key="-NOMEMOD-", disabled=True)],
                        [sg.Text("Afiliação:", font=('Helvetica', 11)), sg.Multiline(autmod.get("affiliation"), font=('Georgia', 11), key="-AFILMOD-", size=(36, 4))],
                        [sg.Text("Orcid:", font=('Helvetica', 11)), sg.Input(autmod.get("orcid"), font=('Georgia', 11), key="-ORCIDMOD-")],
                        [sg.Button("Confirmar", font=('Open Sans', 11)), sg.Button("Sair", font=('Open Sans', 11))]
                    ]
                    window_mod = sg.Window("Modificar autor", layout_mod, font=("Helvetica", 16), modal=True)
                    stop_mod = False
                    while not stop_mod:
                        event_mod, values_mod = window_mod.read()
                        if event_mod in (sg.WINDOW_CLOSED, "Sair"):
                            stop_mod = True
                        elif event_mod == "Confirmar":
                            if values_mod["-NOMEMOD-"] == "":
                                sg.Popup("Campo nome obrigatório")
                            else:
                                autmod["name"] = values_mod["-NOMEMOD-"]
                            if values_mod["-AFILMOD-"] != "":
                                autmod["affiliation"] = values_mod["-AFILMOD-"]
                            if values_mod["-ORCIDMOD-"] != "":
                                autmod["orcid"] = values_mod["-ORCIDMOD-"]
                            for autor in user["authors"]:
                                if autor["name"] == values_mod["-NOMEMOD-"]:
                                    for key, value in autmod.items():
                                        autor[key] = value
                            stop_mod = True
                    window_mod.close()

        if event == "Remover autor" and not values["-AUTORES-"]:
            sg.Popup("Não selecionaste um autor")
        elif event == "Remover autor":
            for autor in user["authors"]:
                if autor["name"] == values["-AUTORES-"]:
                    user["authors"].remove(autor)
            window_criar_pub["-AUTORES-"].update(values=[autor["name"] for autor in user["authors"]])

        user["doi"] = values["-DOI-"]
        user["pdf"] = values["-PDF-"]
        user["title"] = values["-TITULO-"]
        user["url"] = values["-URL-"]

        if event == "Escolher data":
            layout_data = [
                [sg.Text("Selecione uma Data:", font=('Helvetica', 11))],
                [sg.CalendarButton("Escolher Data", target="-DATA-", format="%Y-%m-%d", font=('Open Sans', 11), key="CALENDARIO")],
                [sg.InputText("", key="-DATA-", size=(20, 1), font=('Geogia', 11), readonly=True)],
                [sg.Button("Confirmar", font=('Open Sans', 11)), sg.Button("Cancelar", font=('Open Sans', 11))]
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
                    window_criar_pub["-DATASELECTED-"].update(values_data["-DATA-"])
            window_data.close()

        if event == "Remover data":
            user["publish_date"] = ""
            window_criar_pub["-DATASELECTED-"].update("")

        if event == "Criar":
            if user["title"] == "" or user["authors"] == [] or user["doi"] == "" or user["abstract"] == "" or user["url"] == "":
                sg.Popup("Preencha todos os campos obrigatórios!")
            else:
                bd = sistema.criarPub(bd, user["abstract"], user["keywords"], user["authors"], user["doi"], user["pdf"], user["publish_date"], user["title"], user["url"])
                sg.Popup("Publicação criada com sucesso!")
                window_criar_pub.close()
                return window_admin

def consulta_por_id_interface(window_admin, database):
    layout = [
        [sg.Text("Digite o ID da publicação:")],
        [sg.InputText(key="id_input")],
        [sg.Button("Consultar", key="-PROC-"), sg.Button("Eliminar", key="-DEL-"), sg.Button("Cancelar", key="-CANCELAR-")],
        [sg.Multiline("", key="-RESULTADO-", size=(800, 100), autoscroll=True, no_scrollbar=False, justification='left')],
    ]
    
    window_consulta = sg.Window("Consulta de Publicação por ID", layout, size=(1000, 350), modal=True)
    
    stop = False

    while not stop:

        event, values = window_consulta.read()
        
        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            window_consulta.close()
            return window_admin
        
        if event == "-PROC-":
            id_pub = values["id_input"]
            if not id_pub:
                window_consulta["-RESULTADO-"].update("Erro: O ID fornecido é inválido. Por favor, insira um ID válido.")
            else:
                resultado = sistema.consultapID(database, id_pub)
                if resultado:    
                    window_consulta["-RESULTADO-"].update(resultado)
                else:
                    window_consulta["-RESULTADO-"].update("Erro: O ID fornecido é inválido. Por favor, insira um ID válido.")
        
        if event == "-DEL-":
            id_pub = values["id_input"]
            if not id_pub:
                window_consulta["-RESULTADO-"].update("Erro: O ID fornecido é inválido. Por favor, insira um ID válido para excluir.")
            else:
                resultado = sistema.consultapID(database, id_pub)
                if resultado:
                    confirmar_exclusao = sg.Window(
                        "Confirmar Exclusão",
                        [
                            [sg.Text(f"Tem certeza que deseja eliminar a publicação com ID {id_pub}?")],
                            [sg.Button("Sim", key="-CONFIRMAR-"), sg.Button("Não", key="-CANCELAR-")],
                        ],
                        modal=True,
                    )
                    
                    confirm_event, _ = confirmar_exclusao.read()
                    confirmar_exclusao.close()
                    
                    if confirm_event == "-CONFIRMAR-":
                        try:
                            sistema.elimPub(database, id_pub)
                            window_consulta["-RESULTADO-"].update(f"Publicação com ID {id_pub} eliminada com sucesso.")
                        except Exception as e:
                            window_consulta["-RESULTADO-"].update(f"Erro ao eliminar a publicação: {str(e)}")
                else:
                    window_consulta["-RESULTADO-"].update("Erro: Publicação não encontrada. Não é possível eliminar.")
    
    window_consulta.close()
    return window_admin

def analise_interface(window_admin, database):
    layout = [
        [sg.Button("Top Palavras-Chave", key="-KEYWORDS-"),
         sg.Button("Palavras por Ano", key="-PALAVRAS-ANO-"),
         sg.Button("Publicações por Ano", key="-PUBS-ANO-")],
        [sg.Button("Publicações por Autor", key="-PUBS-AUTOR-"),
         sg.Button("Publicações de Autor por Ano", key="-PUBS-AUTOR-ANO-"),
         sg.Button("Publicações por Mês", key="-PUBS-MES-")],
        [sg.Multiline("", key="-RESULTADO-", size=(80, 20), disabled=True)]
    ]

    window_analise = sg.Window("Análise de Publicações", layout, modal=True)

    stop3 = False

    while not stop3:

        event, values = window_analise.read()

        if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
            stop3 = True

        if event == "-KEYWORDS-":
            n = sg.popup_get_text("Digite o número de palavras-chave mais frequentes:", title="Top Palavras-Chave")
            if n and n.isdigit():
                resultado = sistema.TopPalavrasChave(database, int(n))
                window_analise["-RESULTADO-"].update(resultado)
            else:
                sg.popup_error("Valor inválido. Por favor, insira um número.")

        elif event == "-PALAVRAS-ANO-":
            n = sg.popup_get_text("Digite o número de palavras-chave por ano:", title="Palavras por Ano")
            if n and n.isdigit():
                resultado = sistema.PalavraporAno(database, int(n))
                window_analise["-RESULTADO-"].update(resultado)
            else:
                sg.popup_error("Valor inválido. Por favor, insira um número.")

        elif event == "-PUBS-ANO-":
            resultado = sistema.statsPubAno(database)
            window_analise["-RESULTADO-"].update(resultado)

        elif event == "-PUBS-AUTOR-":
            n = sg.popup_get_text("Digite o número de autores mais frequentes:", title="Publicações por Autor")
            if n and n.isdigit():
                resultado = sistema.PubporAutor(database, int(n))
                window_analise["-RESULTADO-"].update(resultado)
            else:
                sg.popup_error("Valor inválido. Por favor, insira um número.")

        elif event == "-PUBS-AUTOR-ANO-":
    
            autores_completos = [autor["name"] for pub in database for autor in pub.get("authors", [])]
            autores_unicos = list(set(autores_completos))

            layout_autor = [
                [sg.Text("Digite o nome do autor:")],
                [sg.Input("", key="-INPUT_AUTOR-", enable_events=True, size=(30, 1))],
                [sg.Listbox(values=autores_unicos, size=(40, 15), key="-LISTA_AUTORES-", enable_events=True)],
                [sg.Button("Selecionar", key="-SELECIONAR-"), sg.Button("Cancelar", key="Cancelar")]
            ]

            window_autor = sg.Window("Selecionar Autor", layout_autor, modal=True, finalize=True)

            autor_selecionado = None

            stop = False

            while not stop:
                event_autor, values_autor = window_autor.read()
                if event_autor in (sg.WINDOW_CLOSED, "Cancelar"):
                    stop = True
                elif event_autor == "-INPUT_AUTOR-":
                    termo_busca = values_autor["-INPUT_AUTOR-"].strip().lower()
                    autores_filtrados = [
                        autor for autor in autores_unicos if termo_busca in autor.lower()
                    ]
                    window_autor["-LISTA_AUTORES-"].update(autores_filtrados)
                elif event_autor == "-LISTA_AUTORES-":
                    autor_selecionado = values_autor["-LISTA_AUTORES-"][0] if values_autor["-LISTA_AUTORES-"] else None
                elif event_autor == "-SELECIONAR-":
                    if autor_selecionado:
                        stop = True
                    else:
                        sg.popup_error("Nenhum autor selecionado. Por favor, escolha um autor.")

            window_autor.close()

    
            if autor_selecionado:
                resultado = sistema.AutorporAno(database, autor_selecionado)
                window_analise["-RESULTADO-"].update(resultado)
            else:
                sg.popup_error("Nenhum autor foi selecionado.")


        elif event == "-PUBS-MES-":
            ano = sg.popup_get_text("Digite o ano para as publicações por mês:", title="Publicações por Mês")
            if ano and ano.isdigit():
                resultado = sistema.statsPubMes(database, int(ano))
                window_analise["-RESULTADO-"].update(resultado)
            else:
                sg.popup_error("Ano inválido. Por favor, insira um ano válido.")

    window_analise.close()
    return window_admin

def lista_autores_interface(window_admin, database):
    stop = False

    layout = [
        [sg.Text('Lista de Autores')],
        [sg.Input('', size=(30, 1), key='-INPUT_AUTOR-', enable_events=True)],
        [sg.Listbox(values=[], size=(50, 15), key='-LISTA_AUTORES-', enable_events=True)],
        [sg.Text('Conteúdo do Autor:')],
        [sg.Multiline('', size=(70, 15), key='-CONTEUDO-', disabled=True)], 
        [sg.Button('Sair')]
    ]

    window_listar_autor = sg.Window('Navegação de Autores', layout, finalize=True, modal=True)

    try:
        autores_completos = sistema.listarautor(database)
    except Exception as e:
        sg.popup_error(f"Erro ao carregar autores: {e}")
        return window_admin

    nomes_autores = [autor for autor in autores_completos]
    window_listar_autor['-LISTA_AUTORES-'].update(nomes_autores)

    while not stop:
        event, values = window_listar_autor.read(timeout=100)

        if event in (sg.WINDOW_CLOSED, 'Sair'):
            stop = True

        elif event == '-INPUT_AUTOR-':
            termo_busca = values['-INPUT_AUTOR-'].strip().lower()
            if termo_busca:
                nomes_filtrados = [nome for nome in nomes_autores if termo_busca in nome.lower()]
            else:
                nomes_filtrados = nomes_autores
            window_listar_autor['-LISTA_AUTORES-'].update(nomes_filtrados)

        elif event == '-LISTA_AUTORES-':
            autor_selecionado = values['-LISTA_AUTORES-']
            if autor_selecionado:
                try:
                    conteudo_dict = sistema.consultarpAutor(database, autor_selecionado[0])
                    conteudo_dict = conteudo_dict[0] if conteudo_dict else {}
                    conteudo = formatar_conteudo(conteudo_dict)
                except Exception as e:
                    conteudo = f"Erro ao carregar conteúdo: {e}"

                window_listar_autor['-CONTEUDO-'].update(conteudo)

    window_listar_autor.close()
    return window_admin

def formatar_conteudo(conteudo):
    """Formata o conteúdo do autor para exibição mais legível."""
    try:
        texto_formatado = (
            f"**Título:** {conteudo.get('title', 'N/A')}\n\n"
            f"**Resumo:**\n{conteudo.get('abstract', 'N/A')}\n\n"
            f"**Palavras-Chave:** {conteudo.get('keywords', 'N/A')}\n\n"
            f"**Autores:**\n" +
            "\n".join(
                f"  - {autor['name']} ({autor.get('affiliation', 'Afiliado não especificado')})"
                for autor in conteudo.get('authors', [])
            ) + "\n\n"
            f"**DOI:** {conteudo.get('doi', 'N/A')}\n"
            f"**Link para o PDF:** {conteudo.get('pdf', 'N/A')}\n"
            f"**Data de Publicação:** {conteudo.get('publish_date', 'N/A')}\n"
            f"**URL:** {conteudo.get('url', 'N/A')}\n"
            "--------------------------------------------------------------------------------------------------------------------------------------------"
        )
    except Exception as e:
        texto_formatado = f"Erro ao formatar conteúdo: {e}"
    return texto_formatado

def interface_importar(window_admin,bd):
    layout = [
        [sg.Text("Selecione um ficheiro JSON para importar:")],
        [sg.Input(key="-FICHEIRO-", enable_events=True), sg.FileBrowse("Procurar", file_types=(("JSON Files", "*.json"),))],
        [sg.Button("Importar", key="-IMPORTAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        [sg.Multiline("", size=(80, 20), key="-RESULTADO-", autoscroll=True, disabled=True)]
    ]

    window_importar = sg.Window("Importar Publicações", layout, modal=True)

    stop4 = False

    while not stop4:
        event, values = window_importar.read()

        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop4 = True

        if event == "-IMPORTAR-":
            ficheiro = values["-FICHEIRO-"]
            if not ficheiro:
                window_importar["-RESULTADO-"].update("Erro: Nenhum ficheiro selecionado.")
            else:
                try:
                    resultado = sistema.importar(bd,ficheiro)
                    if resultado == "Ficheiro não suportado": 
                        window_importar["-RESULTADO-"].update("Erro: Ficheiro não suportado")
                    else:
                        window_importar["-RESULTADO-"].update(f"Ficheiro importado com sucesso.\nNúmero de registros: {len(resultado)}")
                except Exception as e:
                    window_importar["-RESULTADO-"].update(f"Erro ao importar o ficheiro: {str(e)}")
                except Exception as e:
                    window_importar["-RESULTADO-"].update(f"Erro ao importar o ficheiro: {str(e)}")

    window_importar.close()
    return window_admin

def interface_guardar(window_admin, database):
    layout = [
        [sg.Text("Guardar base de dados em ficheiro JSON:")],
        [sg.InputText(key="-FICHEIRO-", enable_events=True), sg.FileSaveAs("Procurar", file_types=(("JSON Files", "*.json"),))],
        [sg.Button("Guardar", key="-GUARDAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        [sg.Multiline("", size=(60, 3), key="-RESULTADO-", autoscroll=True, disabled=True)]
    ]

    window_guardar = sg.Window("Guardar Base de Dados", layout, modal=True)

    stop5 = False

    while not stop5:
        event, values = window_guardar.read()

        if event == sg.WINDOW_CLOSED or event == "-CANCELAR-":
            stop5 = True

        if event == "-GUARDAR-":
            ficheiro = values["-FICHEIRO-"]
            if not ficheiro:
                window_guardar["-RESULTADO-"].update("Erro: Nenhum ficheiro selecionado.")
            else:
                try:
                    sistema.guardarBD(ficheiro, database)
                    window_guardar["-RESULTADO-"].update(f"Base de dados guardada com sucesso em: {ficheiro}")
                except Exception as e:
                    window_guardar["-RESULTADO-"].update(f"Erro ao guardar o ficheiro: {str(e)}")

    window_guardar.close()
    return window_admin