const favoriteButton = document.querySelector('.favorite-button')

favoriteButton.addEventListener('click', async (event) => {
    event.preventDefault()

    if(!favoriteButton.classList.contains('add-favorite')){
        return
    }

    Swal.fire({
        title: 'Favoritando livro...',
        didOpen: async () => {
            Swal.showLoading()
        },
        allowOutsideClick: () => !Swal.isLoading(),
        backdrop: 'var(--swal-backdrop)',
        background: 'var(--surface-secondary)'
    })


    const bookId = favoriteButton.dataset.bookId

    const { message, status } = await submitRegisterFavoriteBook(bookId)


    if (status == 201) {
        Swal.fire({
            title: '<h3>Livro favoritado com sucesso!</h3>',
            icon: 'success',
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            },
        }).then(() => {
            window.location.reload()
        })

    } else {

        Swal.fire({
            title: 'Falha ao favoritar livro!',
            html: message,
            icon: 'error',
            iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            },
        })
    }

});

async function submitRegisterFavoriteBook(bookId) {
    try {

        const response = await fetch('/favorite', {
            method: 'POST',
            body: JSON.stringify({ book_id: bookId }),
            headers: {
                'Content-Type': 'application/json'
            }
        })

        return await response.json()

    } catch (error) {
        return {
            status: 500,
            message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.'
          }
    }
}



const deleteFavoriteModal = document.querySelector('#delete-favorite-modal')
const deleteFavoriteModalButton = deleteFavoriteModal.querySelector('#delete-favorite-button')

deleteFavoriteModalButton.addEventListener('click', async (event) => {
    event.preventDefault()

    if(!favoriteButton.classList.contains('delete-favorite')){
        return
    }

    Swal.fire({
        title: 'Desfavoritando livro...',
        didOpen: async () => {
            Swal.showLoading()
            deleteFavoriteModal.style.display = 'none'
        },
        allowOutsideClick: () => !Swal.isLoading(),
        backdrop: 'var(--swal-backdrop)',
        background: 'var(--surface-secondary)'
    })

    const favoriteId = favoriteButton.dataset.favoriteId

    const { message, status } = await submitDeleteFavoriteBook(favoriteId)

    if (status == 200) {
        Swal.fire({
            title: '<h3>Livro desfavoritado com sucesso!</h3>',
            icon: 'success',
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            },
        }).then(() => {
            window.location.reload()
        })

    } else {

        Swal.fire({
            title: 'Falha ao desfavoritar livro!',
            html: message,
            icon: 'error',
            iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            },
        }).then(() => {
            window.location.reload()
        })

    }
})


async function submitDeleteFavoriteBook(favoriteId) {
    try {

        const response = await fetch(`/favorite/${favoriteId}`, {
            method: 'DELETE',
        })

        return await response.json()

    } catch (error) {
        return {
            status: 500,
            message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.'
          }
    }
}








