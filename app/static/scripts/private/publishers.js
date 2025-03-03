const publishersTable = document.querySelector('#publishers-table')

const registerPublisherModal = document.querySelector('#register-publisher-modal')
const registerPublisherModalButton = document.querySelector('#register-publisher-modal-button')
const registerPublisherForm = registerPublisherModal.querySelector('#register-publisher-form')
const registerPublisherName = registerPublisherForm.querySelector('#register-publisher-name')
const registerPublisherFormButton = registerPublisherForm.querySelector('#register-publisher-form-button')


const editPublisherModal = document.querySelector('#edit-publisher-modal')
const editPublisherModalOverlay = editPublisherModal.querySelector('#edit-publisher-overlay')
const editPublisherModalButtons = publishersTable.querySelectorAll(".edit-publisher-modal-button")
const editPublisherForm = editPublisherModal.querySelector('#edit-publisher-form')
const editPublisherName = editPublisherForm.querySelector('#edit-publisher-name')
const editPublisherFormButton = editPublisherForm.querySelector('#edit-publisher-form-button')


const names = [registerPublisherName, editPublisherName]


const deletePublisherSwalButtons = publishersTable.querySelectorAll('.delete-publisher-swal-button')

//------- Names Mask -------//
names.forEach(name => {
  name.addEventListener('input', () => {
    if (name.value.length > 100) {
      name.value = name.value.substring(0, 100)
    }

    const cursorPosition = name.selectionStart

    const pattern = /[^\sa-zA-ZàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ']|^\s+$|^'/g

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
  })
})


//-------- Submit Register Publisher Form --------//
registerPublisherFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Cadastrando editora...',
    didOpen: async () => {
      Swal.showLoading()
      registerPublisherModal.style.display = 'none'
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)'
  })


  const response = await submitRegisterPublisherForm()

  if (response.status == 201) {

    Swal.fire({
      title: '<h3>Editora cadastrada com sucesso!</h3>',
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
      title: 'Falha ao cadastrar editora!',
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
      registerPublisherModal.style.display = "block"
    })
  }
})


async function submitRegisterPublisherForm() {

  const formData = new FormData(registerPublisherForm)

  try {
    const response = await fetch('/publisher', {
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



//-------- Fill Edit Publisher Modal on Edit Button Click --------//
editPublisherModalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {

    overlay(editPublisherModalOverlay, true)

    const response = await getPublisherInfo(button.dataset.publisherId)

    if (!response.status == 200) {

      await Swal.fire({
        title: '<h3>Editora não encontrado!</h3>',
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
      fillEditPublisherForm(response.data)
      overlay(editPublisherModalOverlay, false)
    }


  })
)

async function getPublisherInfo(publisherId) {
  try {
    const response = await fetch(`/publisher/${publisherId}`, {
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


function fillEditPublisherForm(publisherData) {
 const { id, name } = publisherData

 editPublisherName.value = name
 editPublisherFormButton.dataset.publisherId = id
}


function overlay(element, show) {
  if (show) {
    element.style.display = 'flex'
    return
  }

  element.style.display = 'none'
}



//------- Submit Edit Publisher Form -------//
editPublisherFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Editando editora...',
    didOpen: async () => {
      Swal.showLoading()
      editPublisherModal.style.display = 'none'
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)',
  })

  const response = await submitEditPublisherForm()

  if (response.status == 200) {

    Swal.fire({
      title: '<h3>Editora editada com sucesso!</h3>',
      icon: 'success',
      iconHtml: '<i class="fas fa-check-circle text-success"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'custom-icon-class',
        confirmButton: 'btn-primary'
      },
    }).then(() => {
      $(editPublisherModal).modal('hide')
    })

    const { name, updated_at } = response.data

    const publishersTableRow = publishersTable.querySelector(`#publisher-row-${editPublisherFormButton.dataset.publisherId}`)

    //------- Update Publisher Table Row Name --------//
    const publisherTableRowName = publishersTableRow.querySelector('.publisher-name')
    publisherTableRowName.innerHTML = name
    

    //---- Update Publisher Table Row Updated At ----//
    const publisherTableRowUpdatedAt = publishersTableRow.querySelector('.publisher-updated-at')
    publisherTableRowUpdatedAt.innerHTML = updated_at

  } else {
    Swal.fire({
      title: 'Falha ao editar editora!',
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
      editPublisherModal.style.display = 'block'
    })
  }
})


async function submitEditPublisherForm() {

  try {

    const formData = new FormData(editPublisherForm)

    const response = await fetch(`/publisher/${editPublisherFormButton.dataset.publisherId}`, {
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



//-------- Submit Delete Publisher --------//
deletePublisherSwalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {
    event.preventDefault()

    setTimeout(() => {
      $(button).blur()
    }, 5)

    Swal.fire({
      text: 'Você tem certeza que deseja excluir essa editora?',
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
          title: 'Exluindo editora...',
          didOpen: async () => {
            Swal.showLoading();
          },
          allowOutsideClick: () => !Swal.isLoading(),
          backdrop: 'var(--swal-backdrop)',
          background: 'var(--surface-secondary)',
        });

        const response = await submitDeletePublisher(button.dataset.publisherId);

        if (response.status == 200) {

          Swal.fire({
            title: '<h3>Editora excluída com sucesso!</h3>',
            icon: 'success',
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
              icon: 'custom-icon-class',
              confirmButton: 'btn-primary'
            },
          }).then(() => {
            const publishersTableRow = publishersTable.querySelector(`#publisher-row-${button.dataset.publisherId}`);
            publishersTableRow.remove();
          });

        } else {
          Swal.fire({
            title: '<h3>Falha ao excluir editora!</h3>',
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


async function submitDeletePublisher(publisherId) {
  try {
    const response = await fetch(`/publisher/${publisherId}`, {
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

  //--------- Set Buttons Tooltips ---------//
  $(registerPublisherModalButton).tooltip()
  $(".edit-publisher-modal-button").tooltip()
  $(".delete-publisher-swal-button").tooltip()


  //---- Register Modal on Hidden ----//
  $(registerPublisherModal).on("hidden.bs.modal", () => {
    $(registerPublisherName).val("")

    setTimeout(() => {
      $(registerPublisherModalButton).blur()
    }, 5)

  })


  //---- Edit Modal on Hidden ----//
  $(editPublisherModal).on("hidden.bs.modal", () => {
    $(editPublisherName).val("")
    $(editPublisherFormButton).data('publisherId', '')


    setTimeout(() => {
      $(editPublisherModalButtons).blur()
    }, 5)
  })

})

