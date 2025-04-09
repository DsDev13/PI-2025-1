// Feedback visual ao clicar nos botões
document.querySelectorAll("button").forEach(button => {
    button.addEventListener("mousedown", () => {
      button.style.transform = "scale(0.95)";
    });
    button.addEventListener("mouseup", () => {
      button.style.transform = "scale(1)";
    });
    button.addEventListener("mouseleave", () => {
      button.style.transform = "scale(1)";
    });
  });
  
  document.addEventListener('DOMContentLoaded', () => {
    // Menu lateral recolhível
    const toggleBtn = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
  
    if (toggleBtn && sidebar) {
      toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
      });
    }
  
    // Filtro de anúncios por qualquer conteúdo com destaque
    const filtro = document.getElementById("filtro-anuncio");
    const anuncios = document.querySelectorAll(".anuncio, .card");
  
    filtro?.addEventListener("input", () => {
      const termo = filtro.value.trim().toLowerCase();
  
      anuncios.forEach(anuncio => {
        // Salva o HTML original se ainda não tiver salvo
        if (!anuncio.getAttribute("data-original-html")) {
          anuncio.setAttribute("data-original-html", anuncio.innerHTML);
        }
  
        const originalHTML = anuncio.getAttribute("data-original-html");
        anuncio.innerHTML = originalHTML;
  
        const textoCompleto = anuncio.innerText.toLowerCase();
  
        if (textoCompleto.includes(termo)) {
          anuncio.style.display = "block";
  
          if (termo.length > 0) {
            const regex = new RegExp(`(${termo})`, 'gi');
            anuncio.innerHTML = anuncio.innerHTML.replace(regex, `<mark>$1</mark>`);
          }
  
        } else {
          anuncio.style.display = "none";
        }
      });
    });
  
    // Pré-visualização de imagem
    const inputImagem = document.getElementById('id_imagem');
    const preview = document.getElementById('preview');
  
    if (inputImagem && preview) {
      inputImagem.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
          preview.style.display = "block";
          const reader = new FileReader();
          reader.onload = function (e) {
            preview.src = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      });
    }
  });
  