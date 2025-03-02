const categoriesTable = document.querySelector('#categories-table')

const registerCategoryModal = document.querySelector('#register-category-modal')
const registerCategoryModalButton = document.querySelector('#register-category-modal-button')
const registerCategoryForm = registerCategoryModal.querySelector('#register-category-form')
const registerCategoryName = registerCategoryForm.querySelector('#register-category-name')
const registerCategoryFormButton = registerCategoryForm.querySelector('#register-category-form-button')


const editCategoryModal = document.querySelector('#edit-category-modal')
const editCategoryModalOverlay = editCategoryModal.querySelector('#edit-category-overlay')
const editCategoryModalButtons = categoriesTable.querySelectorAll(".edit-category-modal-button")
const editCategoryForm = editCategoryModal.querySelector('#edit-category-form')
const editCategoryName = editCategoryForm.querySelector('#edit-category-name')
const editCategoryFormButton = editCategoryForm.querySelector('#edit-category-form-button')


const names = [registerCategoryName, editCategoryName]


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


//-------- Submit Register Category Form --------//
registerCategoryFormButton.addEventListener('click', async (event) => {
  event.preventDefault();

  Swal.fire({
    title: 'Cadastrando categoria...',
    didOpen: async () => {
      Swal.showLoading();
      registerCategoryModal.style.display = 'none';
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: 'var(--swal-backdrop)',
    background: 'var(--surface-secondary)'
  });


  const response = await submitRegisterCategoryForm();

  if (response.status == 201) {

    Swal.fire({
      title: '<h3>Categoria cadastrada com sucesso!</h3>',
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
    });

  } else {
    Swal.fire({
      title: 'Falha ao cadastrar categoria!',
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
      registerCategoryModal.style.display = "block";
    });
  }
});


async function submitRegisterCategoryForm() {

  const formData = new FormData(registerCategoryForm);

  try {
    const response = await fetch('/category', {
      method: 'POST',
      body: formData,
    });

    return await response.json();


  } catch (error) {
    return {
      status: 500,
      message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.'
    };

  }
}



//-------- Fill Edit Category Modal on Edit Button Click --------//
editCategoryModalButtons.forEach((button) =>
  button.addEventListener('click', async (event) => {

    overlay(editCategoryModalOverlay, true);

    console.log(button.dataset.categoryId)

    const response = await getCategoryInfo(button.dataset.categoryId);

    if (!response.status == 200) {

      await Swal.fire({
        title: '<h3>Egresso não encontrado!</h3>',
        icon: 'error',
        iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
      backdrop: 'var(--swal-backdrop)',
      background: 'var(--surface-secondary)',
        customClass: {
          icon: 'swal-icon',
        },
      }).then(() => {
        window.location.reload()
      });

    } else {
      updateEditCategoryForm(response.data);
      overlay(editCategoryModalOverlay, false);
    }


  })
);


async function getCategoryInfo(categoryId) {
  try {
    const response = await fetch(`/category/${categoryId}`, {
      method: 'GET'

    });

    return await response.json();

  } catch (error) {
    return {
      status: 500,
      message: 'Erro na conexão. Por favor, recarregue a página e tente novamente.',
    }
  }
}


function updateEditCategoryForm(categoryData) {
 const { name } = categoryData
 editCategoryName.value = name
}



function overlay(element, show) {
  if (show) {
    element.style.display = 'flex'
    return
  }

  element.style.display = 'none'
}



/* 

const editGraduateSubmitButton = document.querySelector("#editGraduateSubmitButton");
editGraduateSubmitButton.addEventListener("click", async (e) => {
  e.preventDefault();

  Swal.fire({
    title: "Editando egresso...",
    didOpen: async () => {
      Swal.showLoading();
      document.getElementById("editGraduateModal").style.display = "none";
    },
    allowOutsideClick: () => !Swal.isLoading(),
    backdrop: "rgba(0,0,0,0.7)",
    background: "#f2f2f2",
  });

  const response = await editGraduate();

  if (response.success) {

    Swal.fire({
      title: "<h3>Egresso editado com sucesso!</h3>",
      icon: "success",
      iconHtml: '<i class="fas fa-check-circle text-success"></i>',
      backdrop: "rgba(0,0,0,0.7)",
      background: "#f2f2f2",
      customClass: {
        icon: "custom-icon-class",
        confirmButton: "btn-primary"
      },
    }).then(() => {
      const editGraduateModal = document.getElementById("editGraduateModal");
      $(editGraduateModal).modal("hide");
    });

    const graduateCpf = document.querySelector("#editLastCpf").value;
    const graduateLineContent = document.querySelector(`#graduateLineContent${graduateCpf}`);

    //UPDATING CPF
    const cpf = document.querySelector("#editCpf").value.replace(/[^0-9]/g, "");
    const lineCpf = graduateLineContent.querySelector(".graduate-cpf");
    lineCpf.innerHTML = cpf;


    //UPDATING BIRTHDATE
    const birthDate = document.querySelector("#editBirthDate").value;
    const [year, month, day] = birthDate.split("-");
    const lineBirthDate = graduateLineContent.querySelector(".graduate-birthdate");
    lineBirthDate.innerHTML = `${day}/${month}/${year}`;


    //UPDATING TD ID
    graduateLineContent.id = `graduateLineContent${cpf}`;


    //UPDATING DATASET EDIT BUTTON
    const editButton = graduateLineContent.querySelector(".edit-graduate-button");
    editButton.dataset.graduateCpf = cpf;


    //UPDATING DATASET DELETE BUTTON
    const deleteButton = graduateLineContent.querySelector(".delete-graduate-button");
    deleteButton.dataset.graduateCpf = cpf;


  } else {
    Swal.fire({
      title: "Falha ao editar egresso!",
      html: response.message,
      icon: "error",
      iconHtml: '<i class="fas fa-times-circle text-danger"></i>',
      backdrop: "rgba(0,0,0,0.7)",
      background: "#f2f2f2",
      customClass: {
        icon: "custom-icon-class",
        confirmButton: "btn-primary"
      },
    }).then(() => {
      document.getElementById("editGraduateModal").style.display = "block";
    });
  }
});


async function editGraduate() {

  try {
    const form = document.getElementById("editGraduateForm");
    const formData = new FormData(form);

    const cleanedCpf = document.getElementById("editCpf").value.replace(/[^0-9]/g, "");

    formData.append("editCpf", cleanedCpf);

    const response = await fetch("/graduate/edit", {
      method: "POST",
      body: formData,
    });

    return await response.json();

  } catch (error) {
    return {
      success: false,
      message: "Erro na conexão. Por favor, recarregue a página e tente novamente."
    }
  }

}




const deleteGraduateButtons = document.querySelectorAll(".delete-graduate-button");
deleteGraduateButtons.forEach((button) =>
  button.addEventListener("click", async (e) => {
    e.preventDefault();

    setTimeout(() => {
      $(button).blur();
    }, 5);

    Swal.fire({
      text: "Você tem certeza que deseja excluir esse egresso?",
      showCancelButton: true,
      cancelButtonText: "Cancelar",
      confirmButtonText: "Confirmar",
      backdrop: "rgba(0,0,0,0.7)",
      background: "#f2f2f2",
      customClass: {
        confirmButton: "btn-primary",
        cancelButton: "btn-danger"
      },
      didClose: () => {
        setTimeout(() => {
          $(button).blur();
        }, 3);
      }
    }).then(async (result) => {

      if (result.isConfirmed) {

        Swal.fire({
          title: "Exluindo egresso...",
          didOpen: async () => {
            Swal.showLoading();
          },
          allowOutsideClick: () => !Swal.isLoading(),
          backdrop: "rgba(0,0,0,0.7)",
          background: "#f2f2f2",
        });

        const response = await deleteGraduate(button.dataset.graduateCpf);

        if (response.success) {

          Swal.fire({
            title: "<h3>Egresso excluído com sucesso!</h3>",
            icon: "success",
            iconHtml: '<i class="fas fa-check-circle text-success"></i>',
            backdrop: "rgba(0,0,0,0.7)",
            background: "#f2f2f2",
            customClass: {
              icon: "custom-icon-class",
              confirmButton: "btn-primary"
            },
          }).then(() => {
            const graduateLineContent = document.querySelector(`#graduateLineContent${button.dataset.graduateCpf}`);
            graduateLineContent.remove();
          });

        } else {
          Swal.fire({
            title: "<h3>Falha ao excluir egresso!</h3>",
            icon: "error",
            iconHtml: `<i class="fas fa-times-circle text-danger"></i>`,
            backdrop: "rgba(0,0,0,0.7)",
            background: "#f2f2f2",
            customClass: {
              icon: "custom-icon-class",
              confirmButton: "btn-primary"
            },
          }).then(() => {
            window.location.reload()
          });
        }
      }
    });
  })
);


async function deleteGraduate(graduateCpf) {
  try {
    const response = await fetch("/graduate/delete/" + graduateCpf, {
      method: "POST",
    });

    return response.json();

  } catch (error) {
    return {
      success: false,
      message: "Erro na conexão. Por favor, recarregue a página e tente novamente."
    };
  }
} */


$(document).ready(() => {
  $(registerCategoryModalButton).tooltip();
  $(".edit-category-button").tooltip();
  $(".delete-category-button").tooltip();


  $(registerCategoryModal).on("hidden.bs.modal", () => {
    $(registerCategoryName).val("");


    setTimeout(() => {
      $(registerCategoryModalButton).blur();
    }, 5);

  });

})




/*   $("#editGraduateModal").on("hidden.bs.modal", () => {
    $("#editLastCpf").val("");
    $("#editCpf").val("");
    $("#editBirthDate").val("");

    setTimeout(() => {
      $(".edit-graduate-button").blur();
    }, 5);
  });


  $("#registerGraduatesModal").on("hidden.bs.modal", () => {
    $("#registerGraduatesFile").val("");

    setTimeout(() => {
      $("#registerGraduatesButton").blur();
    }, 5);
  });

  $(".page-item").on("click", () => {
    $(".edit-graduate-button").tooltip();
    $(".delete-graduate-button").tooltip();
  }); */

// });



