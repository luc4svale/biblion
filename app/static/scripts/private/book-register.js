const bookRegisterForm = document.querySelector('#book-register-form')
const bookRegisterButton = bookRegisterForm.querySelector('#book-register-button')

bookRegisterButton.addEventListener('click', async (event) => {
  event.preventDefault()
  const formData = new FormData(bookRegisterForm)

  const response = await fetch('/book-register', {
    method: 'POST',
    body: formData
  })

  const data = await response.json()
  console.log(data)
})