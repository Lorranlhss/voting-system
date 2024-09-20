// Função para verificar se o usuário escolheu uma opção de voto antes de enviar
function validarVoto() {
  const radios = document.querySelectorAll('input[name="voto"]');
  let votoSelecionado = false;

  // Verifica se algum dos botões de rádio está selecionado
  for (const radio of radios) {
      if (radio.checked) {
          votoSelecionado = true;
          break;
      }
  }

  // Se nenhum voto foi selecionado, mostra um alerta
  if (!votoSelecionado) {
      alert('Por favor, selecione um candidato antes de votar.');
      return false;
  }
  return true;
}

// Associa o evento ao botão de envio do formulário de votação
document.querySelector("form").addEventListener("submit", function(event) {
  let radios = document.querySelectorAll('input[name="voto"]:checked');
  if (radios.length === 0) {
      alert("Por favor, selecione um candidato antes de votar.");
      event.preventDefault();
  }
});