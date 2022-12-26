import controle_estoque as ce
import PySimpleGUI as sg
import util

def janelaVenda():
    font = ("Halvetica", 10)
    sg.theme("LightBlue")
    sg.set_options(font=font)

    view = ce.read_file()
    name_list = list()
    if len(view) > 0:
        for item in view:
            name_list.append(item[0])

    layout = [
        [sg.Text('Venda de Produto', size=(20, 1), font=("Arial", 24), pad=((220, 0),(70, 10)))],
        [sg.Text('Selecionar Produto: ', size=(20, 0), pad=((200, 16), (0, 10))),
         sg.Combo(name_list, key='-COMBO-'), sg.Button('Selecionar')],
        [sg.Text('Preco: ', size=(20, 0), pad=((200, 0), 10)),
         sg.Text(util.coin_format('0') ,size=(20, 0), pad=((20, 0), 10), key="preco")],
        [sg.Text('Quantidade em Estoque: ', size=(20, 0), pad=((200, 0), 10)),
         sg.Text(f'0 pecas', size=(20, 0), pad=((20, 0), 10), key="qtd_estoque")],
        [sg.Text('Pecas Vendidas: ', size=(20, 0), pad=((200, 0), 10)),
         sg.Input(size=(5, 0), pad=((20, 0), 10), key="qtd_vendida")],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((200, 40), 20)),
         sg.Button('Vender', button_color="Blue", size=(15, 1), pad=(40, 20))]
    ]

    janela = sg.Window("Janela Produtos", layout, size=(720, 480))
    dados = list()

    index = -1
    qtd_vendida = 0

    while True:
        event, values = janela.read()
        if event == "Selecionar":
            if values['-COMBO-'] in name_list:
                index = int(name_list.index(values['-COMBO-']))
                janela['preco'].update(util.coin_format(str(view[index][1])))
                janela['qtd_estoque'].update(f'{view[index][2]} pecas')
                qtd_estoque = view[index][2]
        if event == "Vender":
            try:
                qtd_vendida = int(values['qtd_vendida'])
                if index == -1:
                    sg.popup_ok("Selecione um produto para vender!")
                elif not int(qtd_vendida) > 0:
                    sg.popup_ok("Selecione a quantidade a ser vendida!")
                elif int(qtd_vendida) > int(view[index][2]):
                    sg.popup_ok("Quantidade acima do que tem no estoque!")
                else:
                    ce.buy_produto(index, qtd_vendida)

                    view = ce.read_file()

                    janela['preco'].update(util.coin_format(str(view[index][1])))
                    janela['qtd_estoque'].update(f'{view[index][2]} pecas')

                    sg.popup_ok("Registro de venda adicionado com sucesso!")
            except:
                sg.popup_error("Erro ao vender o produto verifique os campos!")

        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()