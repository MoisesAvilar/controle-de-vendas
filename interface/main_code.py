import PySimpleGUI as psg

import cadastro_produtos
from registro_vendas import table_exists, Vendas


class Start:
    def __init__(self):
        branca = '#FFFFFF'
        preta = '#000000'
        roxo = '#550681'
        amarelo = '#C1C100'
        cinza = '#999999'

        titulo = [
            [psg.Text('Bem-vindo ao APP', size=70, text_color=branca,
                      background_color=roxo, pad=(0, 0),
                      justification='center')]
        ]

        opcao = [
            [psg.Button('Cadastrar Produtos', button_color=(preta, amarelo),
                        pad=(5, 100)),
                psg.Button('Registrar Vendas', button_color=(preta, amarelo))]
        ]

        layout = [
            titulo,
            [psg.Column(opcao, justification='c', background_color=cinza)]

        ]

        window = psg.Window('Tela Inicial', background_color=cinza,
                            size=(700, 350), location=(500, 170),
                            button_color=(branca, preta),
                            use_custom_titlebar=True,
                            font='Helvetica 14 italic',).layout(layout)

        while True:
            event, value = window.read()
            if event == psg.WINDOW_CLOSED:
                break
            elif event == 'Registrar Vendas':
                if table_exists('tables/produtos.db', 'Produtos'):
                    window.close()
                    Vendas()
                else:
                    psg.popup('A tabela de produtos não existe. Por favor,'
                              'cadastre produtos primeiro.',
                              background_color='white',
                              text_color='black',
                              button_color=('black', 'white'))

            elif event == 'Cadastrar Produtos':
                window.close()
                cadastro_produtos.Produtos()

        window.close()


Start()
