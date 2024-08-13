document.addEventListener("DOMContentLoaded", () => {
  showSection("about");
});

function showSection(id) {
  const sections = document.querySelectorAll(".content-section");
  const menuItems = document.querySelectorAll("nav ul li a");

  sections.forEach((section) => {
    section.classList.remove("active");
  });

  menuItems.forEach((item) => {
    item.classList.remove("active");
  });

  document.getElementById(id).classList.add("active");
  document.querySelector(`nav ul li a[href="#${id}"]`).classList.add("active");
}

function addToCart(productId, quantity) {
  // You can implement AJAX or other methods here to handle cart operations
  console.log(`Product ID: ${productId}, Quantity: ${quantity}`);
}
