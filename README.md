# Controle de Vendas

O Controle de Vendas é uma aplicação de software desenvolvida para auxiliar na gestão de vendas e controle de estoque. Com um foco na simplicidade e usabilidade, o projeto oferece uma interface intuitiva para o cadastro de produtos, registro de vendas e visualização de histórico de transações.

## Principais Recursos:
**Cadastro de Produtos:** Permite a inserção de informações detalhadas sobre os produtos em estoque, incluindo nome, categoria, descrição, quantidade disponível e preço.

**Registro de Vendas:** Facilita o registro de vendas, permitindo aos usuários selecionar produtos, quantidades e preços para criar transações de venda. Também realiza automaticamente a atualização do estoque.

**Visualização de Vendas:** Oferece a capacidade de visualizar o histórico de vendas registradas, incluindo informações sobre produtos vendidos, datas e valores. 

## Estrutura do Projeto:
**functions:** Contém funções utilitárias essenciais para diferentes partes do projeto. Contém módulos específicos para funcionalidades como cadastro de produtos, registro de vendas e visualização de vendas.

**interface:** Abriga os códigos relacionados à interface gráfica da aplicação, incluindo telas iniciais e elementos visuais.

**tables:** Armazena os arquivos de banco de dados utilizados para manter os registros de produtos e vendas.

## Requisitos de Instalação:
Para executar o projeto, é necessário ter o Python instalado no seu sistema. Você também deve instalar a biblioteca PySimpleGUI usando o pip:

    ```bash
    pip install PySimpleGUI

## Como Usar:

1. Execute o arquivo `main_code.py` para iniciar a aplicação.

2. A partir da tela inicial, você pode escolher entre "Cadastrar Produtos" e "Registrar Vendas".

3. Ao clicar em "Cadastrar Produtos", você pode inserir informações sobre novos produtos em estoque.

4. Ao clicar em "Registrar Vendas", é possível realizar transações de venda, selecionando produtos e quantidades.

5. A aplicação manterá um histórico de vendas que pode ser visualizado a qualquer momento.

Espero que o Controle de Vendas seja útil para o controle eficaz de vendas e estoque. Fique à vontade para contribuir, relatar problemas ou sugerir melhorias!