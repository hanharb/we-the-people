(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Footer year ---------------------------------------------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Sticky header shadow -------------------------------------- */
  var header = document.getElementById("site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobile nav toggle ------------------------------------------ */
  var nav = document.getElementById("main-nav");
  var toggle = document.getElementById("nav-toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-label", isOpen ? "Menü schließen" : "Menü öffnen");
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---------- Scroll reveal ------------------------------------------------ */
  var revealTargets = document.querySelectorAll(
    ".fade-in, .process-step, .js-reveal-canvas, .js-pipeline"
  );

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealTargets.forEach(function (el) {
      el.classList.add("is-visible");
    });
  } else {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3, rootMargin: "0px 0px -8% 0px" }
    );
    revealTargets.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------- Contact form (Web3Forms, AJAX) ------------------------------ */
  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");

  if (form && status) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();

      var accessKey = form.querySelector('input[name="access_key"]');
      if (accessKey && accessKey.value === "YOUR_WEB3FORMS_ACCESS_KEY") {
        status.textContent =
          "Formular ist noch nicht aktiv: Bitte zuerst einen gültigen Web3Forms Access Key hinterlegen.";
        status.className = "form-status is-error";
        return;
      }

      var submitBtn = form.querySelector('button[type="submit"]');
      var originalLabel = submitBtn ? submitBtn.textContent : "";
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Wird gesendet …";
      }
      status.className = "form-status";
      status.textContent = "";

      var formData = new FormData(form);
      var payload = Object.fromEntries(formData.entries());
      payload.access_key = form.querySelector('input[name="access_key"]').value;

      fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { ok: res.ok, data: data };
          });
        })
        .then(function (result) {
          if (result.ok && result.data && result.data.success) {
            status.textContent =
              "Danke für Ihre Nachricht. Wir melden uns zeitnah bei Ihnen.";
            status.className = "form-status is-success";
            form.reset();
          } else {
            throw new Error((result.data && result.data.message) || "Unbekannter Fehler");
          }
        })
        .catch(function () {
          status.textContent =
            "Ihre Nachricht konnte nicht gesendet werden. Bitte versuchen Sie es erneut oder schreiben Sie uns direkt per E-Mail.";
          status.className = "form-status is-error";
        })
        .finally(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = originalLabel;
          }
        });
    });
  }
})();
