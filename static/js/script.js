document.addEventListener("DOMContentLoaded", () => {
  showSection("about");
  document
    .getElementById("checkout-form")
    .addEventListener("submit", handleCheckout);
  updateCartDisplay(cart);
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

  const targetSection = document.getElementById(id);
  if (targetSection) {
    targetSection.classList.add("active");
  } else {
    console.warn(`Section with id ${id} not found.`);
  }

  const targetMenuItem = document.querySelector(`nav ul li a[href="#${id}"]`);
  if (targetMenuItem) {
    targetMenuItem.classList.add("active");
  } else {
    console.warn(`Menu item with href "#${id}" not found.`);
  }
}

function changeQuantity(productId, change) {
  var quantityInput = document.getElementById("quantity" + productId);
  var currentQuantity = parseInt(quantityInput.value, 10);
  var newQuantity = currentQuantity + change;
  if (newQuantity >= 1) {
    quantityInput.value = newQuantity;
  }
}

function addToCart(productId, quantity) {
  if (!quantity) {
    quantity = 1;
  }

  const csrftoken = getCookie("csrftoken");

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

function updateCartDisplay(cart) {
  let cartList = document.getElementById("cart-list");
  cartList.innerHTML = "";

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

function handleCheckout(event) {
  event.preventDefault();

  fetch("/checkout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(cart),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("結帳成功！");
        cart = [];
        updateCartDisplay();
      } else {
        alert("結帳失敗，請稍後再試。");
      }
    })
    .catch((error) => {
      console.error("結帳時發生錯誤：", error);
      alert("結帳失敗，請稍後再試。");
    });
}

// 全局变量
var cart = [];

document.addEventListener("DOMContentLoaded", function () {
  // 通过AJAX获取图表数据
  fetch("/get-chart-data/")
    .then((response) => response.json())
    .then((data) => {
      // 处理日营收的折线图
      const revenueCtx = document
        .getElementById("revenueChart")
        .getContext("2d");
      new Chart(revenueCtx, {
        type: "line",
        data: {
          labels: data.revenue_labels,
          datasets: [
            {
              label: "每日營收",
              data: data.revenue_data,
              borderColor: "rgba(75, 192, 192, 1)",
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });

      // 处理最热门商品的柱状图
      const popularCtx = document
        .getElementById("popularProductsChart")
        .getContext("2d");
      new Chart(popularCtx, {
        type: "bar",
        data: {
          labels: data.popular_products_labels,
          datasets: [
            {
              label: "最熱門商品週銷量",
              data: data.popular_products_data,
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });

      // 处理最不热门商品的柱状图
      const unpopularCtx = document
        .getElementById("unpopularProductsChart")
        .getContext("2d");
      new Chart(unpopularCtx, {
        type: "bar",
        data: {
          labels: data.unpopular_products_labels,
          datasets: [
            {
              label: "最不熱門商品週銷量",
              data: data.unpopular_products_data,
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    })
    .catch((error) => console.error("Error fetching chart data:", error));
});
