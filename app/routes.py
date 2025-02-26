from flask import render_template, request, jsonify, redirect, url_for
from app.controllers.auth_controller import register_user
from app.controllers.book_controller import register_book


def init_routes(app):
    """Função para registrar as rotas na aplicação"""

    @app.route('/')
    def intro():
        return render_template('public/index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            response = {
                "email": email, 
                "password": password
            }
            return jsonify(response)
        return render_template('public/login.html')

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            user = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email": request.form['email'],
                "password": request.form['password'],
                "confirm_password": request.form['confirm_password'], 
            }

            return jsonify(register_user(user))

        return render_template('public/register.html')

    @app.route('/forgot-password')
    def forgot_password():
        return render_template('public/forgot-password.html')

    @app.route('/home')
    def home():
        return render_template('private/home.html')

    @app.route('/book-details')
    def book_details():
        return render_template('private/book-details.html')

    @app.route('/reading')
    def reading():
        return render_template('private/reading.html')

    @app.route('/favorites')
    def favorites():
        return render_template('private/favorites.html')

    @app.route('/profile')
    def profile():
        return render_template('private/profile.html')
    
    @app.route('/book-register', methods=['GET', 'POST'])
    def register_book_route():
        if request.method == 'POST':
            # Chama a função do controller para registrar o livro
            result = register_book(request.form, request.files)

            # Se o resultado for None, houve erro no cadastro
            if result is None:
                return redirect(url_for('register_book_route'))

            # Se o cadastro for bem-sucedido, redireciona para a página de cadastro
            return redirect(url_for('register_book_route'))

        return render_template('private/book-register.html')