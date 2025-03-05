const deleteFavoriteButtons = document.querySelectorAll('.delete-favorite')
const deleteFavoriteModal = document.querySelector('#delete-favorite-modal')
const deleteFavoriteModalButton = deleteFavoriteModal.querySelector('#delete-favorite-button')


deleteFavoriteButtons.forEach((deleteFavoriteButton) => {
    deleteFavoriteButton.addEventListener('click', async (event) => {
        const favoriteId = deleteFavoriteButton.dataset.favoriteId

        deleteFavoriteModalButton.dataset.favoriteId = favoriteId

    })

})

deleteFavoriteModalButton.addEventListener('click', async (event) => {
    event.preventDefault()

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

    const favoriteId = deleteFavoriteModalButton.dataset.favoriteId

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


$(document).ready(() => {

    //---- Delete Favorite Modal on Hidden ----//
    $(deleteFavoriteModal).on('hidden.bs.modal', () => {
        $(deleteFavoriteModalButton).data('favoriteId', '')

    })

})