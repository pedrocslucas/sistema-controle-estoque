import PySimpleGUI as sg
import controle_estoque as ce
from janelaProdutos import janelaProdutos


font = ("Halvetica", 10)
sg.theme("LightBlue")
sg.set_options(font=font)

modo_list = []
date_list = []

view = ce.read_file("produtos.csv")

layout = [
    [sg.Text('Produtos Cadastrados', font=("Arial", 24), pad=((320, 0), (50, 10)))],
    [sg.Table(values=view,
    headings=['Produto','Preco Real', 'Qtd Estoque', 'Data Registro'],
    pad=((190, 0), (20, 30)),
    max_col_width=50,
    auto_size_columns=True,
    justification='center',
    display_row_numbers=True,
    alternating_row_color="Light Gray",
    num_rows=10,
    key='-TABLE_PRODUCTS-',
    enable_events=True,
    tooltip='This is a table')],
    [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((230, 0), 20)),
     sg.Button('Editar Produto', button_color="Olive", size=(15, 1), pad=((50, 0), 20)),
     sg.Button('Adicionar Produto', button_color="Green", size=(15, 1), pad=((50, 0), 20))]
]

janela = sg.Window("Janela Ver Produtos", layout, size=(920, 600))

while True:
    event, values = janela.read()

    if event == "Editar Produto":
        continue


    if event == "Adicionar Produto":
        janelaProdutos()

        view = ce.read_file("produtos.csv")

        #ATUALIZANDO OS DADOS
        janela['-TABLE_PRODUCTS-'].update(view)


    if event == '-TABLE_PRODUCTS-':
        try:
            row_selected = values['-TABLE_PRODUCTS-'][0]
            product_name = str(view[row_selected][0])
            pop_message = f"Tem certeza que deseja excluir o registro de {product_name} da posicao {row_selected}?"
            if sg.popup_yes_no(pop_message) == 'Yes':
                view = ce.remove_registro("produtos.csv", int(row_selected))

            view = ce.read_file("produtos.csv")

            # ATUALIZANDO OS DADOS
            janela['-TABLE_PRODUCTS-'].update(view)
        except:
            sg.popup_error(f"Erro ao remover item {product_name}")
        janela['-TABLE_PRODUCTS-'].set_focus()


    if event == sg.WIN_CLOSED or event == "Voltar":
        break

janela.close()