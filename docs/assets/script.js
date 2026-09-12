/**
 * Livro 3D — reconstrução em CSS/JS puro (sem dependências) do visualizador
 * de capa em 3D usado em lojas como a uiClap, aplicado ao livro
 * "O Horizonte na Paulista". Arrasta ou usa o slider para girar.
 */
(function () {
  "use strict";

  const ROTACAO_MIN = -360;
  const ROTACAO_MAX = 0;
  const ROTACAO_INICIAL = -145;
  const RAZAO_ALTURA = 494.857 / 346.4; // proporção real da capa do livro
  const RAZAO_LOMBADA = 27.8357 / 346.4;

  function iniciarLivro3D(raiz) {
    const wrapper = raiz.querySelector(".livro3d-wrapper");
    const livro = raiz.querySelector(".livro");
    const slider = raiz.querySelector(".livro3d-slider");

    let rotacaoAtual = ROTACAO_INICIAL;
    let arrastando = false;
    let inicioX = 0;
    let rotacaoNoInicio = 0;

    function aplicarRotacao(graus, comTransicao) {
      rotacaoAtual = Math.max(ROTACAO_MIN, Math.min(ROTACAO_MAX, graus));
      livro.classList.toggle("sem-transicao", !comTransicao);
      livro.style.setProperty("--rotation", rotacaoAtual + "deg");
      if (slider) slider.value = String(Math.round(rotacaoAtual));
    }

    function medirEAjustarDimensoes() {
      const larguraDisponivel = raiz.clientWidth || 320;
      const larguraAlvo = Math.min(340, Math.max(200, larguraDisponivel));
      const altura = larguraAlvo * RAZAO_ALTURA;
      const lombada = larguraAlvo * RAZAO_LOMBADA;
      const margem = altura / 10;

      const vars = {
        "--w": larguraAlvo + "px",
        "--h": altura + "px",
        "--t": lombada + "px",
        "--half-t": lombada / 2 + "px",
        "--neg-half-t": -(lombada / 2) + "px",
        "--half-w": larguraAlvo / 2 + "px",
        "--half-h": altura / 2 + "px",
        "--spine-left": (larguraAlvo / 2 - lombada / 2) + "px",
        "--edge-top": (altura / 2 - lombada / 2) + "px",
        "--perspective": larguraAlvo * 2 + "px",
        "--margin": margem + "px",
      };

      Object.keys(vars).forEach(function (nome) {
        raiz.style.setProperty(nome, vars[nome]);
      });
    }

    function posicaoX(evento) {
      if (evento.touches && evento.touches.length) {
        return evento.touches[0].clientX;
      }
      return evento.clientX;
    }

    function onPointerDown(evento) {
      arrastando = true;
      inicioX = posicaoX(evento);
      rotacaoNoInicio = rotacaoAtual;
      wrapper.classList.add("dragging");
      if (evento.cancelable) evento.preventDefault();
    }

    function onPointerMove(evento) {
      if (!arrastando) return;
      const deltaX = posicaoX(evento) - inicioX;
      aplicarRotacao(rotacaoNoInicio + deltaX * 0.5, false);
    }

    function onPointerUp() {
      if (!arrastando) return;
      arrastando = false;
      wrapper.classList.remove("dragging");
    }

    wrapper.addEventListener("mousedown", onPointerDown);
    window.addEventListener("mousemove", onPointerMove);
    window.addEventListener("mouseup", onPointerUp);

    wrapper.addEventListener("touchstart", onPointerDown, { passive: false });
    window.addEventListener("touchmove", onPointerMove, { passive: true });
    window.addEventListener("touchend", onPointerUp);

    if (slider) {
      slider.addEventListener("input", function () {
        aplicarRotacao(Number(slider.value), false);
      });
    }

    window.addEventListener("resize", medirEAjustarDimensoes);

    medirEAjustarDimensoes();
    aplicarRotacao(ROTACAO_MIN, false);

    // Pequena apresentação: o livro gira até a pose de destaque ao carregar.
    requestAnimationFrame(function () {
      setTimeout(function () {
        aplicarRotacao(ROTACAO_INICIAL, true);
      }, 250);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-livro3d]").forEach(iniciarLivro3D);
  });
})();
