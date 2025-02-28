import os
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import flash
from app import db
from app.models.book import Book
from app.utils.allowed_files import allowed_file

# Função para garantir que os diretórios de upload existam
def create_upload_directory(path):
    """Verifica se o diretório existe, se não, cria o diretório"""
    if not os.path.exists(path):
        os.makedirs(path)

def register_book(form_data, book_files):
    # Capturando os dados do formulário
    title = form_data['title']
    synopsis = form_data['synopsis']
    publication_year = form_data['publication_year']
    author_id = form_data['author_id']
    category_id = form_data['category_id']
    publisher_id = form_data['publisher_id']

    # Verificando os arquivos do livro e da capa
    book_file = book_files.get('book_file')
    cover_image = book_files.get('cover_image')

    # Validação dos campos obrigatórios
    if not title or not synopsis or not author_id or not category_id or not publisher_id:
        flash('Todos os campos obrigatórios devem ser preenchidos!', 'error')
        return None

    # Definindo os caminhos dos arquivos
    file_path = None
    if book_file and allowed_file(book_file.filename):
        # Criando o diretório de livros se não existir
        books_dir = os.path.join('uploads', 'books')
        create_upload_directory(books_dir)

        filename = secure_filename(f'{uuid4()}_{book_file.filename}')
        file_path = os.path.join(books_dir, filename)
        book_file.save(file_path)

    cover_image_path = None
    if cover_image and allowed_file(cover_image.filename):
        # Criando o diretório de capas se não existir
        covers_dir = os.path.join('uploads', 'covers')
        create_upload_directory(covers_dir)

        filename = secure_filename(f'{uuid4()}_{cover_image.filename}')
        cover_image_path = os.path.join(covers_dir, filename)
        cover_image.save(cover_image_path)

    # Criando o novo livro
    new_book = Book(
        title=title,
        synopsis=synopsis,
        publication_year=int(publication_year),
        file_path=file_path,
        cover_image_path=cover_image_path,
        author_id=author_id,
        category_id=category_id,
        publisher_id=publisher_id
    )

    try:
        # Salvando o livro no banco de dados
        db.session.add(new_book)
        db.session.commit()
        flash('Livro cadastrado com sucesso!', 'success')
        return new_book
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar livro: {str(e)}', 'error')
        return None
