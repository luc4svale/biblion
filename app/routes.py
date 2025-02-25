from flask import render_template, request, jsonify

def init_routes(app):
    """Função para registrar as rotas na aplicação"""

    @app.route('/')
    def intro():
        return render_template('index.html')

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

        return render_template('login.html')

    @app.route('/register')
    def register():
        return render_template('register.html')

    @app.route('/forgot-password')
    def forgot_password():
        return render_template('forgot-password.html')

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/book-details')
    def book_details():
        return render_template('private/book-details.html')

    @app.route('/reading')
    def reading():
        return render_template('reading.html')

    @app.route('/favorites')
    def favorites():
        return render_template('favorites.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')
