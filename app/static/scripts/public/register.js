const registerForm = document.querySelector('#register-form')
const firstName = registerForm.querySelector('#first-name')
const lastName = registerForm.querySelector('#last-name')
const names = [firstName, lastName]
const email = registerForm.querySelector('#email')
const password = registerForm.querySelector('#password')
const confirmPassword = registerForm.querySelector('#confirm-password')
const registerFormButton = registerForm.querySelector('#register-button')



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


//-- Passwords Visibility --//
const toggleIcons = document.querySelectorAll('.password-visibility')

toggleIcons.forEach(toggleIcon => {
  toggleIcon.addEventListener('click', () => {
    const passwordField = toggleIcon.parentElement.querySelector('input')
    const isPasswordVisible = passwordField.type === 'text'

    if (isPasswordVisible) {
      passwordField.type = 'password'
      toggleIcon.classList.remove("fa-eye")
      toggleIcon.classList.add('fa-eye-slash')
      toggleIcon.title = 'Mostrar'
    } else {
      passwordField.type = 'text'
      toggleIcon.classList.remove('fa-eye-slash')
      toggleIcon.classList.add('fa-eye')
      toggleIcon.title = 'Ocultar'
    }
    $(toggleIcon).tooltip('dispose').tooltip('show')
  })
})

$(document).ready(() => {
  $('.password-visibility').tooltip('dispose').tooltip()
})

//----- Submit Register Form ------//
registerFormButton.addEventListener('click', async (event) => {
  event.preventDefault()

  Swal.fire({
    title: 'Cadastrando usuário...',
    didOpen: async () => {
      Swal.showLoading()
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)',
  })

  const response = await submitRegisterForm()

  if (response.status === 201) {
    Swal.fire({
      title: '<h3>Usuário cadastrado com sucesso!</h3>',
      icon: 'success',
      iconHtml: '<i class="fas fa-check-circle text-success"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
      customClass: {
        icon: 'swal-icon',
        confirmButton: 'btn-primary'
      }
    }).then(() => {
      window.location.href = '/login'
    })

  } else {
    Swal.fire({
      title: 'Falha ao cadastrar usuário!',
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

async function submitRegisterForm() {
  try {
    const formData = new FormData(registerForm)

    const response = await fetch('/register', {
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















