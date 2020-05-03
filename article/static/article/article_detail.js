// article-detail的高度
var article_height = $('.content-body').outerHeight(true);
var list_body = $('.list-body').outerHeight(true);
// 课程介绍的高度补不满时
if(article_height <= 600) {
  //不满600px时，设置其高为600px，添加new_height
  $(".content-body").addClass('new-height');
}else{
  $(".content-body").removeClass('new-height');
}
// 课程目录的高度不满时
if(list_body <= 600) {
  //不满600px时，设置其高为600px，添加new_height
  $(".list_body").addClass('new-height');
}else{
  console.log('yes');
  $(".list_body").removeClass('new-height');
}
$('.change').click(function () {
  if(article_height <= 600) {
  //不满600px时，设置其高为600px，添加new_height
    $(".content-body").addClass('new-height');
  }else{
    $(".content-body").removeClass('new-height');
  }
  if(list_body <= 600) {
  //不满600px时，设置其高为600px，添加new_height
    $(".list_body").addClass('new-height');
  }else{
    $(".list_body").removeClass('new-height');
  }
});
function beginStudy() {
  $('html').animate({scrollTop: $('.change').offset().top - 60}, 300, function () {
    $('.change').eq(1).addClass('active').siblings().removeClass('active');
    $('.cont').eq(1).addClass('active').siblings().removeClass('active');
      });
}

// 选项卡
$(function () {
  //选项卡切换
  $('.category ul li').click(function () {
    const tab_num = $(this).index();
    $(this).addClass('active').siblings().removeClass('active');
    $('.cont').eq(tab_num).addClass('active').siblings().removeClass('active');
    sessionStorage.setItem('tab_num', tab_num);
    sessionStorage.setItem('url', window.location.pathname)
  });
});
// 消息入口时，页面滑动到对应评价处
if (window.location.hash) {
  $('.category ul li').eq(2).addClass('active').siblings().removeClass('active');
  $('.cont').eq(2).addClass('active').siblings().removeClass('active');
  $('html').animate({
      scrollTop: $(window.location.hash).offset().top - 60
  }, 500);
}
else{
  // 选项卡记录
  $(window).load(function () {
    const tab_num = sessionStorage.getItem('tab_num');
    if (tab_num == null) {
      $('.category ul li').eq(1).addClass('active').siblings().removeClass('active');
    }
    $('.category ul li').eq(tab_num).addClass('active').siblings().removeClass('active');
    $('.cont').eq(tab_num).addClass('active').siblings().removeClass('active');
  });
}

// 星星打分
window.onload = function () {
  // var s = document.getElementById("pingStar");
   var s = $('#pingStar');
  // n = s.getElementsByTagName("li");
  n = $('#pingStar li');
    input = $("#startP");//保存所选值
  score = $('#id_scored');
  clearAll = function () {
    for (var i = 0; i < n.length; i++) {
      n[i].className = "";
    }
  };
  for (var i = 0; i < n.length; i++) {
    n[i].onclick = function () {
      var q = this.getAttribute("rel");
      clearAll();
      score.val(q);
      for (var i = 0; i < q; i++) {
        n[i].className = "on";
      }
    };
    n[i].onmouseover = function () {
      var q = this.getAttribute("rel");
      clearAll();
      for (var i = 0; i < q; i++) {
        n[i].className = "on";
      }
    };
    n[i].onmouseout = function () {
      clearAll();
      for (var i = 0; i < score.val(); i++) {
        n[i].className = "on";
      }
    }
  }
};
window.onload = function(){
  let to_top = $('#to-top');
  to_top.fadeOut();
  $(window).scroll(function () {
    if ($(window).scrollTop() > 600) {
      to_top.fadeIn();
    }else {
      to_top.fadeOut();
    }
  });
  to_top.click(function() {
    $('body,html').animate({
      scrollTop: 0
    },
    500);
    return false;
  });
};