var load_btn = document.getElementById("homepage-load-wb-prices")
var load_spinner = document.getElementById("homepage-load-wb-prices-sipnner")
var data_container = document.getElementById("homepage-wb-prices")
var load_btn_text = document.getElementById("load-btn-text")

var httpRequestPrices;
var isPricesLoading = false;
var ajaxURLPrices = 'load_prices'

load_btn.onclick = function() { getPricesAsync(httpRequestPrices, ajaxURLPrices); }

function getPricesAsync(xhttpr, url) {
  if (!xhttpr) {
    var xhttprArray = [];
    initAJAX(xhttprArray, 1);
    xhttpr = xhttprArray[0];
  }
  loadPrices(xhttpr, url);
}

function loadPrices(xhttpr, url) {
  if (isPricesLoading) {
    return;
  }
  isPricesLoading = true;
  load_spinner.hidden = false;
  load_btn.disabled = true;
  load_btn.className = 'btn btn-dark';
  load_btn_text.innerText = 'Загрузка...'

  xhttpr.open('GET', url, true)
  xhttpr.send(null);
  xhttpr.onreadystatechange = function() { onPricesLoad(xhttpr); };
}

function onPricesLoad(xhttpr) {
  if (xhttpr.readyState == 4 ) {
    if (xhttpr.status == 200) {
      data_container.innerHTML = xhttpr.responseText;
      load_btn_text.innerText = 'Загрузить цены на гречу';
    } else {
      load_btn.className = 'btn btn-danger';
      load_btn_text.innerText = 'Ошибка. Попробуйте еще раз';
    }
  } else {
    return;
  }
  load_spinner.hidden = true;
  load_btn.disabled = false;
  isPricesLoading = false;
}