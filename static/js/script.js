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
  if (!quantity) {
    quantity = 1; // 如果没有传递数量值，设置默认值
  }

  const csrftoken = getCookie("csrftoken"); // 获取CSRF token

  fetch("/add-to-cart/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("成功加入購物車", data);
      updateCartDisplay(data.cart);
    })
    .catch((error) => {
      console.error("發生錯誤:", error);
    });
}

function updateCartUI(cart) {
  const cartList = document.querySelector(".cart-section ul");
  cartList.innerHTML = "";
  for (const [itemId, item] of Object.entries(cart)) {
    cartList.innerHTML += `<li>${item.name} x ${item.quantity} - $${item.price}</li>`;
  }
}

function updateCartDisplay(cart) {
  let cartList = document.getElementById("cart-list");
  cartList.innerHTML = ""; // 清空現有列表

  for (let item_id in cart) {
    let item = cart[item_id];
    let listItem = document.createElement("li");
    listItem.textContent = `${item.name} x ${item.quantity} - $${item.price}`;
    cartList.appendChild(listItem);
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
