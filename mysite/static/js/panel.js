import { successMessage, errorMessage } from "./utils/messages.js";
import { getToken, getUserID } from "./utils/tokens.js";

$(() => {
  // Helper function to remove placeholders
  const removePlaceholders = () => {
    $("#sidebarPlaceholder").empty();
    $("#turnosList").empty();
    $("#contentPanel .placeholder-glow").remove();
    $("#testimonioForm").removeClass("placeholder-glow");
  };


  // Mostrar un mensaje en formato de toast
  const showToast = (messageHtml) => {
    $("#response").append(messageHtml);
    const toastEl = $("#response .toast").last()[0];
    if (toastEl) {
      const toast = new bootstrap.Toast(toastEl);
      toast.show();
    }
  };

  async function getUserData() {
    try {
      const response = await fetch(`/API/users/${getUserID()}/`, {
        method: "GET",
      });

      if (!response.ok) {
        showToast(errorMessage("Usuario no autenticado"));
        throw new Error(response.statusText);
      }

      showToast(successMessage("Usuario autenticado"));
      const data = await response.json();
      let img = data.imagen;
      if (data.imagen_url){
        img = data.imagen_url;
      }
      const userData = {
        dni: data.dni,
        nombre: data.nombre,
        apellido: data.apellido,
        username: data.username,
        email: data.email,
        contraseña: data.contraseña,
        imagen: img,
        telefono: data.telefono,
      };
      return userData;
    } catch (error) {
      console.error(error);
      showToast(errorMessage(error.message));
    }
  }

  const loadSidebar = async () => {
    try {
      const templateResponse = await fetch("/static/components/sidebar.hbs");
      const templateText = await templateResponse.text();
      const compiledTemplate = Handlebars.compile(templateText);
      const userData = await getUserData();
      const html = compiledTemplate(userData);
      $("#sidebarPlaceholder").html(html);
    } catch (error) {
      console.error("Error loading sidebar:", error);
    }
  }

  // Fetch user data
  fetch(`/API/users/${getUserID()}/`, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        showToast(errorMessage("Usuario no autenticado"));
        throw new Error(response.statusText);
      }
      showToast(successMessage("Usuario autenticado"));
      return response.json();
    })
    .then((data) => {
      let img = data.imagen;
      if (data.imagen_url){
        img = ' ';
      }
      console.log(data.username);
      const userData = {
        username: data.username,
        email: data.email,
        contraseña: data.contraseña,
        imagen: img,
        CSRF: getToken(),
        telefono: data.telefono, // Asegúrate de que este campo esté presente en tus datos
      };
      renderUserProfileForm(userData);
      initializeFileInput();
      removePlaceholders();
      loadSidebar();
    })
    .catch((error) => {
      console.error(error);
      showToast(errorMessage(error.message));
    });

  // Fetch turnos data
  fetch(`/API/users/${getUserID()}/turnos/`, {
    method: "GET",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      renderTurnosLinks(data);
      initializeTurnosClickEvents();
      removePlaceholders();
    })
    .catch((error) => {
      console.error(error);
      showToast(errorMessage(error.message));
    });

  // Renderizar formulario de perfil de usuario con Handlebars
  const renderUserProfileForm = (userData) => {
    $.get("/static/components/panelForm.hbs", (template) => {
      const compiledTemplate = Handlebars.compile(template);
      const html = compiledTemplate(userData);
      $("#contentPanel").html(html);
      $("#perfilForm").hide();
    });
  };

  // Renderizar lista de turnos
  const renderTurnosLinks = (turnosData) => {
    let turnos = "";
    console.log(turnosData.length)
    if (turnosData.length === 0){
      turnos += `
        <a class="btn btn-dark" href="/turnero/" > Sacar Turno </a>
      `;
      $("#turnosList").html(turnos);
    }else{
      turnosData.forEach((data) => {
        turnos += `
          <a id="turnoLink${data.id}" class="list-group-item list-group-item-action panel-link">
            <div class="d-flex w-100 justify-content-between">
              <h5 class="mb-1">${data.id} ${data.horario.hora}</h5>
              <small>${data.estado}</small>
            </div>
            <p class="mb-1">${data.medico.nombre} - ${data.motivo}</p>
          </a>
        `;
      });
      $("#turnosList").html(turnos);
    }
  };

  // Inicializar eventos de clic en los enlaces de turnos
  const initializeTurnosClickEvents = () => {
    $(".panel-link").on("click", (event) => {
      const id = event.currentTarget.id.split("turnoLink")[1];
      window.location.href = `/turnero/turnos/${id}/`;
    });
  };

  // Inicializar el input de archivo y su comportamiento
  const initializeFileInput = () => {
    $("#fileInput").on("change", function () {
      const fileInput = $(this)[0];
      const fileNameSpan = $("#fileName");

      if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileNameSpan.text(fileName);
      } else {
        fileNameSpan.text("No file chosen");
      }
    });
  };

  // Renderizar formulario de testimonio
  const testimonioForm = (testimonioData) => {
    return `
      <form id="testimonioForm" class="card p-4 shadow-sm">
        <div class="mb-3">
          <textarea class="form-control" placeholder="Testimonio">${testimonioData?.content || ""}</textarea>
        </div>
      </form>
    `;
  };

  // Inicializar contenido con placeholders
  $("#contentPanel").append(testimonioForm({ content: "testimonio de John Doe" }));
  $("#testimonioForm").hide();

  // Manejar navegación por pestañas
  $("#perfilTab").on("click", () => {
    $("#turnosTab").removeClass("active");
    $("#perfilTab").addClass("active");
    $("#testimoniosTab").removeClass("active");
    $("#perfilForm").show();
    $("#testimonioForm").hide();
    $("#turnosList").hide();
  });

  $("#turnosTab").on("click", () => {
    $("#turnosTab").addClass("active");
    $("#perfilTab").removeClass("active");
    $("#testimoniosTab").removeClass("active");
    $("#turnosList").show();
    $("#perfilForm").hide();
    $("#testimonioForm").hide();
  });

  $("#testimoniosTab").on("click", () => {
    $("#turnosTab").removeClass("active");
    $("#testimoniosTab").addClass("active");
    $("#perfilTab").removeClass("active");
    $("#testimonioForm").show();
    $("#perfilForm").hide();
    $("#turnosList").hide();
  });
});