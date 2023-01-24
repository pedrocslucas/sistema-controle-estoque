def coin_format(num):
    if (num.replace(',', '')).replace('.', '').isnumeric():
        valor = float(num.replace(',', '.'))
        valor_real = "R${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
        return valor_real
    else:
        print("Não é um numero!")
        return 0


def convert_float(num):
    try:
        valor = float(num.replace(',', '.'))
    except:
        print('[ERRO] Não é um número válido!')
        return -1
    else:
        return valor


def get_date_now():
    from datetime import date
    data_default = date.today()
    return data_default


def format_date(date_now=''):
    from datetime import datetime
    data_default = datetime.strptime(date_now, '%Y-%m-%d').date()
    data = f'{data_default.day}/{data_default.month}/{data_default.year}'
    return data


def convert_to_date(str_date='01/01/2000'):
    from datetime import datetime
    data_default = datetime.strptime(str_date, '%d/%m/%Y').date()
    return data_default