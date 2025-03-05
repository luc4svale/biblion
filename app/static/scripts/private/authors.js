const authorsTable = document.querySelector('#authors-table')

const registerAuthorModal = document.querySelector('#register-author-modal')
const registerAuthorModalButton = document.querySelector('#register-author-modal-button')
const registerAuthorForm = registerAuthorModal.querySelector('#register-author-form')
const registerAuthorName = registerAuthorForm.querySelector('#register-author-name')
const registerAuthorFormButton = registerAuthorForm.querySelector('#register-author-form-button')


const editAuthorModal = document.querySelector('#edit-author-modal')
const editAuthorModalOverlay = editAuthorModal.querySelector('#edit-author-overlay')
const editAuthorModalButtons = authorsTable.querySelectorAll(".edit-author-modal-button")
const deleteAuthorSwalButtons = authorsTable.querySelectorAll('.delete-author-swal-button')
const editAuthorForm = editAuthorModal.querySelector('#edit-author-form')
const editAuthorName = editAuthorForm.querySelector('#edit-author-name')
const editAuthorFormButton = editAuthorForm.querySelector('#edit-author-form-button')


const names = [registerAuthorName, editAuthorName]




//------- Names Mask -------//
names.forEach(name => {
  name.addEventListener('input', () => {
    if (name.value.length > 100) {
      name.value = name.value.substring(0, 100)
    }

    const cursorPosition = name.selectionStart

    const pattern = /[^\sa-zA-ZàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ'\.]|^\s+$|^'/g

    if (pattern.test(name.value)) {
      name.value = name.value.replace(pattern, '')
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1)
    }

    if (/\s{2,}/g.test(name.value)) {
      name.value = name.value.replace(/\s{2,}/g, ' ')
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1)
    }

    if (/'{2,}/g.test(name.value)) {
      name.value = name.value.replace(/'{2,}/g, "'")
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1)
    }

    if (/\.{2,}/g.test(name.value)) {
      name.value = name.value.replace(/\.{2,}/g, ".")
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1)
    }
  })
})


//-------- Submit Register Author Form --------//
registerAuthorFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Cadastrando autor...',
    didOpen: async () => {
      Swal.showLoading()
      registerAuthorModal.style.display = 'none'
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)'
  })


  const response = await submitRegisterAuthorForm()

  if (response.status == 201) {

    Swal.fire({
      title: '<h3>Autor cadastrado com sucesso!</h3>',
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
      title: 'Falha ao cadastrar autor!',
      html: response.message,
      icon: 'error',
      iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'swal-icon',
        confirmButton: 'btn-primary'
      },
    }).then(() => {
      registerAuthorModal.style.display = "block"
    })
  }
})


async function submitRegisterAuthorForm() {

  const formData = new FormData(registerAuthorForm)

  try {
    const response = await fetch('/author', {
      method: 'POST',
      body: formData,
    })

    return await response.json()


  } catch (error) {
    return {
      status: 500,
      message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.'
    }

  }
}



//-------- Fill Edit Author Modal on Edit Button Click --------//
editAuthorModalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {

    overlay(editAuthorModalOverlay, true)

    const response = await getAuthorInfo(button.dataset.authorId)

    if (!response.status == 200) {

      await Swal.fire({
        title: '<h3>Autor não encontrado!</h3>',
        icon: 'error',
        iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
        backdrop: 'var(--swal-backdrop)',
        background: 'var(--surface-secondary)',
        customClass: {
          icon: 'swal-icon',
        },
      }).then(() => {
        window.location.reload()
      })

    } else {
      fillEditAuthorForm(response.data)
      overlay(editAuthorModalOverlay, false)
    }


  })
)

async function getAuthorInfo(authorId) {
  try {
    const response = await fetch(`/author/${authorId}`, {
      method: 'GET'

    })

    return await response.json()

  } catch (error) {
    return {
      status: 500,
      message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.',
    }
  }
}


function fillEditAuthorForm(authorData) {
 const { id, name } = authorData

 editAuthorName.value = name
 editAuthorFormButton.dataset.authorId = id
}


function overlay(element, show) {
  if (show) {
    element.style.display = 'flex'
    return
  }

  element.style.display = 'none'
}



//------- Submit Edit Author Form -------//
editAuthorFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Editando autor...',
    didOpen: async () => {
      Swal.showLoading()
      editAuthorModal.style.display = 'none'
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)',
  })

  const response = await submitEditAuthorForm()

  if (response.status == 200) {

    Swal.fire({
      title: '<h3>Autor editado com sucesso!</h3>',
      icon: 'success',
      iconHtml: '<i class="fas fa-check-circle text-success"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'custom-icon-class',
        confirmButton: 'btn-primary'
      },
    }).then(() => {
      $(editAuthorModal).modal('hide')
    })

    const { name, updated_at } = response.data

    const authorsTableRow = authorsTable.querySelector(`#author-row-${editAuthorFormButton.dataset.authorId}`)

    //------- Update Author Table Row Name --------//
    const authorTableRowName = authorsTableRow.querySelector('.author-name')
    authorTableRowName.innerHTML = name
    

    //---- Update Author Table Row Updated At ----//
    const authorTableRowUpdatedAt = authorsTableRow.querySelector('.author-updated-at')
    authorTableRowUpdatedAt.innerHTML = updated_at

  } else {
    Swal.fire({
      title: 'Falha ao editar autor!',
      html: response.message,
      icon: 'error',
      iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'swal-icon',
        confirmButton: 'btn-primary'
      },
    }).then(() => {
      editAuthorModal.style.display = 'block'
    })
  }
})


