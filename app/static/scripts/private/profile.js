const changePersonalInfoForm = document.querySelector('#change-personal-info-form')
const photoContainer = changePersonalInfoForm.querySelector('#photo-container')
const photoOverlay = changePersonalInfoForm.querySelector('#photo-overlay')
const photoPreview = changePersonalInfoForm.querySelector('#photo-preview')
const photoInput = changePersonalInfoForm.querySelector('#photo')
const firstName = changePersonalInfoForm.querySelector('#first-name')
const lastName = changePersonalInfoForm.querySelector('#last-name')
const names = [firstName, lastName]
const email = changePersonalInfoForm.querySelector('#email')
const changePersonalInfoFormButton = changePersonalInfoForm.querySelector('#change-personal-info-button')


const changePasswordForm = document.querySelector('#change-password-form')
const currentPassword = changePasswordForm.querySelector("#current-password");
const newPassword = changePasswordForm.querySelector("#new-password");
const confirmNewPassword = changePasswordForm.querySelector("#confirm-new-password");
const toggleIcons = changePasswordForm.querySelectorAll('.password-visibility')
const changePasswordFormButton = changePasswordForm.querySelector('#change-password-button')



//------- Photo Mask/Validation ------//
var lastPhotoFile;

photoInput.addEventListener('change', async (event) => {

    const file = event.target.files[0];

    if (file) {

        let validPhotoNewsObject = await validatePhoto(photoInput);

        if (!validPhotoNewsObject.status == 200) {

            photoInput.value = "";

            Swal.fire({
                title: '<h3>Ocorreu um problema!</h3>',
                html: validPhotoNewsObject.message,
                icon: 'error',
                iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
                backdrop: 'var(--swal-backdrop)',
                background: 'var(--surface-secondary)',
                customClass: {
                    icon: 'swal-icon',
                    confirmButton: 'btn-primary'
                }
            });

        } else {

            lastPhotoFile = file;

            const reader = new FileReader();

            reader.onload = function (event) {
                const photoUrl = event.target.result;
                photoPreview.src = photoUrl;
            };

            reader.readAsDataURL(file);
        }

    } else {

        if (lastPhotoFile) {
            const fileList = new DataTransfer();
            fileList.items.add(new File([lastPhotoFile], lastPhotoFile.name));
            photoInput.files = fileList.files;
        }
    }
});


async function validatePhoto(input) {
    let file = input.files[0];

    if (file.size > 5000000) {
        return {
            status: 400,
            message: "Tamanho máximo de 5MB excedido para <strong>imagem de perfil</strong>."
        };
    }


    try {

        const arrayBuffer = await readFileAsArrayBuffer(file);

        const text = await readFileAsText(file);
        const svgPattern = /<svg[^>]*xmlns="http:\/\/www\.w3\.org\/2000\/svg"[^>]*>/;
        const isSVG = svgPattern.test(text);

        const isValidFormat = (isValidPhotoExtension(arrayBuffer) || isSVG);


        if (!isValidFormat) {
            return {
                status: 400,
                message: "Tipo de arquivo inválido para <strong>imagem de perfil</strong>."
            };
        }


        return {
            status: 200,
            message: "Imagem de perfil válida."
        };


    } catch (error) {
        return {
            status: 404,
            message: "Erro ao carregar <strong>imagem de perfil</strong>. Tente novamente."
        };
    }
}


function readFileAsArrayBuffer(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function (event) {
            resolve(new Uint8Array(event.target.result));
        };

        reader.onerror = function (event) {
            reject(event);
        };

        reader.readAsArrayBuffer(file);
    });
}


function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function (event) {
            resolve(event.target.result);
        };

        reader.onerror = function (event) {
            reject(event);
        };

        reader.readAsText(file);
    });

}


function isValidPhotoExtension(arrayBuffer) {
    let fileCodes = ["89504e47", "ffd8ffdb", "ffd8ffe0", "ffd8ffee", "ffd8ffe1", "0000000c", "ff4fff51", "52494646"];

    var arr = arrayBuffer.subarray(0, 4);
    var header = "";
    for (var i = 0; i < arr.length; i++) {
        header += arr[i].toString(16);
    }

    if (!fileCodes.includes(header)) {
        return false;
    }
    return true;
}



