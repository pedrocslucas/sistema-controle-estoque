import controle_estoque as ce
import PySimpleGUI as sg
import util

def janelaVenda(carrinho=[]):
    font = ("Halvetica", 10)
    sg.theme("default")
    sg.set_options(font=font)

    view = list()
    preco_total = 0

    if len(carrinho) > 0:
        for item in carrinho:
            view.append(item)
            preco_total += util.convert_float(item[2]) * item[3]

    layout = [
        [sg.Text('Finalizar Venda', size=(16, 0), font=("Arial", 24), pad=((360, 0),(70, 10)))],
        [sg.Table(values=view,
            headings=['Index', 'Produto','Preco Vendido', 'Qtd Vendida'],
            pad=((200, 0), 10),
            max_col_width=50,
            auto_size_columns=True,
            justification='center',
            display_row_numbers=True,
            alternating_row_color="Light Gray",
            num_rows=5,
            key='-TABLE_PRODUCTS-',
            enable_events=True,
            tooltip='This is a table')],
        [sg.Text('Forma de Pagamento: ', size=(20, 0), pad=((240, 0), 10)),
         sg.Radio('Crédito', 'modalidade', key='credit'),
         sg.Radio('Pix', 'modalidade', key='pix'),
         sg.Radio('Débito', 'modalidade', key='debit'),
         sg.Radio('Dinheiro', 'modalidade', default=True, key='cash')],
        [sg.Text('Total a Pagar: ', size=(20, 0), pad=((240, 0), 10)),
         sg.Text(util.coin_format(str(preco_total)), size=(20, 0), pad=((20, 0), 10), key="preco_total")],
        [sg.Text('Aplicar Desconto: ', size=(20, 0), pad=((240, 0), 10)),
         sg.Input(size=(5, 0), pad=((20, 0), 10), key="preco_vendido")],
        [sg.Button('Cancelar', button_color="Red", size=(15, 1), pad=((300, 40), 20)),
         sg.Button('Finalizar', button_color="Green", size=(15, 1), pad=(40, 20))]
    ]

    janela = sg.Window("Janela Produtos", layout, size=(920, 600))
    lista_de_compra = list()

    while True:
        event, values = janela.read()

        if event == '-TABLE_PRODUCTS-':
            try:
                row_selected = values['-TABLE_PRODUCTS-'][0]
                product_name = str(view[row_selected][0])
                pop_message = f"Tem certeza que deseja excluir o produto {product_name} da posicao {row_selected}?"
                if sg.popup_yes_no(pop_message) == 'Yes':

                    del carrinho[row_selected]      #Deletando item do carrinho de compras

                    view = []
                    preco_total = 0
                    if len(carrinho) > 0:
                        for item in carrinho:
                            view.append(item)
                            preco_total += util.convert_float(item[2]) * item[3]

                    janela['-TABLE_PRODUCTS-'].update(view)
                    janela.Element('preco_total').update(util.coin_format(str(preco_total)))
            except:
                sg.popup_error(f"Erro ao remover item {product_name}")
            janela['-TABLE_PRODUCTS-'].set_focus()


        if event == "Finalizar":
            preco_vendido = values["preco_vendido"]

            print(f'values[preco_vendido] = {preco_vendido}')

            if len(str(preco_vendido)) > 0:
                preco_vendido = util.convert_float(preco_vendido)
            else:
                preco_vendido = util.convert_float(preco_total)

            #Modalidade
            if janela['credit'] == True:
                modalidade = 'Crédito'
            elif janela['pix'] == True:
                modalidade = 'Pix'
            elif janela['debit'] == True:
                modalidade = 'Débito'
            else:
                modalidade = 'Dinheiro'

            #Registrando Venda

            diferenca = preco_total - preco_vendido
            print(f'Diferenca: {diferenca}')
            print(f'preco_total: {preco_total}')
            print(f'preco_vendido: {preco_vendido}')
            desconto_aplicado = False

            if len(carrinho) > 0:
                for i in range(len(carrinho)):

                    ce.tirar_estoque(carrinho[i][0], carrinho[i][3]) #Tirando quantidade vendida do estoque
                    del carrinho[i][0]                        #Deletando o indice do produto

                    dados = []

                    dados.append(carrinho[i][0])              #Adicionando Nome do Produto

                    print(f'Preco: {carrinho[i][1]}')

                    if util.convert_float(carrinho[i][1]) > diferenca and not desconto_aplicado:
                        dados.append(util.convert_float(carrinho[i][1])-diferenca)  #Adicionando Preco do Produto
                        desconto_aplicado = True
                    else:
                        dados.append(util.convert_float(carrinho[i][1]))   #Adicionando Preco do Produto

                    dados.append(carrinho[i][2])       #Adicionando Quantidade Vendida do Produto
                    dados.append(modalidade)           #Adicionando Modalidade de Venda
                    dados.append(util.get_date_now())  #Adicionando Data Atual

                    lista_de_compra.append(dados)      #Adicionando na Lista de Compras

                for peca in lista_de_compra:
                   ce.addVenda(peca)       #Adicionando Nova Venda ao Arquivo

            sg.popup_ok("Registro de venda adicionado com sucesso!")

            #Limpando os dados
            janela['preco_vendido'].update('')
            lista_de_compra.clear()
            carrinho.clear()
            view = list()
            janela['-TABLE_PRODUCTS-'].update(view)
            janela['preco_total'].update(0)

        if event == sg.WIN_CLOSED or event == "Cancelar":
            break

    janela.close()

    return carrinho