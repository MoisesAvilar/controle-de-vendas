import PySimpleGUI as psg
import sqlite3


def table_exists(database, table_name):
    try:
        con = sqlite3.connect(database)
        cursor = con.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        tabela = cursor.fetchone()
        con.close()
        return tabela is not None
    except sqlite3.Error:
        return False


def carregar_produtos():
    con = sqlite3.connect('tables/produtos.db')
    curso = con.cursor()
    curso.execute('''SELECT Produto, Quantidade,
                  Categoria, Descricao from Produtos''')
    dados = curso.fetchall()
    return dados


def verifica_estoque(quantidade, disponivel):
    if quantidade > disponivel:
        return psg.popup('Quantidade não disponível', background_color='white',
                         text_color='black',
                         button_color=('black', 'white'))

    elif quantidade < 1:
        return psg.popup('Quantidade inválida', background_color='white',
                         text_color='black', button_color=('black', 'white'))


def registrar_venda(produto, valor, quantidade, codigo, descricao):
    con = sqlite3.connect('tables/vendas.db')
    curso = con.cursor()
    curso.execute('''CREATE TABLE IF NOT EXISTS Vendas
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Produto TEXT NOT NULL,
                        Categoria TEXT NOT NULL,
                        Descricao TEXT NOT NULL,
                        Quantidade INT NOT NULL,
                        Valor REAL NOT NULL)''')
    curso.execute('''INSERT INTO Vendas
                        (Produto, Categoria, Descricao, Quantidade, Valor)
                        VALUES (?, ?, ?, ?, ?)''', (produto, codigo, descricao,
                                                    quantidade, valor))
    con.commit()
    con.close()


def registrar_vendas(lista_listbox, window):
    produtos = {
        'nome': [],
        'categoria': [],
        'descricao': [],
        'quantidade': [],
        'valor': []
    }

    for item in lista_listbox:
        elementos = item[0].split(' ')
        quantidade_valor = item[1].split(' ')

        produto = {
            'nome': elementos[1],
            'categoria': elementos[4],
            'descricao': elementos[7],
            'quantidade': int(quantidade_valor[1]),
            'valor': float(quantidade_valor[4].replace('R$', ''))
        }

        produtos['nome'].append(produto['nome'])
        produtos['categoria'].append(produto['categoria'])
        produtos['descricao'].append(produto['descricao'])
        produtos['quantidade'].append(produto['quantidade'])
        produtos['valor'].append(produto['valor'])

    conn = sqlite3.connect('tables/vendas.db')
    curso = conn.cursor()

    curso.execute('''CREATE TABLE IF NOT EXISTS Vendas
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Produto TEXT NOT NULL,
                        Categoria TEXT NOT NULL,
                        Descricao TEXT NOT NULL,
                        Quantidade INT NOT NULL,
                        Valor REAL NOT NULL)''')

    for i in range(len(produtos['nome'])):
        curso.execute('''INSERT INTO Vendas
                        (Produto, Categoria, Descricao, Quantidade, Valor)
                        VALUES (?, ?, ?, ?, ?)''', (produtos['nome'][i],
                                                    produtos['categoria'][i],
                                                    produtos['descricao'][i],
                                                    produtos['quantidade'][i],
                                                    produtos['valor'][i]))

        con = sqlite3.connect('tables/produtos.db')
        curs = con.cursor()
        curs.execute('''UPDATE Produtos
                     SET Quantidade = Quantidade - ?
                     WHERE Produto = ?''',
                     (produtos['quantidade'][i], produtos['nome'][i]))

        con.commit()
        con.close()
    conn.commit()
    conn.close()
    psg.popup('Os produtos foram salvos',
              background_color='white',
              text_color='black',
              button_color=('black', 'white'))


def validar_real(numero):
    while True:
        try:
            real = float(numero.replace(',', '.'))
        except (ValueError, TypeError):
            psg.popup('Insira o valor correto', background_color='white',
                      text_color='black', button_color=('black', 'white'))
        else:
            return real


