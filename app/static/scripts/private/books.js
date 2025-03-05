const booksTable = document.querySelector('#books-table')

const registerBookModal = document.querySelector('#register-book-modal')
const registerBookModalButton = document.querySelector('#register-book-modal-button')
const registerBookForm = registerBookModal.querySelector('#register-book-form')
const registerBookCoverContainer = registerBookForm.querySelector('#register-book-cover-container')
const registerBookCoverOverlay = registerBookCoverContainer.querySelector('#register-book-cover-overlay')
const registerBookCoverPreview = registerBookCoverContainer.querySelector('#register-book-cover-preview')
const registerBookCoverInput = registerBookCoverContainer.querySelector('#register-book-cover')
const registerBookTitle = registerBookForm.querySelector('#register-book-title')
const registerBookAuthor = registerBookForm.querySelector('#register-book-author')
const registerBookPublisher = registerBookForm.querySelector('#register-book-publisher')
const registerBookCategory = registerBookForm.querySelector('#register-book-category')
const registerBookPublicationYear = registerBookForm.querySelector('#register-book-publication-year')
const registerBookSynopsis = registerBookForm.querySelector('#register-book-synopsis')
const registerBookFile = registerBookForm.querySelector('#register-book-file')
const registerBookFormButton = registerBookForm.querySelector('#register-book-form-button')


const editBookModal = document.querySelector('#edit-book-modal')
const editBookModalOverlay = editBookModal.querySelector('#edit-book-overlay')
const editBookModalButtons = booksTable.querySelectorAll(".edit-book-modal-button")
const deleteBookSwalButtons = booksTable.querySelectorAll('.delete-book-swal-button')
const editBookForm = editBookModal.querySelector('#edit-book-form')
const editBookCoverContainer = editBookForm.querySelector('#edit-book-cover-container')
const editBookCoverOverlay = editBookCoverContainer.querySelector('#edit-book-cover-overlay')
const editBookCoverPreview = editBookCoverContainer.querySelector('#edit-book-cover-preview')
const editBookCoverInput = editBookCoverContainer.querySelector('#edit-book-cover')
const editBookTitle = editBookForm.querySelector('#edit-book-title')
const editBookAuthor = editBookForm.querySelector('#edit-book-author')
const editBookPublisher = editBookForm.querySelector('#edit-book-publisher')
const editBookCategory = editBookForm.querySelector('#edit-book-category')
const editBookPublicationYear = editBookForm.querySelector('#edit-book-publication-year')
const editBookSynopsis = editBookForm.querySelector('#edit-book-synopsis')
const editBookFile = editBookForm.querySelector('#edit-book-file')
const editBookFilePreview = editBookFile.parentElement.querySelector('a')
const editBookFormButton = editBookForm.querySelector('#edit-book-form-button')

const authorsSelects = [registerBookAuthor, editBookAuthor]
const publishersSelects = [registerBookPublisher, editBookPublisher]
const categoriesSelects = [registerBookCategory, editBookCategory]



//------------ Cover Mask ------------//
var registerLastCoverFile
var editLastCoverFile

//----- Register Cover Mask ------//
handleCoverChange(registerLastCoverFile, registerBookCoverInput, registerBookCoverPreview)

//------- Edit Cover Mask -------//
handleCoverChange(editLastCoverFile, editBookCoverInput, editBookCoverPreview)


function handleCoverChange(lastCoverFile, coverInput, coverPreview) {

  coverInput.addEventListener('change', async (event) => {

    const file = event.target.files[0]

    if (file) {


      let validCoverObject = await validateCover(coverInput)


      if (validCoverObject.status != 200) {

        coverInput.value = ''

        Swal.fire({
          title: '<h3>Ocorreu um problema!</h3>',
          html: validCoverObject.message,
          icon: 'error',
          iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
          backdrop: 'var(--swal-backdrop)',
          background: 'var(--surface-secondary)',
          customClass: {
            icon: 'swal-icon',
            confirmButton: 'btn-primary'
          }
        })

      } else {

        lastCoverFile = file

        const reader = new FileReader()

        reader.onload = function (event) {
          const photoUrl = event.target.result
          coverPreview.src = photoUrl
        }

        reader.readAsDataURL(file)
      }

    } else {

      if (lastCoverFile) {
        const fileList = new DataTransfer()
        fileList.items.add(new File([lastCoverFile], lastCoverFile.name))
        coverInput.files = fileList.files
      }
    }

  })
}

