import PySimpleGUI as sg
from janelaPrincipal import janelaPrincipal

font = ("Halvetica", 10)
sg.set_options(font=font)

layout = [
    [sg.Text("Login: ", pad=((150, 16), (80, 10))), sg.Input(size=(15, 1), key='login', pad=(0, (80, 10)))],
    [sg.Text("Senha: ", pad=((150, 10), 10)), sg.Input(size=(15, 1), key='password', password_char='*', pad=(0, 10))],
    [sg.Button("Entrar", button_color="Green", size=(10, 1), pad=((190, 0), 10), bind_return_key=True)]
]

janela = sg.Window('Tela Login', layout, size=(480, 320), finalize=True)

access_system = ['admin', '12345']

while True:
    event, values = janela.read()

    if event == 'Entrar':
        try:
            login = values['login']
            password = values['password']
            if str(login) == str(access_system[0]) and str(password) == str(access_system[1]):
                sg.popup("Login feito com SUCESSO!", auto_close=True, auto_close_duration=1)
                janela['login'].update('')
                janela['password'].update('')
                janela['login'].set_focus()
                janelaPrincipal()
            else:
                sg.popup_error("Usuario ou senha incorretos!")
        except:
            sg.popup_error("ERRO ao efetuar o login!")


    if event == sg.WIN_CLOSED:
        break

janela.close()