async function submitEditAuthorForm() {

  try {

    const formData = new FormData(editAuthorForm)

    const response = await fetch(`/author/${editAuthorFormButton.dataset.authorId}`, {
      method: "PUT",
      body: formData,
    })

    return await response.json()

  } catch (error) {
    return {
      status: 500,
      message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.'
    }
  }

}



//-------- Submit Delete Author --------//
deleteAuthorSwalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {
    event.preventDefault()

    setTimeout(() => {
      $(button).blur()
    }, 5)

    Swal.fire({
      text: 'Você tem certeza que deseja excluir esse autor?',
      showCancelButton: true,
      cancelButtonText: 'Cancelar',
      confirmButtonText: 'Confirmar',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        confirmButton: 'btn-primary',
        cancelButton: 'btn-danger'
      },
      didClose: () => {
        setTimeout(() => {
          $(button).blur()
        }, 3)
      }
    }).then(async (result) => {

      if (result.isConfirmed) {

        Swal.fire({
          title: 'Exluindo autor...',
          didOpen: async () => {
            Swal.showLoading();
          },
          allowOutsideClick: () => !Swal.isLoading(),
          backdrop: 'var(--swal-backdrop)',
          background: 'var(--surface-secondary)',
        });

        const response = await submitDeleteAuthor(button.dataset.authorId);

        if (response.status == 200) {

          Swal.fire({
            title: '<h3>Autor excluído com sucesso!</h3>',
            icon: 'success',
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
              icon: 'custom-icon-class',
              confirmButton: 'btn-primary'
            },
          }).then(() => {
            const authorsTableRow = authorsTable.querySelector(`#author-row-${button.dataset.authorId}`)
            authorsTableRow.remove()

            const authorsTableRows = authorsTable.querySelectorAll('.author-row')
            if (authorsTableRows.length == 0) {
              window.location.reload()
            }
          });

        } else {
          Swal.fire({
            title: '<h3>Falha ao excluir autor!</h3>',
            icon: 'error',
            iconHtml: `<i class="fas fa-times-circle text-danger"></i>`,
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
              icon: 'swal-icon',
              confirmButton: 'btn-primary'
            },
          }).then(() => {
            window.location.reload()
          });
        }
      }
    });
  })
);


async function submitDeleteAuthor(authorId) {
  try {
    const response = await fetch(`/author/${authorId}`, {
      method: "DELETE",
    });

    return response.json();

  } catch (error) {
    return {
      status: 500,
      message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.'
    };
  }
} 


$(document).ready(() => {


  //----- Set Authors Datatable Config ------//
  $(authorsTable).DataTable({
    'language': {
        'decimal': '',
        'emptyTable': 'Nenhum dado disponível na tabela',
        'info': '', //'Mostrando _START_ até _END_ de _TOTAL_ registros', 
        'infoEmpty': '', //'Mostrando 0 até 0 de 0 registros', 
        'infoFiltered': '(filtrado de _MAX_ registros totais)',
        'infoPostFix': '',
        'thousands': '.',
        'lengthMenu': 'Mostrar _MENU_ registros por página',
        'loadingRecords': 'Carregando...',
        'processing': 'Processando...',
        'search': 'Pesquisar:',
        'zeroRecords': 'Nenhum registro correspondente foi encontrado',
        'paginate': {
            'first': 'Primeiro',
            'last': 'Último',
            'next': '>',
            'previous': '<'
        },
        'aria': {
            'sortAscending': ': ativar para classificar coluna ascendente',
            'sortDescending': ': ativar para classificar coluna descendente'
        }
    },
    'paging': true,
    'searching': true,
    'info': true,
    'lengthChange': true,
    'columnDefs': [
        { 'orderable': true, 'targets': 0 },
        { 'orderable': true, 'targets': 1 },
        { 'orderable': true, 'targets': 2 },
        { 'orderable': false, 'targets': 3 },
    ],
    'order': [['1', 'desc']]
});

  //--------- Set Buttons Tooltips ---------//
  $(registerAuthorModalButton).tooltip()
  $('.edit-author-modal-button').tooltip()
  $('.delete-author-swal-button').tooltip()


  //---- Register Modal on Hidden ----//
  $(registerAuthorModal).on('hidden.bs.modal', () => {
    $(registerAuthorName).val('')

    setTimeout(() => {
      $(registerAuthorModalButton).blur()
    }, 5)

  })


  //---- Edit Modal on Hidden ----//
  $(editAuthorModal).on('hidden.bs.modal', () => {
    $(editAuthorName).val('')
    $(editAuthorFormButton).data('authorId', '')


    setTimeout(() => {
      $(editAuthorModalButtons).blur()
    }, 5)
  })

})

