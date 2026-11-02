(function () {
  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Tema: il default è scuro, la scelta resta in questo browser.
  var toggle = document.querySelector(".theme");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.dataset.theme === "light" ? "dark" : "light";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // Le card seguono il puntatore con un alone.
  document.querySelectorAll(".card").forEach(function (card) {
    card.addEventListener("pointermove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", e.clientX - r.left + "px");
      card.style.setProperty("--my", e.clientY - r.top + "px");
    });
  });

  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -40px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // Il terminale della home scrive il comando, poi mostra l'output.
  var term = document.querySelector(".term[data-type]");
  if (term && !reduced && !document.hidden) {
    var cmd = term.querySelector(".cmd");
    var text = cmd.textContent;
    var i = 0;
    cmd.textContent = "";
    term.classList.add("typing");
    (function type() {
      cmd.textContent = text.slice(0, ++i);
      if (i < text.length) setTimeout(type, 34);
      else setTimeout(function () { term.classList.remove("typing"); }, 180);
    })();
  }

  // Frecce della galleria di screenshot.
  document.querySelectorAll(".arrows button").forEach(function (button) {
    button.addEventListener("click", function () {
      var gallery = document.querySelector(".gallery");
      var step = gallery.querySelector("img").clientWidth + 16;
      gallery.scrollBy({ left: Number(button.dataset.dir) * step, behavior: reduced ? "auto" : "smooth" });
    });
  });
})();
