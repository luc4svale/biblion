from flask import Flask, render_template, request, jsonify
from config import Config

def create_app():
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    @app.route('/')
    def intro():
        return render_template('index.html')

    @app.route('/login',  methods=['GET', 'POST'])
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
        return render_template('book-details.html')

    @app.route('/reading')
    def reading():
        return render_template('reading.html')

    @app.route('/favorites')
    def favorites():
        return render_template('favorites.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')


    return app
