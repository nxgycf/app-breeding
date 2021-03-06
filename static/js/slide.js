;(function($){
      var touch = {},
        touchTimeout, tapTimeout, swipeTimeout, longTapTimeout,
        longTapDelay = 750,
        gesture

      function swipeDirection(x1, x2, y1, y2) {
        return Math.abs(x1 - x2) >=
          Math.abs(y1 - y2) ? (x1 - x2 > 0 ? 'Left' : 'Right') : (y1 - y2 > 0 ? 'Up' : 'Down')
      }

      function longTap() {
        longTapTimeout = null
        if (touch.last) {
          touch.el.trigger('longTap')
          touch = {}
        }
      }

      function cancelLongTap() {
        if (longTapTimeout) clearTimeout(longTapTimeout)
        longTapTimeout = null
      }

      function cancelAll() {
        if (touchTimeout) clearTimeout(touchTimeout)
        if (tapTimeout) clearTimeout(tapTimeout)
        if (swipeTimeout) clearTimeout(swipeTimeout)
        if (longTapTimeout) clearTimeout(longTapTimeout)
        touchTimeout = tapTimeout = swipeTimeout = longTapTimeout = null
        touch = {}
      }

      function isPrimaryTouch(event){
        return (event.pointerType == 'touch' ||
          event.pointerType == event.MSPOINTER_TYPE_TOUCH)
          && event.isPrimary
      }

      function isPointerEventType(e, type){
        return (e.type == 'pointer'+type ||
          e.type.toLowerCase() == 'mspointer'+type)
      }

      $(document).ready(function(){
        var now, delta, deltaX = 0, deltaY = 0, firstTouch, _isPointerType

        if ('MSGesture' in window) {
          gesture = new MSGesture()
          gesture.target = document.body
        }

        $(document)
          .bind('MSGestureEnd', function(e){
            var swipeDirectionFromVelocity =
              e.velocityX > 1 ? 'Right' : e.velocityX < -1 ? 'Left' : e.velocityY > 1 ? 'Down' : e.velocityY < -1 ? 'Up' : null
            if (swipeDirectionFromVelocity) {
              touch.el.trigger('swipe')
              touch.el.trigger('swipe'+ swipeDirectionFromVelocity)
            }
          })
          .on('touchstart MSPointerDown pointerdown', function(e){
            if((_isPointerType = isPointerEventType(e, 'down')) &&
              !isPrimaryTouch(e)) return
            firstTouch = _isPointerType ? e : e.touches[0]
            if (e.touches && e.touches.length === 1 && touch.x2) {
              // Clear out touch movement data if we have it sticking around
              // This can occur if touchcancel doesn't fire due to preventDefault, etc.
              touch.x2 = undefined
              touch.y2 = undefined
            }
            now = Date.now()
            delta = now - (touch.last || now)
            touch.el = $('tagName' in firstTouch.target ?
              firstTouch.target : firstTouch.target.parentNode)
            touchTimeout && clearTimeout(touchTimeout)
            touch.x1 = firstTouch.pageX
            touch.y1 = firstTouch.pageY
            if (delta > 0 && delta <= 250) touch.isDoubleTap = true
            touch.last = now
            longTapTimeout = setTimeout(longTap, longTapDelay)
            // adds the current touch contact for IE gesture recognition
            if (gesture && _isPointerType) gesture.addPointer(e.pointerId)
          })
          .on('touchmove MSPointerMove pointermove', function(e){
            if((_isPointerType = isPointerEventType(e, 'move')) &&
              !isPrimaryTouch(e)) return
            firstTouch = _isPointerType ? e : e.touches[0]
            cancelLongTap()
            touch.x2 = firstTouch.pageX
            touch.y2 = firstTouch.pageY

            deltaX += Math.abs(touch.x1 - touch.x2)
            deltaY += Math.abs(touch.y1 - touch.y2)
          })
          .on('touchend MSPointerUp pointerup', function(e){
            if((_isPointerType = isPointerEventType(e, 'up')) &&
              !isPrimaryTouch(e)) return
            cancelLongTap()

            // swipe
            if ((touch.x2 && Math.abs(touch.x1 - touch.x2) > 30) ||
                (touch.y2 && Math.abs(touch.y1 - touch.y2) > 30))

              swipeTimeout = setTimeout(function() {
                if (touch.el){
                  touch.el.trigger('swipe')
                  touch.el.trigger('swipe' + (swipeDirection(touch.x1, touch.x2, touch.y1, touch.y2)))
                }
                touch = {}
              }, 0)

            // normal tap
            else if ('last' in touch)
              // don't fire tap when delta position changed by more than 30 pixels,
              // for instance when moving to a point and back to origin
              if (deltaX < 30 && deltaY < 30) {
                // delay by one tick so we can cancel the 'tap' event if 'scroll' fires
                // ('tap' fires before 'scroll')
                tapTimeout = setTimeout(function() {

                  // trigger universal 'tap' with the option to cancelTouch()
                  // (cancelTouch cancels processing of single vs double taps for faster 'tap' response)
                  var event = $.Event('tap')
                  event.cancelTouch = cancelAll
                  // [by paper] fix -> "TypeError: 'undefined' is not an object (evaluating 'touch.el.trigger'), when double tap
                  if (touch.el) touch.el.trigger(event)

                  // trigger double tap immediately
                  if (touch.isDoubleTap) {
                    if (touch.el) touch.el.trigger('doubleTap')
                    touch = {}
                  }

                  // trigger single tap after 250ms of inactivity
                  else {
                    touchTimeout = setTimeout(function(){
                      touchTimeout = null
                      if (touch.el) touch.el.trigger('singleTap')
                      touch = {}
                    }, 250)
                  }
                }, 0)
              } else {
                touch = {}
              }
              deltaX = deltaY = 0

          })
          // when the browser window loses focus,
          // for example when a modal dialog is shown,
          // cancel all ongoing events
          .on('touchcancel MSPointerCancel pointercancel', cancelAll)

        // scrolling the window indicates intention of the user
        // to scroll, not tap or swipe, so cancel all ongoing events
        $(window).on('scroll', cancelAll)
      })

      ;['swipe', 'swipeLeft', 'swipeRight', 'swipeUp', 'swipeDown',
        'doubleTap', 'tap', 'singleTap', 'longTap'].forEach(function(eventName){
        $.fn[eventName] = function(callback){ return this.on(eventName, callback) }
      })
    })(Zepto)