async function validateCover(input) {
  let file = input.files[0]

  if (file.size > (1024 * 1024 * 5)) {
    return {
      status: 400,
      message: 'Tamanho máximo de 5MB excedido para <strong>imagem de capa do livro</strong>.'
    }
  }


  try {

    const arrayBuffer = await readFileAsArrayBuffer(file)

    const text = await readFileAsText(file)
    const svgPattern = /<svg[^>]*xmlns="http:\/\/www\.w3\.org\/2000\/svg"[^>]*>/
    const isSVG = svgPattern.test(text)

    const isValidFormat = (isValidCoverExtension(arrayBuffer) || isSVG)


    if (!isValidFormat) {
      return {
        status: 400,
        message: 'Tipo de arquivo inválido para <strong>imagem de capa do livro</strong>.'
      }
    }


    return {
      status: 200,
      message: 'Imagem de capa do livro válida.'
    }


  } catch (error) {
    return {
      status: 404,
      message: 'Erro ao carregar <strong>imagem de capa do livro</strong>. Tente novamente.'
    }
  }
}

function readFileAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onload = function (event) {
      resolve(new Uint8Array(event.target.result))
    }

    reader.onerror = function (event) {
      reject(event)
    }

    reader.readAsArrayBuffer(file)
  })
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onload = function (event) {
      resolve(event.target.result)
    }

    reader.onerror = function (event) {
      reject(event)
    }

    reader.readAsText(file)
  })

}

function isValidCoverExtension(arrayBuffer) {
  let fileCodes = ['89504e47', 'ffd8ffdb', 'ffd8ffe0', 'ffd8ffee', 'ffd8ffe1', '0000000c', 'ff4fff51', '52494646']

  var arr = arrayBuffer.subarray(0, 4)
  var header = ''
  for (var i = 0; i < arr.length; i++) {
    header += arr[i].toString(16)
  }

  if (!fileCodes.includes(header)) {
    return false
  }
  return true
}


