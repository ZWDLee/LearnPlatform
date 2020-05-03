    $(document).ready(function () {
      //设计案例切换
      var clickindex = 0;  // 记录点击时的对象序列
      $('.new_telst li').click(function () {
        var liindex = $('.new_telst li').index(this);
        clickindex = liindex;
        $(this).addClass('newon').siblings().removeClass('newon');
        $('.new-wrap div.new_lst').eq(liindex).fadeIn(150).siblings('div.new_lst').hide();
        var liWidth = $('.new_telst li').width();
        $('.newtel .new_telst p').stop(false, true).animate({'left': liindex * liWidth + 'px'}, 300);
      });
      // 鼠标悬浮时
      $('.new_telst li').mouseover(function () {
        var liindex = $('.new_telst li').index(this);
        var liWidth = $('.new_telst li').width();
        $('.newtel .new_telst p').stop(false, true).animate({'left': liindex * liWidth + 'px'}, 300);
      });
      // 鼠标离开时
      $('.new_telst').mouseleave(function () {
        var liWidth = $('.new_telst li').width();
        $('.newtel .new_telst p').stop(false, true).animate({'left': clickindex * liWidth + 'px'}, 350);
      });
    });

    //底部栏置底
    //窗体改变大小事件
    $(window).click(function () {
      //正文高度
      var body_height = $(document.body).outerHeight(true);
      //底部元素高度
      var bottom_height = $("#footer").outerHeight(true);
      //浏览器页面高度
      var window_height = $(window).height();
      //判断并调整底部元素的样式
      if ($(".footer").hasClass('page-bottom')) {
        //若包含有page-bottom类，就应用了position设置
        //当position为absolute时，body高度不包含这个元素
        //所以页面高度需要判断body和footer之和若小于浏览器窗口
        //则移除样式，让footer自然跟随在正文后面
        if (body_height + bottom_height >= window_height) {
          $(".footer").removeClass('page-bottom');
        }
      } else {
        //若没有page-bottom类，body高度包含footer
        //判断body高度小于浏览器时，则悬浮于底部
        if (body_height < window_height) {
          $(".footer").addClass('page-bottom');
        }
      }
    });
    //页面加载时，模拟触发一下resize事件
    $(window).trigger('resize');