$(function(){
    photoCarousel($(".images"),$(".images li"),$(".index ul"),-$(window).width(),$(window).width(),$(".images li").length,3000,1000);

    //图片轮播
    //$ul 容器,$li 元素,$index 索引,left 当前偏移量,width 一次滚动宽度,parentWidth 容器宽度,size 图片数量,interval 循环滚动间隔   0不循环播放,scrolltime 滚动过程时间
    function photoCarousel($ul,$li,$index,left,width,size,interval,scrolltime){
        //move 0:默认左滑右滑；1：停止默认事件，图片跟随手势移动，time 时间大于200毫秒图片跟随手势移动  否则执行默认左滑 右滑事件
        var inner,move=0,time=0,parentWidth=(size+2)*width;
        $ul.width(parentWidth).css("transition-duration","0s").css("-webkit-transition-duration","0s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
        $li.width(width).css("line-height",$ul.height()+"px");
        $li.first().before($li.last().clone());
        $li.last().after($li.first().clone());
        $li.find("img").width(width);
        index();
        //触屏  
        //触屏开始
        $li.bind("touchstart", function(event) {
            if(interval!=0)
                clearInterval(inner);
            move = event.touches[0].pageX;
            time = new Date().getTime();
            //事件停止
            event.preventDefault();
        });

        //触屏结束
        $li.bind("touchend", function(event) {
            if(interval!=0)
                inner = auto();
            if(move !=0){
                $ul.css("transition-duration",(scrolltime/1000.0)+"s").css("-webkit-transition-duration",(scrolltime/1000.0)+"s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
            }
            time = new Date().getTime();
            event.preventDefault();
        }); 

        //触屏移动
        $li.bind("touchmove", function(event) {
            if(interval!=0)
                clearInterval(inner);
            if(new Date().getTime()-time>=200){
                touch = event.touches[0];
                $ul.css("transition-duration","0s").css("-webkit-transition-duration","0s").css("transform", "translate3d("+ (left+touch.pageX-move) +"px,0px,0px)").css("-webkit-transform", "translate3d("+ (left+touch.pageX-move) +"px,0px,0px)");
                event.preventDefault();
            } 
        });

        //左滑
        $li.swipeLeft(function(){
            move = 0;
            left = -left != parentWidth - width ? left -width : 0;
            $ul.css("transition-duration",(scrolltime/1000.0)+"s").css("-webkit-transition-duration",(scrolltime/1000.0)+"s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
            //重置滚动位置
            if(-left == (parentWidth - width)){
                left = -width;
                setTimeout(function(){
                    $ul.css("transition-duration","0s").css("-webkit-transition-duration","0s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
                },scrolltime);
            }
            index();
        })

        //右滑
        $li.swipeRight(function(){
            move = 0;
            left = left !=0 ? left + width : -parentWidth + width;
            $ul.css("transition-duration",(scrolltime/1000.0)+"s").css("-webkit-transition-duration",(scrolltime/1000.0)+"s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
            //重置滚动位置
            if(left ==0){
                left = -(parentWidth - 2*width);
                setTimeout(function(){
                    $ul.css("transition-duration","0s").css("-webkit-transition-duration","0s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
                },scrolltime);
            }
            index();
        })

        //更新图片下方焦点
        function index(){
            $index.children().removeClass("on");
            $index.children().eq(-left/width-1).addClass("on");
            $index.parent().parent().find(".name").text($li.eq(-left/width-1).find("img").attr("alt"));
        }

        function auto() {
            inner = setInterval(function () {
                move = 0;
                left = -left != parentWidth - width ? left -width : 0;
                $ul.css("transition-duration",(scrolltime/1000.0)+"s").css("-webkit-transition-duration",(scrolltime/1000.0)+"s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
                if(-left == (parentWidth - width)){
                    left = -width;
                    setTimeout(function(){
                        $ul.css("transition-duration","0s").css("-webkit-transition-duration","0s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
                    },scrolltime);
                }
                index();
            }, interval);
            return inner;
        }

        //横竖屏切换
        $(window).bind("orientationchange", function(event){
            clearInterval(inner);
            width = $(window).width();
            left=-width;
            parentWidth=(size+2)*width;
            $li.width(width).css("line-height",$ul.height()+"px");
            $li.find("img").width(width);
            $ul.width(parentWidth).css("transition-duration","0s").css("-webkit-transition-duration","0s").css("transform", "translate3d("+ left +"px,0px,0px)").css("-webkit-transform", "translate3d("+ left +"px,0px,0px)");
            index();
            if(interval!=0)
                inner = auto();
        });

        if(interval!=0){
            auto();
        }
    }
})