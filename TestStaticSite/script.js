function scrollToSection(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

function openModal(member) {
  const modal = document.getElementById("modal");
  const title = document.getElementById("modal-title");
  const desc = document.getElementById("modal-description");

  if (member === 'john') {
    title.textContent = "John - CEO";
    desc.textContent = "John is the visionary leader who drives innovation at our company.";
  } else if (member === 'jane') {
    title.textContent = "Jane - CTO";
    desc.textContent = "Jane spearheads all tech-related innovations and R&D.";
  } else if (member === 'mike') {
    title.textContent = "Mike - Designer";
    desc.textContent = "Mike ensures the designs are top-notch and intuitive.";
  }

  modal.classList.remove("hidden");
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}

document.getElementById("contactForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const message = document.getElementById("message").value.trim();
  const msgBox = document.getElementById("form-message");

  if (!name || !email || !message) {
    msgBox.textContent = "Please fill in all fields!";
    msgBox.style.color = "red";
    return;
  }

  msgBox.textContent = "Thanks for contacting us, " + name + "!";
  msgBox.style.color = "green";
  this.reset();
});
