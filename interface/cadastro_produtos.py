import PySimpleGUI as psg
import sqlite3


def cadastrar_produto(nome, quantidade, categoria, descricao):
    try:
        con = sqlite3.connect('tables/produtos.db')
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Produto TEXT NOT NULL,
                            Quantidade INTEGER NOT NULL,
                            Categoria TEXT NOT NULL,
                            Descricao TEXT NOT NULL)''')

        if not nome or not quantidade or not categoria or not descricao:
            psg.popup('Todos os campos são obrigatórios.',
                      background_color='white',
                      text_color='black',
                      button_color=('black', 'white'))
        elif not quantidade.isdigit():
            psg.popup('A quantidade deve ser um número inteiro.',
                      background_color='white',
                      text_color='black',
                      button_color=('black', 'white'))
        else:
            cursor.execute('''INSERT INTO Produtos
                            (Produto, Quantidade, Categoria, Descricao)
                                VALUES (?, ?, ?, ?)''', (nome, quantidade,
                                                         categoria, descricao))
            con.commit()
            psg.popup('Produto Cadastrado',
                      background_color='white',
                      text_color='black',
                      button_color=('black', 'white'))
        con.close()
    except sqlite3.Error as e:
        psg.popup(f'Ocorreu um erro: {str(e)}',
                  background_color='white',
                  text_color='black',
                  button_color=('black', 'white'))


class Produtos:

    def __init__(self):
        azul = '#4A3CAE'

        title = [psg.Text('Sistema de Vendas', font=('Helvetica 30 bold'),
                          size=70,
                          text_color='white', background_color=azul,
                          pad=(0, 0), justification='c')]

        button_event = [
            [psg.Button(key='voltar', button_color=('white', 'white'),
                        image_filename='interface/images/1216.png',
                        image_subsample=2, border_width=0)]
        ]

        title_cadastro = [psg.Text('Cadastrar Produtos', font=('Any 20 bold'),
                                   size=40, pad=(20, 20),
                                   background_color='white',
                                   text_color='gray', justification='c')]

        left_column = [
            title_cadastro,
            [psg.Text('Nome do Produto: *', background_color='white',
                      text_color='black', pad=(30, 5))],

            [psg.InputText(size=55, pad=(20, 5), key='produto')],
            [psg.Text('Quantidade: *', background_color='white',
                      text_color='black', pad=(30, 5))],

            [psg.InputText(size=55, pad=(20, 5), key='quantidade')],
            [psg.Text('Categoria: *', background_color='white',
                      text_color='black', pad=(30, 5))],

            [psg.InputText(size=55, pad=(20, 5), key='categoria')],
            [psg.Text('Descrição: *', background_color='white',
                      text_color='black', pad=(30, 5))],

            [psg.InputText(size=55, pad=(20, 5), key='descricao')],
            [psg.Button('Cadastrar', pad=(50, 30),
                        button_color=('white', azul), size=15),
                psg.Button('Limpar Campos', pad=(10, 30))]
        ]

        layout = [
            title,
            [psg.Column(button_event, justification='left',
                        background_color='white')],
            [psg.Column(left_column, justification='center',
                        background_color='white')],
        ]

        window = psg.Window('Cadastrar Produtos', layout,
                            use_custom_titlebar=True,
                            background_color='white',
                            font='Helvetica 14 italic',
                            finalize=True,
                            resizable=True,
                            location=(300, 100),
                            grab_anywhere=True,
                            button_color=('black', 'white'),
                            size=(800, 650), )

        while True:

            event, value = window.read()
            if event == psg.WINDOW_CLOSED:
                break

            if event == 'voltar':
                window.close()
                from main_code import Start
                Start()

            elif event == 'Cadastrar':
                nome = value['produto']
                quantidade = value['quantidade']
                categoria = value['categoria']
                descricao = value['descricao']

                cadastrar_produto(nome, quantidade, categoria, descricao)

            elif event == 'Limpar Campos':
                window.Element('produto').update('')
                window.Element('quantidade').update('')
                window.Element('categoria').update('')
                window.Element('descricao').update('')
                window['produto'].set_focus()

        window.close()
