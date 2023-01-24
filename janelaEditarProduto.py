import controle_estoque as ce
import PySimpleGUI as sg
import util

def janelaEditarProduto(product_selected):

    font = ("Halvetica", 10)
    sg.theme("LightBlue")
    sg.set_options(font=font)

    layout = [
        [sg.Text('Editar Produto', size=(20, 1), font=("Arial", 24), pad=((260, 0),(70, 10)))],
        [sg.Text('Nome do Produto: ', size=(20, 0), pad=((200, 0), (30, 10))),
         sg.Input(product_selected[1], size=(20, 0), pad=((20, 0), (30, 10)), key="nome")],
        [sg.Text('Preco: ', size=(20, 0), pad=((200, 0), 10)),
         sg.Input(product_selected[2], size=(10, 0), pad=((20, 0), 10), key="preco")],
        [sg.Text('Quantidade em Estoque: ', size=(20, 0), pad=((200, 0), 10)),
         sg.Input(product_selected[3], size=(5, 0), pad=((20, 0), 10), key="qtd_estoque")],
        [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((140, 20), 20)),
         sg.Button('Excluir', button_color="Olive", size=(15, 1), pad=(20, 20)),
         sg.Button('Editar', button_color="Green", size=(15, 1), pad=(20, 20))]
    ]

    janela = sg.Window("Janela Produtos", layout, size=(720, 480))
    dados = list()

    while True:
        event, values = janela.read()

        if event == "Editar":
            try:
                dados.append(values['nome'])    #Nome Produto
                dados.append(util.convert_float(values['preco']))   #Preço Unitário
                dados.append(int(values['qtd_estoque']))    #Quantidade em Estoque
                dados.append(util.get_date_now())   #Data do dia atual
                if ce.jaTemNoEstoque(dados, product_selected[1]):
                    sg.popup_error("Produto ja foi registrado antes!")
                else:
                    ce.remove_registro("produtos.csv",
                                       int(product_selected[0]))  # Excluindo o produto antes de editar novo
                    ce.writer_file("produtos.csv", dados)
                    sg.popup_ok("Novo produto registrado com SUCESSO!")
            except:
                sg.popup_error("Error ao adicionar um registro de item!")
            #Limpando os dados do input
            dados.clear()
            break


        if event == 'Excluir':
            try:
                product_name = product_selected[1]
                pop_message = f"Tem certeza que deseja excluir o produto {product_name} da posicao {product_selected[0]}?"
                if sg.popup_yes_no(pop_message) == 'Yes':
                    ce.remove_registro("produtos.csv", int(product_selected[0]))        #Excluindo o produto do arquivo
            except:
                sg.popup_error(f"Erro ao remover item {product_name}")
            break


        if event == sg.WIN_CLOSED or event == "Voltar":
            break

    janela.close()