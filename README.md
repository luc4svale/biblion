# Biblion | Sistema de Gerenciamento de Biblioteca Digital

Visão Geral
O projeto Biblion foi criado para oferecer uma solução completa para o gerenciamento de bibliotecas digitais. A aplicação possibilita que usuários cadastrem-se, façam login, realizem buscas, visualizem detalhes dos livros e salvem seus títulos favoritos. Além disso, administradores dispõem de uma área exclusiva para gerenciar o conteúdo – incluindo livros, autores, categorias e editoras – com uma interface baseada no template SB Admin 2.

Recursos
Gerenciamento de Livros: Cadastro, atualização, visualização e remoção de livros.
Gerenciamento de Autores: Inclusão e manutenção dos dados dos autores.
Categorias e Editoras: Organização dos livros por categorias e editoras.
Autenticação e Autorização: Sistema completo de registro, login e controle de acesso com Flask-Login.
Área Administrativa: Interface administrativa intuitiva baseada no template SB Admin 2.
Favoritos: Permite que os usuários salvem livros de interesse para acesso rápido.
Uploads de Arquivos: Funcionalidade para upload de imagens, arquivos PDF e outros conteúdos relacionados aos livros.

Tecnologias Utilizadas
Linguagem: Python 3.x
Framework Web: Flask
Banco de Dados: SQLAlchemy (configurável via variável de ambiente, com opção padrão para SQLite)
Autenticação: Flask-Login e Flask-Bcrypt para segurança
Migrações: Flask-Migrate para gerenciamento das alterações no banco de dados
Templates: Jinja2
Frontend: HTML5, CSS3, JavaScript e o template SB Admin 2

Instalação
Siga os passos abaixo para configurar e executar o projeto localmente:

Clone o repositório:

Copiar:
git clone git clone https://github.com/luc4svale/biblion.git
cd biblion

Crie e ative um ambiente virtual:

Copiar:
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
Instale as dependências:

Copiar:
pip install -r requirements.txt
Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto com as seguintes configurações básicas:

env
Copiar:
FLASK_APP=biblion/app
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta
DATABASE_URL=sqlite:///biblion.db

Execute as migrações do banco de dados:

Copiar
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
Configuração
Variáveis de Ambiente: Ajuste o arquivo .env conforme as necessidades do ambiente (desenvolvimento, produção, etc.).
Banco de Dados: A configuração padrão utiliza SQLite, mas você pode alterar para outro SGBD modificando a variável DATABASE_URL.
Segurança: Certifique-se de definir uma SECRET_KEY forte para a segurança da aplicação.