ALLOWED_EXTENSIONS = {'pdf', 'epub', 'mobi', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    """Verifica se o arquivo tem uma das extensões permitidas."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS