var comments_section = document.getElementById("homepage-feedback-block");
var comments_spinner = document.getElementById("homepage-load-comments-sipnner");
var send_comment_btn = document.getElementById("send-comment-btn");
var comment_nickname = document.getElementById("nickname");
var comment_text = document.getElementById("comment");
var comment_form = document.getElementById("comment-form");
var delete_comment_btn = document.getElementsByClassName("delete-comment-btn");
var like_btn = document.getElementsByClassName("like-btn");
var dislike_btn = document.getElementsByClassName("dislike-btn");

var isCommentsLoading = false;
var comments;
var context;

class CommentUpdate {
  constructor(comment_id, action) {
    this.comment_id = comment_id;
    this.action = action;
  }
}

class CommentsContext {
  constructor() { 
    this.xhttprArray = [];
    initAJAX(this.xhttprArray, 3);

    this.httpRequestComments = this.xhttprArray[0];
    this.httpRequestUpdate = this.xhttprArray[1];
    this.httpRequestAddComment = this.xhttprArray[2];

    this.ajaxURLLoadComments = 'load_comments';
    this.ajaxURLAddComment = 'add_comment';
    this.ajaxURLUpdateComment = 'update_comment';
  }
}

$(document).ready(function() {
  context = new CommentsContext()

  if (comment_form) {
    comment_nickname.onkeyup = function() {
      const forbidden = new RegExp('[!@#$%^&*()_]');
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
  
    send_comment_btn.onclick = function() {
      if (send_comment_btn.disabled == true) {
        return;
      }
      if (comment_nickname.value.length == 0 || comment_text.value.length == 0) {
        return;
      }
      sendComment(context);
    }
  }

  getCommentsAsync(context);
});

async function getCommentsAsync(context) {
  while(true) {
    loadComments(context);
    await new Promise(r => setTimeout(r, 500000));
    // TODO: сделать подгрузку по скроллу/нажатию
  }
}

function deleteComment(e, context) {
  var xhttpr = context.httpRequestUpdate;
  var url = context.ajaxURLUpdateComment;

  var comment_id_hidden = e.currentTarget.parentNode.getElementsByClassName('comment-id')[0];
  var csrf_token = comment_id_hidden.nextElementSibling.value;
  var comment_id = comment_id_hidden.value;
  var action = new CommentUpdate(comment_id, 'delete');
  var action_json = JSON.stringify(action);
  
  xhttpr.open('POST', url, true);
  xhttpr.setRequestHeader('X-CSRFToken', csrf_token);
  xhttpr.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
  xhttpr.send(action_json);
  xhttpr.onreadystatechange = function() { loadComments(context); };
}

function sendComment(context) {
  var xhttpr = context.httpRequestAddComment;
  var url = context.ajaxURLAddComment;
  var commentFormData = new FormData(document.forms.comment_form);

  send_comment_btn.disabled = true;
  xhttpr.open('POST', url, true);
  xhttpr.send(commentFormData);
  xhttpr.onreadystatechange = function() { onCommentSent(context); };
}

function onCommentSent(context) {
  var xhttpr = context.httpRequestAddComment;

  if (xhttpr.readyState == XMLHttpRequest.DONE ) {
    if (xhttpr.status == 200) {
      send_comment_btn.className = 'btn btn-success';
      send_comment_btn.innerText = 'Отправлено';
      loadComments(context);
    } else {
      send_comment_btn.innerText = "Ошибка при отправке";
      send_comment_btn.className = 'btn btn-danger';
    }
  } else {
    return;
  }
  send_comment_btn.disabled = false;
}

function getLastCommentId() {
  return '0';
}

function loadComments(context) {
  if (isCommentsLoading == true) {
    return;
  }
  var xhttpr = context.httpRequestComments;
  var url = context.ajaxURLLoadComments;
  
  isCommentsLoading = true;
  var url_params = new URLSearchParams();
  url_params.append('lastComment', getLastCommentId());
  xhttpr.open('GET', url + '?' + url_params, true);
  xhttpr.send(null);
  xhttpr.onreadystatechange = function() { onCommentsLoad(context); };
}

function onCommentsLoad(context) {
  var xhttpr = context.httpRequestComments;

  if (xhttpr.readyState == 4) {
    if (xhttpr.status == 200) {
      var responce = xhttpr.responseText;
      // TODO: дополнять, а не перезаписывать
      comments_section.innerHTML = responce;
      comments_spinner.hidden = true;
      $('[data-toggle="popover"]').popover();
      var comments = document.getElementsByClassName('comment-card');
      var i;
      for (i = 0; i < comments.length; i++) {
        delete_btn = comments[i].getElementsByClassName('delete-comment-btn')[0];

        if (delete_btn) {
          delete_btn.onclick = function(e) { deleteComment(e, context); };
        }
      }

    } else {
      comments_section.innerText = "Ошибка при загрузке отзывов";
    }
  } else {
      return;
  }

  isCommentsLoading = false;
}