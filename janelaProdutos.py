import controle_estoque as ce
import PySimpleGUI as sg
import util

font = ("Halvetica", 10)
sg.theme("LightBlue")
sg.set_options(font=font)

layout = [
    [sg.Text('Cadastro de Produto', size=(20, 1), font=("Arial", 24), pad=((220, 0),(70, 10)))],
    [sg.Text('Nome do Produto: ', size=(20, 0), pad=((200, 0), (30, 10))), sg.Input(size=(20, 0), pad=((20, 0), (30, 10)), key="nome")],
    [sg.Text('Preco: ', size=(20, 0), pad=((200, 0), 10)), sg.Input(size=(10, 0), pad=((20, 0), 10), key="preco")],
    [sg.Text('Quantidade em Estoque: ', size=(20, 0), pad=((200, 0), 10)), sg.Input(size=(5, 0), pad=((20, 0), 10), key="qtd_estoque")],
    [sg.Button('Voltar', button_color="Red", size=(15, 1), pad=((200, 40), 20)), sg.Button('Salvar', button_color="Blue", size=(15, 1), pad=(40, 20))]
]

janela = sg.Window("Janela Produtos", layout, size=(720, 480))
dados = list()

while True:
    event, values = janela.read()
    if event == "Salvar":
        try:
            dados.append(values['nome'])    #Nome Produto
            dados.append(util.convert_float(values['preco']))   #Preço Unitário
            dados.append(int(values['qtd_estoque']))    #Quantidade em Estoque
            dados.append(0)     #Quantidade Vendida
            dados.append(util.get_date_now())   #Data do dia atual
            if ce.jaTemNoEstoque(dados):
                sg.popup_non_blocking("Produto ja cadastrado!")
            else:
                ce.writer_file("produtos.csv", dados)
                sg.popup_ok("Registro de item adicionado com Sucesso!")
        except:
            sg.popup_error("Error ao adicionar um registro de item!")
        #Limpando os dados do input
        janela['nome'].update('')
        janela['preco'].update('')
        janela['qtd_estoque'].update('')
        dados.clear()

    if event == sg.WIN_CLOSED or event == "Voltar":
        break

janela.close()