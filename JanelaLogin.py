import PySimpleGUI as sg
from janelaPrincipal import janelaPrincipal

font = ("Halvetica", 10)
sg.set_options(font=font)

layout = [
    [sg.Text("Login: ", pad=((150, 16), (80, 10))), sg.Input(size=(15, 1), key='login', pad=(0, (80, 10)))],
    [sg.Text("Senha: ", pad=((150, 10), 10)), sg.Input(size=(15, 1), key='password', pad=(0, 10))],
    [sg.Button("Entrar", button_color="Green", size=(10, 1), pad=((190, 0), 10))]
]

janela = sg.Window('Tela Login', layout, size=(480, 320))

access_system = ['admin', '12345']

while True:
    event, values = janela.read()
    if event == 'Entrar':
        login = values['login']
        password = values['password']
        if str(login) == str(access_system[0]) and str(password) == str(access_system[1]):
            sg.popup_ok("Login feito com SUCESSO!")
            janela['login'].update('')
            janela['password'].update('')
            janela['login'].set_focus()
            janelaPrincipal()
        else:
            sg.popup_error("Usuario ou senha incorretos!")
    if event == sg.WIN_CLOSED:
        break

janela.close()