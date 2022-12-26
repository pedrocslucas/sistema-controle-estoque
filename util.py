def coin_format(num):
    if (num.replace(',', '')).replace('.', '').isnumeric():
        valor = float(num.replace(',', '.'))
        valor_real = "R${:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
        return valor_real
    else:
        print("Não é um numero!")
        return 0


def convert_float(num):
    return num.replace(',', '.')


def get_date_now():
    from datetime import date
    data_default = date.today()
    data = f'{data_default.day}/{data_default.month}/{data_default.year}'
    return data