//------- Mask for Titles and Synopsis -------//
function alphanumericSymbolMask(input) {
  const cursorPosition = input.selectionStart;
  const alphaSymbolRegex = /[^\sa-zA-Z0-9.,-/ªº°àáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ']|^\s+$|^'+|^\.+|^,+|^-+|^\/+|^ª+|^º+|^°+/g;
  if (alphaSymbolRegex.test(input.value)) {
    input.value = input.value.replace(alphaSymbolRegex, '');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/\s{2,}/g.test(input.value)) {
    input.value = input.value.replace(/\s{2,}/g, ' ');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/'{4,}/g.test(input.value)) {
    input.value = input.value.replace(/'{2,}/g, "'''");
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/\.{2,}/g.test(input.value)) {
    input.value = input.value.replace(/\.{2,}/g, '.');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/,{2,}/g.test(input.value)) {
    input.value = input.value.replace(/,{2,}/g, ',');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/-{2,}/g.test(input.value)) {
    input.value = input.value.replace(/-{2,}/g, '-');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/\/{2,}/g.test(input.value)) {
    input.value = input.value.replace(/\/{2,}/g, '/');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/ª{2,}/g.test(input.value)) {
    input.value = input.value.replace(/ª{2,}/g, 'ª');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/º{2,}/g.test(input.value)) {
    input.value = input.value.replace(/º{2,}/g, 'º');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }

  if (/°{2,}/g.test(input.value)) {
    input.value = input.value.replace(/°{2,}/g, '°');
    input.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
  }
}

//------- Set Titles Mask --------//
const titles = [registerBookTitle, editBookTitle]
titles.forEach((title) => {
  title.addEventListener('input', () => {
    if (title.value.length > 200) {
      title.value = title.value.substring(0, 200)
    }

    alphanumericSymbolMask(title)
  })

})

//------ Set Synopsis Mask ------//
const theSynopsis = [registerBookSynopsis, editBookSynopsis]
theSynopsis.forEach((synopsis) => {
  synopsis.addEventListener('input', () => {
    if (synopsis.value.length > 600) {
      synopsis.value = synopsis.value.substring(0, 600)
    }

    alphanumericSymbolMask(synopsis)
  })

})



//-------  Mask for Book Files -------//

//------ Register File Mask --------//
handleBookFileChange(registerBookFile)

//-------- Edit File Mask ---------//
handleBookFileChange(editBookFile)


function handleBookFileChange(bookFile) {
  bookFile.addEventListener('change', async (event) => {

    const isEditBookFile = bookFile.id == 'edit-book-file'
    const editBookFilePreviewFilename = new URL(editBookFilePreview).pathname.split('/').pop()

    const dropzone = bookFile.parentElement
    const fileLegend = dropzone.querySelector('span')

    const file = event.target.files[0]

    if (file) {

      let validBookFileObject = await validateBookFile(bookFile)

      if (validBookFileObject.status != 200) {

        bookFile.value = ''
        fileLegend.innerHtml = isEditBookFile ?
          editBookFilePreviewFilename :
          'Clique para escolher um arquivo'

        if (isEditBookFile) {
          editBookFilePreview.style.display = 'block'
        }


        Swal.fire({
          title: '<h3>Ocorreu um problema!</h3>',
          html: validBookFileObject.message,
          icon: 'error',
          iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
          backdrop: 'var(--swal-backdrop)',
          background: 'var(--surface-secondary)',
          customClass: {
            icon: 'swal-icon',
            confirmButton: 'btn-primary'
          }
        })

      } else {
        fileLegend.innerHTML = file.name.replace(/[\s\/\\'"*?:><]/g, '')
        if (isEditBookFile) {
          editBookFilePreview.style.display = 'none'
        }
      }

    } else {
      fileLegend.innerHTML = isEditBookFile ?
        editBookFilePreviewFilename :
        'Clique para escolher um arquivo'

      if (isEditBookFile) {
        editBookFilePreview.style.display = 'block'
      }
    }

  })
}

async function validateBookFile(bookFile) {
  let file = bookFile.files[0]

  if (file.size > 1024 * 1024 * 20) {
    return {
      status: 400,
      message: 'Tamanho máximo de 20MB excedido para <strong>arquivo de conteúdo do livro</strong>.'
    }
  }


  try {

    const arrayBuffer = await readFileAsArrayBuffer(file)

    if (!hasBookFilePdfExtension(arrayBuffer)) {

      return {
        status: 400,
        message: 'Tipo de arquivo inválido para <strong>arquivo de conteúdo do livro</strong>.'
      }
    }


    return {
      status: 200,
      message: 'Arquivo de conteúdo do livro válido.'
    }


  } catch (error) {
    return {
      status: 404,
      message: 'Erro ao carregar <strong>arquivo de conteúdo do livro</strong>. Tente novamente.'
    }
  }


}

function hasBookFilePdfExtension(arrayBuffer) {
  let pdfCode = '25504446'

  var arr = arrayBuffer.subarray(0, 4)
  var header = ''
  for (var i = 0; i < arr.length; i++) {
    header += arr[i].toString(16)
  }

  if (pdfCode != header) {
    return false
  }
  return true
}


//-------- Fill Selects Forms --------//
async function fetchSelectsData(url, dataKey) {
  try {
    let response = await fetch(url, { method: 'GET' });
    let jsonResponse = await response.json();

    if (jsonResponse.status == 200) {
      return jsonResponse.data[dataKey];
    }

    return []

  } catch (error) {
    return []
    //console.error(`Erro ao buscar ${dataKey}:`, error);
  }
}

function populateSelects(selectElements, items) {
  selectElements.forEach(element => {
    if (element) {
      items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.name;
        element.appendChild(option);
      });
    }
  });
}

//---------- Fill Authors Selects ----------//
fetchSelectsData('/api/author', 'authors').then(authors => {
  populateSelects(authorsSelects, authors);
});

//-------- Fill Publishers Selects ---------//
fetchSelectsData('/api/publisher', 'publishers').then(publishers => {
  populateSelects(publishersSelects, publishers);
});

//-------- Fill Categories Selects ---------//
fetchSelectsData('/api/category', 'categories').then(categories => {
  populateSelects(categoriesSelects, categories);
});



//-------- Submit Register Book Form --------//
registerBookFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Cadastrando livro...',
    didOpen: async () => {
      Swal.showLoading()
      registerBookModal.style.display = 'none'
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)'
  })


  const response = await submitRegisterBookForm()

  if (response.status == 201) {

    Swal.fire({
      title: '<h3>Livro cadastrado com sucesso!</h3>',
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
      title: 'Falha ao cadastrar livro!',
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
      registerBookModal.style.display = "block"
    })
  }
})