//------- Names Mask -------//
names.forEach(name => {
  name.addEventListener('input', () => {
    if (name.value.length > 100) {
      name.value = name.value.substring(0, 100);
    }

    const cursorPosition = name.selectionStart;

    const pattern = /[^\sa-zA-ZàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ']|^\s+$|^'/g;

    if (pattern.test(name.value)) {
      name.value = name.value.replace(pattern, '');
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
    }

    if (/\s{2,}/g.test(name.value)) {
      name.value = name.value.replace(/\s{2,}/g, ' ');
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
    }

    if (/'{2,}/g.test(name.value)) {
      name.value = name.value.replace(/'{2,}/g, "'");
      name.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
    }
  });
});



//------ Email Mask ------//
email.addEventListener('input', () => {
  if (email.value.length > 120) {
    email.value = email.value.substring(0, 120);
  }

  const cursorPosition = email.selectionStart;

  const pattern = /[^a-zA-Z0-9@_.-]/g;

  if (pattern.test(email.value)) {
    email.value = email.value.replace(pattern, '');
    email.setSelectionRange(cursorPosition - 1, cursorPosition - 1);
    return;
  }
  email.setSelectionRange(cursorPosition, cursorPosition);
});


//------ Submit Change Personal Info Form -------//
changePersonalInfoFormButton.addEventListener("click", async (event) => {
    event.preventDefault();
    Swal.fire({
        title: 'Alterando informações...',
        didOpen: async () => {
            Swal.showLoading();
        },
        allowOutsideClick: () => !Swal.isLoading(),
        backdrop: 'var(--swal-backdrop)',
        background: 'var(--surface-secondary)',
    });

    const response = await SubmitChangePersonalInfoForm();

    if (response.status == 200) {

        Swal.fire({
            title: '<h3>Alterações efetuadas com sucesso!</h3>',
            text: response.keep_logged ?
               '' :
               'Para continuar, por favor, faça login novamente utilizando suas novas credenciais.',
            icon:'success',
            iconHtml: "<i class='fas fa-check-circle text-success'></i>",
            backdrop:'var(--swal-backdrop))',
            background:'var(--surface-secondary)',
            customClass: {
                icon:'swal-icon',
                confirmButton:'btn-primary'
            }
        }).then(() => {
            window.location.href = response.keep_logged ? "/profile" : "/logout";
        });

    } else {
        Swal.fire({
            title: '<h3>Falha ao alterar informações!</h3>',
            html: response.message,
            icon: 'error',
            iconHtml: "<i class='fas fa-times-circle text-danger'></i>",
            backdrop:'var(--swal-backdrop))',
            background:'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            }
        });
    }
});

async function SubmitChangePersonalInfoForm() {
    if (photoInput.files.length != 0) {

        const validPhotoProfileObject = await validatePhoto(photoInput);

        if (!validPhotoProfileObject.status == 200) {
            return await new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve(
                        validPhotoProfileObject
                    );
                });
            });
        }
    }


    const formData = new FormData(changePersonalInfoForm);

    try {


        const response = await fetch(`/profile`, {
            method: "PUT",
            body: formData,
        });

        return await response.json();


    } catch (error) {
        return {
            status: 503,
            message: "Erro na conexão. Por favor, recarregue a página e tente novamente."
        };
    }
}



//------ Passwords Visibility -------//
toggleIcons.forEach(toggleIcon => {
    toggleIcon.addEventListener('click', () => {
      const passwordField = toggleIcon.parentElement.querySelector('input')
      const isPasswordVisible = passwordField.type === 'text';
  
      if (isPasswordVisible) {
        passwordField.type = 'password';
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add('fa-eye-slash');
        toggleIcon.title = 'Mostrar';
      } else {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
        toggleIcon.title = 'Ocultar';
      }
      $(toggleIcon).tooltip('dispose').tooltip('show');
    })
  })
  
  $(document).ready(() => {
    $('.password-visibility').tooltip('dispose').tooltip();
  });
  


//-------- Submit Change Password Form --------//
changePasswordFormButton.addEventListener("click", async (event) => {
    event.preventDefault();
    Swal.fire({
        title: 'Alterando senha...',
        didOpen: async () => {
            Swal.showLoading();
        },
        allowOutsideClick: () => !Swal.isLoading(),
        backdrop: 'var(--swal-backdrop)',
        background: 'var(--surface-secondary)',
    });

    const response = await submitChangePasswordForm();

    if (response.status == 200) {
        Swal.fire({
            title: '<h3>Senha alterada com sucesso!</h3>',
            text: 'Para continuar, por favor, faça login novamente utilizando sua nova senha.',
            icon: 'success',
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            }
        }).then(() => {
            window.location.href = '/logout'
        });
    } else {
        Swal.fire({
            title: '<h3>Falha ao alterar senha!</h3>',
            html: response.message,
            icon: 'error',
            iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
            backdrop: 'var(--swal-backdrop)',
            background: 'var(--surface-secondary)',
            customClass: {
                icon: 'swal-icon',
                confirmButton: 'btn-primary'
            }
        });
    }
});



async function submitChangePasswordForm() {
    if (currentPassword.value == "") {
        return await new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({
                    status: 400,
                    message: "Informe a sua senha atual"
                });
            })
        })
    }


    if (newPassword.value == "") {
        return await new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({
                    status: 400,
                    message: "Informe a nova senha"
                });
            })
        })
    }

    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\.])[A-Za-z\d@$!%*?&\.]{8,}$/
    if(!passwordPattern.test(newPassword.value)) {
        return await new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({
                    status: 400,
                    message: "A nova senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial (@$!%*?&.)"
                });
            })
        })
    }



    if (currentPassword.value == newPassword.value) {
        return await new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({
                    status: 400,
                    message: "A senha atual e a nova senha não devem coincidir"
                });
            })
        })
    }




    if (newPassword.value != confirmNewPassword.value) {
        return await new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({
                    status: 400,
                    message: "Verifique a confirmação de nova senha. Senhas não coincidem"
                });
            })
        })
    }



    try {

        const formData = new FormData(changePasswordForm);

        const response = await fetch("/profile", {
            method: "PATCH",
            body: formData
        });

        return await response.json();

    } catch (error) {
        return {
            status: 503,
            message:  "Erro na conexão. Por favor, recarregue a página e tente novamente."
        };
    }
}


