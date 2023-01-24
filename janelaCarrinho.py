import controle_estoque as ce
import PySimpleGUI as sg
from janelaVenda import janelaVenda
import util

def janelaCarrinho():
    font = ("Halvetica", 10)
    sg.theme("default")
    sg.set_options(font=font)

    view = ce.read_file()
    name_list = list()

    if len(view) > 0:
        for item in view:
            name_list.append(item[0])
    else:
        name_list.append('')


    layout = [
        [sg.Text('Venda de Produto', size=(16, 0), font=("Arial", 24), pad=((360, 0),(70, 10))),
         sg.Image(filename="./assets/shop-cart-icon.png", pad=(0, (70, 10))),
         sg.Text('0 itens', size=(10, 0), font=("Arial", 14), pad=((10, 0), (70, 10)), key="qtd_carrinho")],
        [sg.Text('Selecionar Produto: ', size=(20, 0), pad=((280, 16), (0, 10))),
         sg.Combo(name_list, key='-COMBO-'), sg.Button('Selecionar')],
        [sg.Text('Preco: ', size=(20, 0), pad=((280, 0), 10)),
         sg.Text(util.coin_format('0'), size=(20, 0), pad=((20, 0), 10), key="preco")],
        [sg.Text('Quantidade em Estoque: ', size=(20, 0), pad=((280, 0), 10)),
         sg.Text(f'0 pecas', size=(20, 0), pad=((20, 0), 10), key="qtd_estoque")],
        [sg.Text('Pecas Vendidas: ', size=(20, 0), pad=((280, 0), 10)),
         sg.Input(size=(5, 0), pad=((20, 0), 10), key="qtd_vendida")],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((200, 40), 20)),
         sg.Button('Adicionar', button_color="Blue", size=(15, 1), pad=(40, 20)),
         sg.Button('Vender', button_color="Green", size=(15, 1), pad=(40, 20))]
    ]

    janela = sg.Window("Janela Produtos", layout, size=(920, 600))

    index = -1
    carrinho = list()

    while True:
        event, values = janela.read()
        if event == "Selecionar":
            try:
                if values['-COMBO-'] in name_list:
                    index = int(name_list.index(values['-COMBO-']))
                    preco = view[index][1]
                    janela['preco'].update(util.coin_format(str(preco)))
                    janela['qtd_estoque'].update(f'{view[index][2]} pecas')
            except:
                sg.popup_error("O Produto Selecionado não corresponde na lista!")


        if event == "Adicionar":
            try:
                #Tratamento de erro
                qtd_vendida = int(values['qtd_vendida'])
                if index == -1:
                    sg.popup_ok("Selecione um produto para vender!")
                elif not int(qtd_vendida) > 0:
                    sg.popup_ok("Selecione a quantidade a ser vendida!")
                elif int(qtd_vendida) > int(view[index][2]):
                    sg.popup_ok("Quantidade acima do que tem no estoque!")
                else:
                    dados = []

                    dados.append(index)                 #Index da Compra
                    dados.append(values['-COMBO-'])     #Nome do Produto
                    dados.append(preco)                 #Preço Vendido
                    dados.append(qtd_vendida)           #Quantidade Vendida

                    carrinho.append(dados)              #Adicionando ao carrinho

                    janela['qtd_carrinho'].update(f'{len(carrinho)} itens')
                    sg.popup_ok("Adicionado ao carrinho!")

                    # Limpando os dados
                    janela['qtd_vendida'].update('')
            except:
                sg.popup_error("Erro ao adicionar o produto verifique os campos!")


        if event == "Vender":
            try:
                if(len(carrinho) > 0):
                    carrinho = janelaVenda(carrinho)

                    view = ce.read_file()      #Atualizando o arquivo

                    janela['qtd_carrinho'].update(f'{len(carrinho)} itens')
                else:
                    sg.popup_ok("Carrinho Vazio!", "Por favor, adicione ao menos um produto para concluir uma venda!")
            except:
                sg.popup_error("Erro ao vender o produto!")


        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()