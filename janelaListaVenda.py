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

    soma = 0
    qtd_pecas = 0
    view = ce.read_file("venda.csv")
    if len(view) > 0:
        for item in view:
            qtd_pecas += int(item[2])
            soma += float(item[1]) * int(item[2])
            modo_list.append(item[3])       #Modalidade de Venda
            date_list.append(item[4])       #Data de Vendas
        for i in range(len(view)):
            view[i][1] = util.coin_format(str(view[i][1]))


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
        tooltip='This is a table')],
        [sg.Text('Filtrar Produto: ', size=(20, 0), font=("Arial", 14), pad=((80, 0), (10, 0)))],
        [sg.Text('Data de Venda:', pad=((80, 10), 10)),
         sg.Combo(list(set(date_list)), key='-COMBO-DATE-', pad=(10)),
         sg.Text('Modalidade de Pagamento:', pad=(10)),
         sg.Combo(sorted(list(set(modo_list))), key='-COMBO-MODO-', pad=(10)),
         sg.Button('Aplicar', button_color="Olive", size=(15, 1), pad=(10, 10)),
         sg.Button('Restaurar', size=(15, 1), pad=((20, 0), 20))],
        [sg.Text('Total Vendido: ', font=("Arial", 14), pad=((230, 5), (10, 0))), sg.Text(util.coin_format(str(soma)), key='soma', size=(15, 1), pad=(0, (10, 0)), font=("Arial", 14)),
         sg.Text('Total de Pecas: ', pad=((10, 5), (10, 0)), font=("Arial", 14)), sg.Text(qtd_pecas, key='qtd_pecas', size=(15, 1), pad=(0, (10, 0)), font=("Arial", 14))],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((300, 0), 20)),
         sg.Button('Nova Venda', button_color="Green", size=(15, 1), pad=((80, 0), 20))]
    ]

    janela = sg.Window("Janela Ver Valores", layout, size=(920, 600))

    while True:
        event, values = janela.read()

        if event == "-COMBO-DATE-":
            try:
                modo_list = []
                selected_date = values['-COMBO-DATE-']
                #Relacionando o COMBO BOX de Modalidade com Data
                for item in view:
                    if selected_date == item[4]:
                        print(item[3])
                        modo_list.append(item[3])
                janela.Element('-COMBO-MODO-').update(values=sorted(list(set(modo_list))))
            except:
                sg.popup_error("ERRO ao selecionar uma data!")


        if event == "Restaurar":
            try:
                modo_list = []
                date_list = []
                view = ce.read_file("venda.csv")
                soma = 0
                qtd_pecas = 0
                if len(view) > 0:
                    for item in view:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        modo_list.append(item[3])  # Modalidade de Venda
                        date_list.append(item[4])  # Data de Vendas
                    for i in range(len(view)):
                        view[i][1] = util.coin_format(str(view[i][1]))

                # ATUALIZANDO OS DADOS
                janela['-TABLE_PRODUCTS-'].update(view)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
                janela['-COMBO-MODO-'].update('')
                janela['-COMBO-DATE-'].update('')
            except:
                sg.popup_error("ERRO ao restaurar o filtro!")


        if event == "Aplicar":
            try:
                selected_modo = values['-COMBO-MODO-']
                selected_date = values['-COMBO-DATE-']
                search_list = []    #Lista de busca
                view = ce.read_file("venda.csv")
                soma = 0
                qtd_pecas = 0
                for item in view:
                    if len(selected_modo) == 0:
                        if selected_date == item[4]:  # Comparando a data
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                    elif len(selected_date) == 0:
                        if selected_modo == item[3]:  # Comparando modalidade
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                    else:
                        if selected_modo == item[3] and selected_date == item[4]:#Comparando modalidade e data
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                            item[1] = util.coin_format(str(item[1]))
                            search_list.append(item)
                #Atualizando os dados da tabela
                janela['-TABLE_PRODUCTS-'].update(search_list)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
            except:
                sg.popup_error("ERRO ao filtrar as vendas!")


        if event == "Nova Venda":
            try:
                janelaCarrinho()
                modo_list = []
                date_list = []
                view = ce.read_file("venda.csv")
                soma = 0
                qtd_pecas = 0
                if len(view) > 0:
                    for item in view:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        modo_list.append(item[3])  # Modalidade de Venda
                        date_list.append(item[4])  # Data de Vendas
                    for i in range(len(view)):
                        view[i][1] = util.coin_format(str(view[i][1]))

                #ATUALIZANDO OS DADOS
                janela['-TABLE_PRODUCTS-'].update(view)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
                janela['-COMBO-MODO-'].update(values=sorted(list(set(modo_list))))
                janela['-COMBO-DATE-'].update(values=list(set(date_list)))
                janela['-COMBO-MODO-'].update('')
                janela['-COMBO-DATE-'].update('')
            except:
                sg.popup_error("ERRO ao realizar uma nova venda!")


        if event == '-TABLE_PRODUCTS-':
            try:
                row_selected = values['-TABLE_PRODUCTS-'][0]
                product_name = str(view[row_selected][0])
                pop_message = f"Tem certeza que deseja excluir o registro de {product_name} da posicao {row_selected}?"
                if sg.popup_yes_no(pop_message) == 'Yes':
                    view = ce.remove_registro("venda.csv", int(row_selected))

                modo_list = []
                date_list = []
                view = ce.read_file("venda.csv")
                soma = 0
                qtd_pecas = 0
                if len(view) > 0:
                    for item in view:
                        qtd_pecas += int(item[2])
                        soma += float(item[1]) * int(item[2])
                        modo_list.append(item[3])  # Modalidade de Venda
                        date_list.append(item[4])  # Data de Vendas
                    for i in range(len(view)):
                        view[i][1] = util.coin_format(str(view[i][1]))

                # ATUALIZANDO OS DADOS
                janela['-TABLE_PRODUCTS-'].update(view)
                janela.Element('soma').update(util.coin_format(str(soma)))
                janela.Element('qtd_pecas').update(qtd_pecas)
                janela['-COMBO-MODO-'].update(values=sorted(list(set(modo_list))))
                janela['-COMBO-DATE-'].update(values=list(set(date_list)))
                janela['-COMBO-MODO-'].update('')
                janela['-COMBO-DATE-'].update('')
            except:
                sg.popup_error(f"Erro ao remover item {product_name}")
            janela['-TABLE_PRODUCTS-'].set_focus()


        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()