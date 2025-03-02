const loginForm = document.querySelector('#login-form')
const email = loginForm.querySelector('#email')
const password = loginForm.querySelector('#password')
const loginFormButton = loginForm.querySelector('#login-button')


//------ Email Mask ------//
email.addEventListener('input', () => {
  if (email.value.length > 120) {
    email.value = email.value.substring(0, 120)
  }

  const cursorPosition = email.selectionStart

  const pattern = /[^a-zA-Z0-9@_.-]/g

  if (pattern.test(email.value)) {
    email.value = email.value.replace(pattern, '')
    email.setSelectionRange(cursorPosition - 1, cursorPosition - 1)
    return
  }
  email.setSelectionRange(cursorPosition, cursorPosition)
})


//-- Password Visibility --//
const toggleIcon = document.querySelector('.password-visibility')

toggleIcon.addEventListener('click', () => {
  const isPasswordVisible = password.type === 'text'

  if (isPasswordVisible) {
    password.type = 'password'
    toggleIcon.classList.remove("fa-eye")
    toggleIcon.classList.add('fa-eye-slash')
    toggleIcon.title = 'Mostrar'
  } else {
    password.type = 'text'
    toggleIcon.classList.remove('fa-eye-slash')
    toggleIcon.classList.add('fa-eye')
    toggleIcon.title = 'Ocultar'
  }
  $(toggleIcon).tooltip('dispose').tooltip('show')
})

$(document).ready(() => {
  $('.password-visibility').tooltip('dispose').tooltip()
})


//----- Submit Login Form ------//
loginFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Autenticando...',
    didOpen: async () => {
      Swal.showLoading()
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)',
  })

  const response = await submitLoginForm()

  if (response.status == 200) {
      window.location.href = "/home"

  } else {
    Swal.fire({
      title: 'Falha ao autenticar!',
      html: response.message,
      icon: 'error',
      iconHtml: `<i class="fas fa-times-circle text-danger"></i>`,
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'swal-icon',
        confirmButton: 'btn-primary'
      },
    })
  }
})

async function submitLoginForm() {
  try {
    const formData = new FormData(loginForm)

    const response = await fetch('/login', {
      method: 'POST',
      body: formData,
    })

    return await response.json()


  } catch (error) {
    return {
      status: 503,
      message: 'Erro na conexão. Tente novamente mais tarde.'
    }
  }
}















