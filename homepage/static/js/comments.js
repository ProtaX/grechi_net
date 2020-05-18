var comments_section = document.getElementById("homepage-feedback-block");
var comments_spinner = document.getElementById("homepage-load-comments-sipnner");
var send_comment_btn = document.getElementById("send-comment-btn");
var comment_nickname = document.getElementById("nickname");
var comment_text = document.getElementById("comment");
var comment_form = document.getElementById("comment-form");

var httpRequestComments;
var isCommentsLoading = false;
var ajaxURLComments = 'load_comments';
var lastUpdateDate = '0';

$(document).ready(function(){
  getCommentsAsync(httpRequestComments, ajaxURLComments);
});

if (comment_nickname) {
  comment_nickname.onkeyup = function() {
    const forbidden = new RegExp('[!@#$%^&*()]');
    var res = comment_nickname.value.match(forbidden);
    if (res) {
      send_comment_btn.className = 'btn btn-danger';
      send_comment_btn.innerText = 'Некорректное имя';
      send_comment_btn.disabled =  true;
    }
    else {
      send_comment_btn.className = 'btn btn-dark my-2 my-sm-0';
      send_comment_btn.innerText = 'Отправить';
      send_comment_btn.disabled =  false;
    }
  }
}

if (send_comment_btn) {
  send_comment_btn.onclick = function() {
    if (send_comment_btn.disabled == true) {
      return;
    }
    if (comment_nickname.value.length == 0 || comment_text.value.length == 0) {
      return;
    }
    // TODO: ajax here instead
    comment_form.submit();
  }
}

async function getCommentsAsync(xhttpr, url) {
  if (window.XMLHttpRequest) {
      xhttpr = new XMLHttpRequest();
  if (xhttpr.overrideMimeType) {
      xhttpr.overrideMimeType('text/xml');
      }
  } else if (window.ActiveXObject) { // IE
      try {
          xhttpr = new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e) {
          try {
              xhttpr = new ActiveXObject("Microsoft.XMLHTTP");
          } catch (e) {
              alert('Ваш браузер не поддерживает AJAX');
              return false;
          }
      }
  }
  if (!xhttpr) {
      alert('Ваш браузер не поддерживает AJAX');
      return false;
  }

  while(true) {
    loadComments(xhttpr, url);
    await new Promise(r => setTimeout(r, 105000));
  }
}

function loadComments(xhttpr, url) {
  if (isCommentsLoading == true) {
    return;
  }
  isCommentsLoading = true;
  var url_params = new URLSearchParams();
  url_params.append('lastUpdate', lastUpdateDate)
  console.log(url_params);
  xhttpr.open('GET', url + '?' + url_params, true);
  console.log(url_params);
  xhttpr.send(null);
  xhttpr.onreadystatechange = function() { onCommentsLoad(xhttpr); };
}

function onCommentsLoad(xhttpr) {
  if (xhttpr.readyState == 4 ) {
    if (xhttpr.status == 200) {
      var responce = xhttpr.responseText;
      comments_section.innerHTML = responce;
      comments_spinner.hidden = true;
      lastUpdateDate = new Date();
      $('[data-toggle="popover"]').popover();
    } else {
      comments_section.innerText = "Ошибка при загрузке отзывов";
    }
  } else {
      return;
  }

  isCommentsLoading = false;
}