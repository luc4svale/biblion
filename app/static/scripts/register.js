const registerForm = document.querySelector('#register-form')
const registerFormButton = registerForm.querySelector('#register-button')


registerFormButton.addEventListener('click', async (event)=> {
  event.preventDefault()
  const formData = new FormData(registerForm)

  const response = await fetch('/register', {
    method: 'POST',
    body: formData
  })

  const data = await response.json()
  console.log(data)
})