async function submitRegisterBookForm() {

  const formData = new FormData(registerBookForm)

  try {
    const response = await fetch('/book', {
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



//-------- Fill Edit Book Modal on Edit Button Click --------//
editBookModalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {

    overlay(editBookModalOverlay, true)

    const response = await getBookInfo(button.dataset.bookId)

    if (!response.status == 200) {

      await Swal.fire({
        title: '<h3>Livro não encontrado!</h3>',
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
      console.log(response.data)
      fillEditBookForm(response.data)
      overlay(editBookModalOverlay, false)
    }


  })
)

async function getBookInfo(bookId) {
  try {
    const response = await fetch(`/book/${bookId}`, {
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


function fillEditBookForm(bookData) {
  const { id, title, synopsis, publication_year, file, cover, author, category, publisher } = bookData

  editBookCoverPreview.src = `/uploads/covers/${cover}`
  editBookTitle.value = title
  editBookAuthor.value = author.id
  editBookPublisher.value = publisher.id
  editBookCategory.value = category.id
  editBookPublicationYear.value = publication_year
  editBookSynopsis.value = synopsis

  const dropzone = editBookFile.parentElement

  const editBookFileLegend = dropzone.querySelector('span')
  const editBookFilePreview = dropzone.querySelector('a')
  editBookFileLegend.innerHTML = file
  editBookFilePreview.href = `/uploads/books/${file}`
  editBookFilePreview.style.display = 'block'


  editBookFormButton.dataset.bookId = id
}


function overlay(element, show) {
  if (show) {
    element.style.display = 'flex'
    return
  }

  element.style.display = 'none'
}



//------- Submit Edit Book Form -------//
editBookFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Editando livro...',
    didOpen: async () => {
      Swal.showLoading()
      editBookModal.style.display = 'none'
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)',
  })

  const response = await submitEditBookForm()

  if (response.status == 200) {

    Swal.fire({
      title: '<h3>Livro editado com sucesso!</h3>',
      icon: 'success',
      iconHtml: '<i class="fas fa-check-circle text-success"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'custom-icon-class',
        confirmButton: 'btn-primary'
      },
    }).then(() => {
      $(editBookModal).modal('hide')
    })

    const { cover, title, author, publisher, category } = response.data

    const booksTableRow = booksTable.querySelector(`#book-row-${editBookFormButton.dataset.bookId}`)


    //------- Update Book Table Row Title --------//
    const bookTableRowCover = booksTableRow.querySelector('.book-cover img')
  
    bookTableRowCover.src = `/uploads/covers/${cover}`

    //------- Update Book Table Row Title --------//
    const bookTableRowTitle = booksTableRow.querySelector('.book-title')
    bookTableRowTitle.innerHTML = title

    //---- Update Book Table Row Author ----//
    const bookTableRowAuthor = booksTableRow.querySelector('.book-author')
    bookTableRowAuthor.innerHTML = author.name

    //---- Update Book Table Row Publisher ----//
    const bookTableRowPublisher = booksTableRow.querySelector('.book-publisher')
    bookTableRowPublisher.innerHTML = publisher.name

    //---- Update Book Table Row Category ----//
    const bookTableRowCategory = booksTableRow.querySelector('.book-category')
    bookTableRowCategory.innerHTML = category.name



  } else {
    Swal.fire({
      title: 'Falha ao editar livro!',
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
      editBookModal.style.display = 'block'
    })
  }
})


async function submitEditBookForm() {

  try {

    const formData = new FormData(editBookForm)

    const response = await fetch(`/book/${editBookFormButton.dataset.bookId}`, {
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


//-------- Submit Delete Book --------//
deleteBookSwalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {
    event.preventDefault()

    setTimeout(() => {
      $(button).blur()
    }, 5)

    Swal.fire({
      text: 'Você tem certeza que deseja excluir esse livro?',
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
          title: 'Exluindo livro...',
          didOpen: async () => {
            Swal.showLoading();
          },
          allowOutsideClick: () => !Swal.isLoading(),
          backdrop: 'var(--swal-backdrop)',
          background: 'var(--surface-secondary)',
        });

        const response = await submitDeleteBook(button.dataset.bookId);

        if (response.status == 200) {

          Swal.fire({
            title: '<h3>Livro excluído com sucesso!</h3>',
            icon: 'success',
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
              icon: 'custom-icon-class',
              confirmButton: 'btn-primary'
            },
          }).then(() => {
            const booksTableRow = booksTable.querySelector(`#book-row-${button.dataset.bookId}`)
            booksTableRow.remove()

            const booksTableRows = booksTable.querySelectorAll('.book-row')
            if (booksTableRows.length == 0) {
              window.location.reload()
            }
          });

        } else {
          Swal.fire({
            title: '<h3>Falha ao excluir livro!</h3>',
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


async function submitDeleteBook(bookId) {
  try {
    const response = await fetch(`/book/${bookId}`, {
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

  //----- Set Books Datatable Config ------//
  $(booksTable).DataTable({
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
      { 'orderable': false, 'targets': 0 },
      { 'orderable': true, 'targets': 1 },
      { 'orderable': true, 'targets': 2 },
      { 'orderable': true, 'targets': 3 },
      { 'orderable': true, 'targets': 4 },
      { 'orderable': false, 'targets': 5 },
    ],
    'order': []
  })

  //--------- Set Buttons Tooltips ---------//
  $(registerBookModalButton).tooltip()
  $('.edit-book-modal-button').tooltip()
  $('.delete-book-swal-button').tooltip()
  $('#edit-book-file-preview').tooltip()


  //---- Register Modal on Hidden ----//
  $(registerBookModal).on('hidden.bs.modal', () => {
    const registerUploadLegend = registerBookFile.parentElement.querySelector('.upload-legend')
    $(registerBookCoverPreview).attr('src', '/uploads/covers/default-cover.jpg');
    $(registerBookTitle).val('')
    $(registerBookAuthor).val('')
    $(registerBookPublisher).val('')
    $(registerBookCategory).val('')
    $(registerBookPublicationYear).val('')
    $(registerBookSynopsis).val('')
    $(registerBookCoverInput).val('')
    $(registerBookFile).val('')
    $(registerUploadLegend).text('Clique para escolher um arquivo')


    setTimeout(() => {
      $(registerBookModalButton).blur()
    }, 5)

  })


  //---- Edit Modal on Hidden ----//
  $(editBookModal).on('hidden.bs.modal', () => {
    const editUploadLegend = editBookFile.parentElement.querySelector('.upload-legend')
    $(editBookCoverPreview).attr('src', '/uploads/covers/default-cover.jpg');
    $(editBookTitle).val('')
    $(editBookAuthor).val('')
    $(editBookPublisher).val('')
    $(editBookCategory).val('')
    $(editBookPublicationYear).val('')
    $(editBookSynopsis).val('')
    $(editBookCoverInput).val('')
    $(editBookFile).val('')
    $(editUploadLegend).text('Clique para escolher um arquivo') 

    $(editBookFormButton).data('bookId', '')

    setTimeout(() => {
      $(editBookModalButtons).blur()
    }, 5)
  })

})



