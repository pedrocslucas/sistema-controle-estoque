import PySimpleGUI as sg
import controle_estoque as ce
import util
from janelaCarrinho import janelaCarrinho

def janelaListaVenda():
    font = ("Halvetica", 10)
    sg.theme("LightBlue")
    sg.set_options(font=font)

    modo_list = []
    date_list = []
    name_list = []

    soma = 0
    qtd_pecas = 0
    view = ce.read_file("venda.csv")
    view_date_list = []

    if len(view) > 0:
        for item in view:
            qtd_pecas += int(item[2])
            soma += float(item[1]) * int(item[2])
            name_list.append(item[0])       #Nome do Produto
            modo_list.append(item[3])       #Modalidade de Venda
            date_list.append(item[4])       #Data de Vendas
        for i in range(len(view)):
            view[i][1] = util.coin_format(str(view[i][1]))
            view[i][4] = util.format_date(view[i][4])
        for data in sorted(list(set(date_list))):
            view_date_list.append(util.format_date(data))


    layout = [
        [sg.Text('Produtos Vendidos', font=("Arial", 24), pad=((320, 0), (50, 10)))],
        [sg.Table(values=view,
        headings=['Produto','Preco Vendido', 'Qtd Vendida','Modalidade', 'Data Registro'],
        pad=((80, 0), (20, 30)),
        max_col_width=50,
        auto_size_columns=True,
        justification='center',
        display_row_numbers=True,
        alternating_row_color="Light Gray",
        num_rows=10,
        key='-TABLE_PRODUCTS-',
        enable_events=True,
        tooltip='Tabela de Produtos Vendidos')],
        [sg.Text('Filtrar Produto: ', size=(20, 0), font=("Arial", 14), pad=((80, 0), (10, 0)))],
        [sg.Text('Data de Venda:', pad=((80, 10), (10, 0))),
         sg.Combo(view_date_list, key='-COMBO-DATE-INITIAL-', enable_events=True, pad=(10)),
         sg.Text('Modalidade de Pagamento:', pad=(10)),
         sg.Combo(sorted(list(set(modo_list))), key='-COMBO-MODO-', pad=(10)),
         sg.Button('Aplicar', button_color="Olive", size=(15, 1), pad=(10, 10)),
         sg.Button('Restaurar', size=(15, 1), pad=((20, 0), 20))],
        [sg.Text('at??:', pad=((150, 10), (0, 10))),
         sg.Combo(view_date_list, key='-COMBO-DATE-FINISH-', pad=(10)),
         sg.Text('Por Produto:', pad=(10)),
         sg.Combo(sorted(list(set(name_list))), key='-COMBO-NAME-', pad=(10))],
        [sg.Text('Total Vendido: ', font=("Arial", 14), pad=((230, 5), (10, 0))), sg.Text(util.coin_format(str(soma)), key='soma', size=(15, 1), pad=(0, (10, 0)), font=("Arial", 14)),
         sg.Text('Total de Pecas: ', pad=((10, 5), (10, 0)), font=("Arial", 14)), sg.Text(qtd_pecas, key='qtd_pecas', size=(15, 1), pad=(0, (10, 0)), font=("Arial", 14))],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((300, 0), 20)),
         sg.Button('Nova Venda', button_color="Green", size=(15, 1), pad=((80, 0), 20))]
    ]

    janela = sg.Window("Janela Ver Valores", layout, size=(920, 600))
    search_list = []

    while True:
        event, values = janela.read()

        if event == "-COMBO-DATE-INITIAL-":
            try:
                date_list_final = []
                date_list_finish = []
                selected_date = util.convert_to_date(values['-COMBO-DATE-INITIAL-'])
                #Relacionando o COMBO BOX de Modalidade com Data
                for item in view:
                    if util.convert_to_date(item[4]) > selected_date:
                        date_list_final.append(str(util.convert_to_date(item[4])))
                for data in sorted(list(set(date_list_final))):
                    date_list_finish.append(util.format_date(data))
                janela.Element('-COMBO-DATE-FINISH-').update(values=date_list_finish)
            except:
                sg.popup_error("ERRO ao selecionar uma data!")


        if event == "Restaurar":
            try:
                modo_list = []
                date_list = []
                name_list = []

                soma = 0
                qtd_pecas = 0
                view = ce.read_file("venda.csv")
                view_date_list = []

                if len(view) > 0:
                    for item in view:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        name_list.append(item[0])  # Nome do Produto
                        modo_list.append(item[3])  # Modalidade de Venda
                        date_list.append(item[4])  # Data de Vendas
                    for i in range(len(view)):
                        view[i][1] = util.coin_format(str(view[i][1]))
                        view[i][4] = util.format_date(view[i][4])
                    for data in sorted(list(set(date_list))):
                        view_date_list.append(util.format_date(data))

                # ATUALIZANDO OS DADOS
                janela['-TABLE_PRODUCTS-'].update(view)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
                janela['-COMBO-MODO-'].update('')
                janela['-COMBO-DATE-INITIAL-'].update('')
                janela['-COMBO-DATE-FINISH-'].update('')
                janela['-COMBO-NAME-'].update('')
                search_list = []
            except:
                sg.popup_error("ERRO ao restaurar o filtro!")


        if event == "Aplicar":
            selected_modo = values['-COMBO-MODO-']
            selected_date = values['-COMBO-DATE-INITIAL-']
            selected_date_final = values['-COMBO-DATE-FINISH-']
            selected_name = values['-COMBO-NAME-']

            search_list = []                                    #Lista de busca
            view = ce.read_file("venda.csv")
            soma = 0
            qtd_pecas = 0

            if len(selected_date) == 0 and len(selected_modo) == 0 and len(selected_name) == 0:
                sg.popup_error("Selecione um filtro v??lido!")

            elif len(selected_name) != 0 and len(selected_date) == 0 and len(selected_modo) == 0:   #NOME selecionado
                for item in view:
                    item[4] = util.format_date(item[4])
                    if item[0] == selected_name:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        item[1] = util.coin_format(str(item[1]))
                        search_list.append(item)

            elif len(selected_name) != 0 and len(selected_date) != 0 and len(selected_modo) == 0:   #Nome e data selecionados
                for item in view:
                    item[4] = util.format_date(item[4])
                    if len(selected_date_final) != 0:
                        # Comparando a data
                        if util.convert_to_date(item[4]) >= util.convert_to_date(selected_date) and util.convert_to_date(
                                item[4]) <= util.convert_to_date(selected_date_final) and item[0] == selected_name:
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                    else:
                        if item[4] == selected_date and item[0] == selected_name:  # Comparando a data
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)

            elif len(selected_name) != 0 and len(selected_date) == 0 and len(selected_modo) != 0:
                for item in view:
                    item[4] = util.format_date(item[4])
                    if selected_modo == item[3] and item[0] == selected_name:  # Comparando modalidade e nome
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        item[1] = util.coin_format(str(item[1]))
                        search_list.append(item)

            elif len(selected_name) != 0 and len(selected_date) != 0 and len(selected_modo) != 0:   #Todos est??o selecionados
                for item in view:
                    item[4] = util.format_date(item[4])
                    if len(selected_date_final) != 0:
                        # Comparando modalidade e data
                        if util.convert_to_date(item[4]) >= util.convert_to_date(selected_date) and util.convert_to_date(
                                item[4]) <= util.convert_to_date(selected_date_final) and selected_modo == item[3] and \
                                item[0] == selected_name:
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                    else:
                        if selected_modo == item[3] and item[4] == selected_date and item[0] == selected_name:  # Comparando modalidade e data
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)

            elif len(selected_date) != 0 and len(selected_modo) == 0 and len(selected_name) == 0:   #Data selecionada e modalidade n??o
                for item in view:
                    item[4] = util.format_date(item[4])
                    if len(selected_date_final) != 0:
                        # Comparando a data
                        if util.convert_to_date(item[4]) >= util.convert_to_date(selected_date) and util.convert_to_date(
                                item[4]) <= util.convert_to_date(selected_date_final):
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                    else:
                        if item[4] == selected_date:  # Comparando a data
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
            elif len(selected_date) == 0 and len(selected_modo) != 0 and len(selected_name) == 0:   #Modalidade selecionada e data n??o
                for item in view:
                    item[4] = util.format_date(item[4])
                    if selected_modo == item[3]:  # Comparando modalidade
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        item[1] = util.coin_format(str(item[1]))
                        search_list.append(item)
            elif len(selected_date) != 0 and len(selected_modo) != 0 and len(selected_name) == 0:                                                       #Data e modalidade selecionados
                for item in view:
                    item[4] = util.format_date(item[4])
                    if len(selected_date_final) != 0:
                        # Comparando modalidade e data
                        if util.convert_to_date(item[4]) >= util.convert_to_date(selected_date) and util.convert_to_date(
                                item[4]) <= util.convert_to_date(selected_date_final) and selected_modo == item[3]:
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                    else:
                        if selected_modo == item[3] and item[4] == selected_date:  # Comparando modalidade e data
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)

            #Atualizando os dados da tabela
            janela['-TABLE_PRODUCTS-'].update(search_list)
            janela.Element('soma').update(util.coin_format(str(soma)))
            janela.Element('qtd_pecas').update(qtd_pecas)


        if event == "Nova Venda":
            try:
                janelaCarrinho()

                modo_list = []
                date_list = []
                soma = 0
                qtd_pecas = 0
                view = ce.read_file("venda.csv")
                view_date_list = []
                if len(view) > 0:
                    for item in view:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        modo_list.append(item[3])  # Modalidade de Venda
                        date_list.append(item[4])  # Data de Vendas
                    for i in range(len(view)):
                        view[i][1] = util.coin_format(str(view[i][1]))
                        view[i][4] = util.format_date(view[i][4])
                    for data in sorted(list(set(date_list))):
                        view_date_list.append(util.format_date(data))

                #ATUALIZANDO OS DADOS
                janela['-TABLE_PRODUCTS-'].update(view)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
                janela['-COMBO-MODO-'].update(values=sorted(list(set(modo_list))))
                janela['-COMBO-DATE-INITIAL-'].update(values=view_date_list)
                janela['-COMBO-DATE-FINISH-'].update(values=view_date_list)
                janela['-COMBO-MODO-'].update('')
                janela['-COMBO-DATE-INITIAL-'].update('')
                janela['-COMBO-DATE-FINISH-'].update('')
                search_list = []
            except:
                sg.popup_error("ERRO ao realizar uma nova venda!")


        if event == '-TABLE_PRODUCTS-':
            try:
                row_selected = values['-TABLE_PRODUCTS-'][0]
                item = []
                if len(search_list) == 0:
                    for i, dado in enumerate(view):
                        print(dado)
                        if i == row_selected:
                            item = dado
                            break
                else:
                    for i, dado in enumerate(search_list):
                        if i == row_selected:
                            item = dado
                            break

                print(f'Item: {item}')

                product_name = str(item[0])

                pop_message = f"Tem certeza que deseja excluir o registro de {product_name} da posicao {row_selected}?"
                if sg.popup_yes_no(pop_message) == 'Yes':
                    view = ce.remove_item("venda.csv", item)

                modo_list = []
                date_list = []
                soma = 0
                qtd_pecas = 0
                view = ce.read_file("venda.csv")
                view_date_list = []
                if len(view) > 0:
                    for item in view:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        modo_list.append(item[3])  # Modalidade de Venda
                        date_list.append(item[4])  # Data de Vendas
                    for i in range(len(view)):
                        view[i][1] = util.coin_format(str(view[i][1]))
                        view[i][4] = util.format_date(view[i][4])
                    for data in sorted(list(set(date_list))):
                        view_date_list.append(util.format_date(data))

                # ATUALIZANDO OS DADOS
                janela['-TABLE_PRODUCTS-'].update(view)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
                janela['-COMBO-MODO-'].update(values=sorted(list(set(modo_list))))
                janela['-COMBO-DATE-INITIAL-'].update(values=view_date_list)
                janela['-COMBO-DATE-FINISH-'].update(values=view_date_list)
                janela['-COMBO-MODO-'].update('')
                janela['-COMBO-DATE-INITIAL-'].update('')
                janela['-COMBO-DATE-FINISH-'].update('')
            except:
                sg.popup_error(f"Erro ao remover item {product_name}")
            janela['-TABLE_PRODUCTS-'].set_focus()


        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()