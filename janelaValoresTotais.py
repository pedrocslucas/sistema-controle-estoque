import PySimpleGUI as sg
import controle_estoque as ce
import util
from janelaProdutos import janelaProdutos
from janelaCarrinho import janelaCarrinho

def janelaVerTotal():
    font = ("Halvetica", 10)
    sg.theme("LightBlue")
    sg.set_options(font=font)

    soma = 0
    qtd_pecas = 0
    view = ce.read_file("venda.csv")
    if len(view) > 0:
        for item in view:
            qtd_pecas += int(item[2])
            soma += float(item[1]) * int(item[2])
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
        [sg.Text('Total Vendido: ', font=("Arial", 14), pad=((230, 5), (10, 0))), sg.Text(util.coin_format(str(soma)), key='soma', size=(15, 1), pad=(0, (10, 0)), font=("Arial", 14)),
         sg.Text('Total de Pecas: ', pad=((10, 5), (10, 0)), font=("Arial", 14)), sg.Text(qtd_pecas, key='qtd_pecas', size=(15, 1), pad=(0, (10, 0)), font=("Arial", 14))],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((250, 0), 20)),
         sg.Button('Adicionar Produto', size=(15, 1), pad=((30, 0), 20)),
         sg.Button('Nova Venda', button_color="Green", size=(15, 1), pad=((30, 0), 20))]
    ]

    janela = sg.Window("Janela Ver Valores", layout, size=(920, 600))

    while True:
        event, values = janela.read()

        if event == "Adicionar Produto":
            janelaProdutos()
        if event == "Nova Venda":
            janelaCarrinho()
            view = ce.read_file("venda.csv")
            soma = 0
            qtd_pecas = 0
            if len(view) > 0:
                for item in view:
                    qtd_pecas += int(item[2])
                    soma += float(item[1]) * int(item[2])
                for i in range(len(view)):
                    view[i][1] = util.coin_format(str(view[i][1]))

            janela['-TABLE_PRODUCTS-'].update(view)
            janela.Element('soma').update(util.coin_format(str(soma)))
            janela.Element('qtd_pecas').update(qtd_pecas)
        if event == '-TABLE_PRODUCTS-':
            try:
                row_selected = values['-TABLE_PRODUCTS-'][0]
                product_name = str(view[row_selected][0])
                pop_message = f"Tem certeza que deseja excluir o registro de {product_name} da posicao {row_selected}?"
                if sg.popup_yes_no(pop_message) == 'Yes':
                    view = ce.remove_registro("venda.csv", int(row_selected))

                    view = ce.read_file("venda.csv")
                    soma = 0
                    qtd_pecas = 0
                    if len(view) > 0:
                        for item in view:
                            qtd_pecas += int(item[2])
                            soma += float(item[1]) * int(item[2])
                        for i in range(len(view)):
                            view[i][1] = util.coin_format(str(view[i][1]))

                    janela['-TABLE_PRODUCTS-'].update(view)
                    janela.Element('soma').update(util.coin_format(str(soma)))
                    janela.Element('qtd_pecas').update(qtd_pecas)
            except:
                sg.popup_error(f"Erro ao remover item {product_name}")
            janela['-TABLE_PRODUCTS-'].set_focus()


        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()