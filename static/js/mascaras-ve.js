/**
 * Máscaras de entrada — cédula y teléfono venezolanos
 */
(function () {
  "use strict";

  function soloDigitos(s) {
    return (s || "").replace(/\D/g, "");
  }

  function formatoCedulaNumero(d) {
    d = soloDigitos(d).slice(0, 9);
    if (!d) return "";
    var partes = [];
    while (d.length > 3) {
      partes.unshift(d.slice(-3));
      d = d.slice(0, -3);
    }
    if (d) partes.unshift(d);
    return partes.join(".");
  }

  function formatoTelefonoLinea(d) {
    d = soloDigitos(d).slice(0, 7);
    if (d.length <= 3) return d;
    return d.slice(0, 3) + "-" + d.slice(3);
  }

  function initCedula() {
    var input = document.getElementById("id_cedula_numero");
    if (!input) return;
    input.addEventListener("input", function () {
      var pos = input.selectionStart;
      var antes = input.value.length;
      input.value = formatoCedulaNumero(input.value);
      var despues = input.value.length;
      input.setSelectionRange(pos + (despues - antes), pos + (despues - antes));
    });
    input.addEventListener("keypress", function (e) {
      if (!/\d/.test(e.key) && e.key.length === 1) e.preventDefault();
    });
  }

  function initTelefono() {
    var linea = document.getElementById("id_telefono_linea");
    var operadora = document.getElementById("id_telefono_operadora");
    var hint = document.getElementById("tel-prefix-hint");
    if (!linea) return;

    function actualizarHint() {
      if (hint && operadora) hint.textContent = operadora.value || "04XX";
    }

    linea.addEventListener("input", function () {
      linea.value = formatoTelefonoLinea(linea.value);
    });
    linea.addEventListener("keypress", function (e) {
      if (!/\d/.test(e.key) && e.key.length === 1) e.preventDefault();
    });
    if (operadora) {
      operadora.addEventListener("change", actualizarHint);
      actualizarHint();
    }
  }

  function initProfesionOtro() {
    var sel = document.getElementById("id_profesion");
    var wrap = document.getElementById("wrap-profesion-otro");
    if (!sel || !wrap) return;
    function toggle() {
      wrap.style.display = sel.value === "otro" ? "" : "none";
    }
    sel.addEventListener("change", toggle);
    toggle();
  }

  document.addEventListener("DOMContentLoaded", function () {
    initCedula();
    initTelefono();
    initProfesionOtro();
  });
})();
