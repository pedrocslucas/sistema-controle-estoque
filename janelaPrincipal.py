import PySimpleGUI as sg
from janelaProdutos import janelaProdutos
from janelaValoresTotais import janelaVerTotal
from janelaCarrinho import janelaCarrinho

def janelaPrincipal():
    font = ("Halvetica", 10)
    sg.theme("LightBlue")
    sg.set_options(font=font)

    layout = [
        [sg.Image(filename="./assets/add-shop-icon.png", pad=((30, 30), (50, 10))),
         sg.Image(filename="./assets/add-registro-icon.png", pad=(30, (50, 10))),
         sg.Image(filename="./assets/see-table-icon.png", pad=(30, (50, 10)))],
        [sg.Button('Vender Produto', button_color="Green", size=(15, 2), pad=((70, 0), 10)),
         sg.Button('Cadastrar Produto', size=(15, 2), pad=((100, 0), 10)),
         sg.Button('Ver Total', button_color="Olive", size=(15, 2), pad=((100, 0), 10))]
    ]

    janela = sg.Window("Janela Principal", layout, size=(720, 480))

    while True:
        event, values = janela.read()
        if event == "Cadastrar Produto":
            janelaProdutos()
        if event == "Ver Total":
            janelaVerTotal()
        if event == "Vender Produto":
            janelaVenda()
        if event == sg.WIN_CLOSED:
            break

    janela.close()