class Vendas:

    def __init__(self):
        roxo = '#550681'

        itens = carregar_produtos()
        deposito = [deposito[1] for deposito in itens]
        dados = []
        linha_info = []
        lista_listbox = []

        for item in itens:
            dados.append(
                f'Item {item[0]} - Categoria {item[2]} - Descrição {item[3]}'
                )
        title = [psg.Text('Sistema de Vendas', font=('Helvetica 30 bold'),
                          size=70, text_color='white', background_color=roxo,
                          pad=(0, 0), justification='center')]

        button_event = [
            [psg.Button(key='voltar', button_color=('white', 'white'),
                        image_filename='interface/images/1216.png', image_subsample=2,
                        border_width=0)]
        ]

        second_title = [
            psg.Text('Registrar Vendas', font=('Any 20 bold'), size=40,
                     background_color='white',
                     text_color='gray', justification='center')
        ]

        botoes = [
            [psg.Button('Adicionar Venda', pad=(30, 30))],
        ]

        janela_vendas = [
            [psg.Listbox([linha_info], key='lista', bind_return_key=True,
                         sbar_background_color=roxo,
                         size=(70, 5), font=8, pad=(20, 10))],
        ]

        vender_itens = [
            [psg.Button('Registrar Itens', button_color=('white', roxo),
                        size=(15, 2), pad=(0, 15))]
        ]

        lista_produtos = [
            second_title,
            [psg.Text('Escolher Produto', text_color='black',
                      background_color='white', pad=(30, 5))],
            [psg.Combo(dados, pad=(20, 5), size=60, readonly=True,
                       enable_events=True, key='combo',
                       text_color='black', button_background_color=roxo,
                       background_color='white',)],

            [psg.Text('Disponível no depósito:', text_color='black',
                      background_color='white', pad=(30, 5)),
                psg.Text(key='disponivel', background_color='white',
                         text_color='black', pad=(0, 0))],
            [psg.Text('Valor da Venda R$', pad=(30, 5),
                      background_color='white', text_color='black'),
                psg.Input(key='valor', size=5, justification='r'),
                psg.Text('Digite a quantidade', background_color='white',
                         text_color='black', pad=(30, 5)),
                psg.Input(key='quantidade', size=5, justification='r')],
        ]

        layout = [
            title,
            [psg.Column(button_event, justification='left',
                        background_color='white')],
            [psg.Column(lista_produtos, justification='center',
                        background_color='white')],
            [psg.Column(botoes, justification='center',
                        background_color='white')],
            [psg.Column(janela_vendas, justification='center',
                        background_color='white')],
            [psg.Column(vender_itens, justification='center',
                        background_color='white')]
        ]

        window = psg.Window('Registrar Vendas', layout,
                            use_custom_titlebar=True, background_color='white',
                            font='Helvetica 14 italic', finalize=True,
                            resizable=True,
                            location=(300, 0), grab_anywhere=True,
                            button_color=('black', 'white'),
                            size=(800, 700))

        while True:
            event, value = window.read()
            if event == psg.WINDOW_CLOSED:
                break

            if event == 'voltar':
                import main_code
                window.close()
                main_code.Start()

            elif event == 'combo':
                produto = value['combo']
                position = dados.index(value['combo'])
                window['disponivel'].update(deposito[position])

            elif event == 'Adicionar Venda':
                if not value['quantidade'] or not window['valor'].get() or not window['disponivel'].get():
                    psg.popup('Preencha todos os campos corretamente',
                              background_color='white',
                              text_color='black',
                              button_color=('black', 'white'))
                else:
                    disponivel_str = window['disponivel'].get()
                    if disponivel_str.isdigit():
                        disponivel = int(disponivel_str)
                        if disponivel == 0:
                            psg.popup('Quantidade não disponível',
                                      background_color='white',
                                      text_color='black',
                                      button_color=('black', 'white'))
                        else:
                            valor = validar_real(window['valor'].get())
                            quantidade = int(value['quantidade'])
                            verifica_estoque(quantidade, disponivel)

                            linha_info.append(value['combo'])
                            linha_adicional = f'Quantidade {quantidade} - Valor R${(valor * quantidade):.2f}'
                            nova_lista = [linha_info[-1], linha_adicional]
                            lista_listbox.append(nova_lista)
                            lista_strings = [" - ".join(lista) for lista in lista_listbox]
                            window.Element('lista').update(lista_strings)
                            window.Element('disponivel').update('')
                            window.Element('valor').update('')
                            window.Element('quantidade').update('')
                    else:
                        psg.popup('Quantidade disponível inválida',
                                  background_color='white',
                                  text_color='black',
                                  button_color=('black', 'white'))

            elif event == 'lista':
                valor_selecionado = value['lista'][0]
                escolha = psg.popup_yes_no('Deseja deletar esse item?',
                                           background_color='white',
                                           text_color='black',
                                           button_color=('black', 'white'))

                if escolha == 'Yes':
                    posicao = lista_strings.index(valor_selecionado)
                    lista_strings.pop(posicao)
                    lista_listbox.pop(posicao)
                    lista_strings = [" - ".join(lista) for lista in
                                     lista_listbox]
                    window['lista'].update(lista_strings)

            elif event == 'Registrar Itens':
                if not lista_listbox:
                    psg.popup('Não há vendas registradas ainda',
                              background_color='white',
                              text_color='black',
                              button_color=('black', 'white'))
                else:
                    for venda in lista_listbox:
                        produto = venda[0]
                        quantidade_str = venda[1].split('-')[0].strip().replace('Quantidade ', '')
                        quantidade_vendida = int(quantidade_str)
                        position = dados.index(produto)
                        deposito[position] -= quantidade_vendida
                        window['disponivel'].update(deposito[position])

                    registrar_vendas(lista_listbox, window)
                    lista_listbox.clear()
                    window['disponivel'].update('')
                    window['valor'].update('')
                    window['lista'].update('')

        window.close()
