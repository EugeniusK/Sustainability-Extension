if (document.getElementById("sc-active-cart") != null) {
  var total_co2 = 0;
  calculateCartCo2();

  var total_co2_cart = 0;

  window.addEventListener("click", calculateCartCo2);
  document.getElementById("activeCartViewForm"),
    addEventListener("change", calculateCartCo2);
  function calculateCartCo2() {
    var items = document.getElementById("activeCartViewForm").children;

    for (item of items) {
      if (item.getAttribute("data-name") == "Active Items") {
        var active_items = item;
      }
    }
    var total_co2 = 0;
    for (div of active_items.children) {
      if (div.getAttribute("data-asin") != null) {
        console.log(div);
        console.log(div.getAttribute("data-quantity"));
        console.log(
          div.getElementsByClassName("a-truncate-full")[0].textContent
        );
        div.getElementsByClassName("sc-product-price")[0].textContent =
          "$" +
          div.getAttribute("data-price") +
          " " +
          Math.round(
            parseFloat(div.getAttribute("data-quantity")) *
              localStorage.getItem(
                div.getElementsByClassName("a-truncate-full")[0].textContent
              ) *
              100
          ) /
            100 +
          "kg";
        total_co2 +=
          parseFloat(div.getAttribute("data-quantity")) *
          parseFloat(
            localStorage.getItem(
              div.getElementsByClassName("a-truncate-full")[0].textContent
            )
          );
      }
      total_co2_cart = total_co2;
    }

    localStorage.setItem("co2", total_co2);
    document.getElementsByClassName(
      "a-column a-span2 a-text-right a-spacing-top-micro a-span-last"
    )[0].children[0].innerHTML = "Price CO<sub>2</sub>";
    document.getElementById(
      "sc-subtotal-amount-activecart"
    ).children[0].textContent =
      document
        .getElementById("sc-subtotal-amount-activecart")
        .children[0].textContent.split(" ")[0] +
      " " +
      Math.round(total_co2 * 100) / 100 +
      "kg";
    if (total_co2 == 0) {
      document
        .getElementById("sc-subtotal-amount-activecart")
        .children[0].textContent.split(" ")[0] +
        " " +
        "0.00" +
        "kg";
    }
  }
  document
    .getElementById("sc-buy-box-ptc-button")
    .children[0].children[0].addEventListener("click", function () {
      chrome.runtime.sendMessage({
        type: "contentToBackground",
        co2_to_extension: localStorage.getItem("co2"),
      });
      fetch("http://127.0.0.1:8000/api/item/", {
        method: "POST",
        body: JSON.stringify({ co2e: total_co2 }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      // localStorage.clear();
    });
} else {
  var productTitle = document.getElementById("productTitle").textContent.trim();

  var foundDet = null;
  var prodDet = document.getElementsByClassName("prodDetSectionEntry");
  for (var i = 0; i < prodDet.length; i++) {
    if (prodDet[i].textContent == " Best Sellers Rank ") {
      foundDet = prodDet[i];
    }
  }
  if (foundDet != null) {
    var category = foundDet.nextElementSibling.textContent;
  } else {
    var category_div = document.getElementsByClassName("a-text-bold");
    for (div of category_div) {
      if (div.textContent == " Best Sellers Rank: ") {
        category = div.nextElementSibling.textContent;
      }
    }
  }
  console.log(productTitle, category);

  fetch("http://127.0.0.1:8000/api/search/", {
    method: "POST",
    body: JSON.stringify({ main: productTitle + category }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  })
    .then((response) => response.json())
    .then((json) => {
      localStorage.setItem(productTitle, json["co2e_factor"]);
      if (
        document.getElementById("corePriceDisplay_desktop_feature_div") != null
      ) {
        var price = document
          .getElementById("corePriceDisplay_desktop_feature_div")
          .getElementsByClassName("a-offscreen")[0]
          .textContent.match(/[+-]?\d+(\.\d+)?/g)
          .join("");
        var co2e = co2e_calculate(json, price);
        addCO2ElementFromHTML(co2e_calculate(json, price));
      } else {
        var price_divs = document.getElementsByClassName("swatchElement");
        for (div of price_divs) {
          console.log(div);
          var tmp_price = div
            .getElementsByClassName("a-size-base")[0]
            .textContent.match(/[+-]?\d+(\.\d+)?/g)
            .join("");
          console.log(tmp_price);
          div.getElementsByClassName("a-size-base")[0].innerHTML +=
            '<img width="16px" src="' +
            chrome.runtime.getURL("DODOICON.png") +
            '">' +
            co2e_calculate(json, tmp_price) +
            "kg";
        }
      }
    });
  function addCO2ElementFromHTML(co2) {
    var price_div = document.getElementsByClassName("priceToPay")[0];
    var div = document.createElement("div");
    div.innerHTML =
      '<span class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay" data-a-size="xl" data-a-color="base"><img width="32px" src="' +
      chrome.runtime.getURL("DODOICON.png") +
      '"><span style="top:5px" class="a-price-whole">' +
      co2.toString() +
      "kg</span></span>";
    price_div.parentElement.appendChild(div.firstChild);

    // Change this to div.childNodes to support multiple top-level nodes.
    return div.firstChild;
  }
  function co2e_calculate(json, price) {
    return Math.round(json["co2e_factor"] * parseFloat(price) * 100) / 100;
  }
}
