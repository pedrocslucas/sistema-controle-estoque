import csv

#Ler o arquivo
def read_file(path="produtos.csv"):
    """
    Função que ler um arquivo csv e o transforma em lista python
    :param path: caminho com o nome e extensão do arquivo csv que deseja ler
    :return: retorna uma lista com todos os dados
    """
    dados = []
    try:
        with open(path, "r", encoding="utf-8") as arquivo:
            file = csv.reader(arquivo, delimiter=";")
            for linha in file:
                dados.append(linha)
    except:
        print("[ERRO] Não foi possível ler o arquivo!")
    else:
        return dados
    return []


#Escrever no arquivo
def writer_file(path="produtos.csv", dados=[]):
    """
        Função que escrever em um arquivo csv
        :param path: caminho com o nome e extensão do arquivo csv que deseja ler
        :return: retorna uma tabela com todos os dados
        """
    try:
        with open(path, "a", encoding="utf-8", newline="") as arquivo:
            file = csv.writer(arquivo, delimiter=";")
            file.writerow(dados)
    except:
        print("[ERRO] Não foi possível escrever no arquivo!")


def writer_new_file(path="produtos.csv", dados=[]):
    """
    Função para reescrever um arquivo novo utilizando array.
    :param path: caminho do arquivo a ser escrito.
    :param dados: array com os dados a serem escritos no arquivo.
    :return: void
    """
    try:
        with open(path, "w", encoding="utf-8", newline="") as arquivo:
            file = csv.writer(arquivo, delimiter=";")
            for linha in dados:
                file.writerow(linha)
    except:
        print("[ERRO] Não foi possível escrever no arquivo!")


def remove_registro(path="produtos.csv", index_element=0):
    """
    Função para remover um elemento na lista com base no indice dele.
    :param path: caminho do arquivo
    :param index_element: indice do elemento a ser removido.
    :return: retorna uma nova lista sem o elemento removido.
    """
    try:
        dados = read_file(path)
        del dados[index_element]
    except:
        print('Erro ao ler o arquivo!')
    else:
        writer_new_file(path, dados)
    return []


def tirar_estoque(index_element, qtd_vendida):
    try:
        dados = read_file("produtos.csv")
        for i in range(len(dados)):
            if index_element == i:
                if qtd_vendida > int(dados[i][2]):
                    print('[ERRO] a quantidade não pode ser vendida')
                else:
                    dados[i][2] = int(dados[i][2]) - qtd_vendida
    except:
        print('Erro ao ler o arquivo!')
    else:
        writer_new_file("produtos.csv", dados)
    return []


def jaTemNoEstoque(item=[], except_item=""):
    try:
        dados = read_file("produtos.csv")
        for produto in dados:
            if produto[0] == item[0] and produto[0] != except_item:
                return True
    except:
        print('Erro ao ler o arquivo!')
    return False


def addVenda(dados=[]):
    try:
        writer_file("venda.csv", dados)
    except:
        print('[ERRO] Não foi possível ler o arquivo')
