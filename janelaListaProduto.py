import PySimpleGUI as sg
import controle_estoque as ce
from janelaProdutos import janelaProdutos
from janelaEditarProduto import janelaEditarProduto
from util import format_date

def janelaListaProduto():
    font = ("Halvetica", 10)
    sg.theme("LightBlue")
    sg.set_options(font=font)

    view = ce.read_file("produtos.csv")
    for item in view:
        item[3] = format_date(item[3])

    layout = [
        [sg.Text('Produtos Cadastrados', font=("Arial", 24), pad=((320, 0), (50, 10)))],
        [sg.Table(values=view,
        headings=['Produto','Preco Real', 'Qtd Estoque', 'Data Registro'],
        pad=((190, 0), (20, 30)),
        max_col_width=60,
        auto_size_columns=True,
        justification='center',
        display_row_numbers=True,
        alternating_row_color="Light Gray",
        num_rows=10,
        key='-TABLE_PRODUCTS-',
        enable_events=True,
        tooltip='This is a table')],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((320, 0), 20)),
         sg.Button('Adicionar Produto', button_color="Green", size=(15, 1), pad=((50, 0), 20))]
    ]

    janela = sg.Window("Janela Ver Produtos", layout, size=(920, 600))

    while True:
        event, values = janela.read()


        if event == "Adicionar Produto":
            try:
                janelaProdutos()

                #ATUALIZANDO OS DADOS
                view = ce.read_file("produtos.csv")
                janela['-TABLE_PRODUCTS-'].update(view)
            except:
                sg.popup_error("ERRO ao Adicionar um produto novo!")


        if event == '-TABLE_PRODUCTS-':
            try:
                row_selected = values['-TABLE_PRODUCTS-'][0]
                product_name = str(view[row_selected][0])
                product_selected = []
                product_selected.append(row_selected)            #Index do Produto
                product_selected.append(product_name)            #Nome do Produto
                product_selected.append(view[row_selected][1])   #Preco do Produto
                product_selected.append(view[row_selected][2])   #Quantidade do Produto

                janelaEditarProduto(product_selected)

                # ATUALIZANDO OS DADOS
                view = ce.read_file("produtos.csv")
                janela['-TABLE_PRODUCTS-'].update(view)
            except:
                sg.popup_error(f"Produto {product_name} foi editado!")
            janela['-TABLE_PRODUCTS-'].set_focus()


        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()