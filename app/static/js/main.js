// Auto-dismiss alerts after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);
});

// Confirm delete actions
document.addEventListener("click", function (event) {
  if (event.target.matches("[data-confirm]")) {
    if (!confirm(event.target.dataset.confirm)) {
      event.preventDefault();
    }
  }
});

// Enable tooltips everywhere
document.addEventListener("DOMContentLoaded", function () {
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

// Form validation
document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll(".needs-validation");
  Array.from(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false
    );
  });
});

// Price formatting
function formatPrice(price) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  }).format(price);
}

// Date formatting
function formatDate(date) {
  return new Intl.DateTimeFormat("en-IN", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
}

// Copy to clipboard function
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(function () {
      // Show success message
      const toast = new bootstrap.Toast(document.querySelector(".toast"));
      toast.show();
    })
    .catch(function (err) {
      console.error("Failed to copy text: ", err);
    });
}

// Handle mobile navigation
document.addEventListener("DOMContentLoaded", function () {
  const navbarToggler = document.querySelector(".navbar-toggler");
  const navbarCollapse = document.querySelector(".navbar-collapse");

  if (navbarToggler && navbarCollapse) {
    document.addEventListener("click", function (event) {
      const isClickInside =
        navbarToggler.contains(event.target) ||
        navbarCollapse.contains(event.target);

      if (!isClickInside && navbarCollapse.classList.contains("show")) {
        navbarToggler.click();
      }
    });
  }
});
