# -*- coding: utf-8 -*-

'''
        function removeClass(ele,cls) { 
            if (hasClass(ele,cls)) { 
                    var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)'); 
            ele.className=ele.className.replace(reg,' '); 
            } 
        } 
        
        function addClass(ele, cls) {
            if (!hasClass(elem, cls)) {
                ele.className = ele.className == '' ? cls : ele.className + ' ' + cls;
            }
        }
    
        var Ajax={
          get: function(url, fn) {
            // XMLHttpRequest对象用于在后台与服务器交换数据   
            var xhr = new XMLHttpRequest();            
            xhr.open('GET', url, true);
            xhr.onreadystatechange = function() {
              // readyState == 4说明请求已完成
              if (xhr.readyState == 4 && xhr.status == 200 || xhr.status == 304) { 
                // 从服务器获得数据 
                fn.call(this, xhr.responseText);  
              }
            };
            xhr.send();
          },
          // datat应为'a=a1&b=b1'这种字符串格式，在jq里如果data为对象会自动将对象转成这种字符串格式
          post: function (url, data, fn) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", url, true);
            // 添加http头，发送信息至服务器时内容编码类型
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");  
            xhr.onreadystatechange = function() {
              if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 304)) {
                fn.call(this, xhr.responseText);
              }
            };
            xhr.send(data);
          }
        }
        
        var btn=document.getElementsByClassName("div .subMenu");
        btn.onclick=function(){
        // 取消当前激活状态
            var img = document.getElementsByClassName("active").getElementsByTagName("img");
            var name = img.getAttribute('img-name');
            var src = "../static/image/" + name + ".png";
            img.setAttribute("src", src);
            removeClass(document.getElementByClassName("active"), "active");
            
            addClass(btn, "active")
            var imgs = btn.getElementsByTagName("img");
            for ( var i = 0; i <imgs.length; i++){
                var name = imgs[i].getAttribute('img-name');
                var src = "../static/image/" + name + ".png";
                imgs[i].setAttribute("src", src);
            }
            
            var page = btn.getAttribute('data-src');
            if(page){
                var content = document.getElementById("content");
                content.innerHTML = Ajax.get(page);
            }
            
            var value = btn.getAttribute('value');
            if(value){
                var title = document.getElementById("title");
                title.innerHTML = value;
            }
        }
        
        // 自动点击第一个菜单

        btn[0].onclick();
    
        /*content高度*/
        function initSize() {
            var height = window.screen.height - document.getElementById("title").scrollHeight - document.getElementById("menu").scrollHeight;;
            document.getElementById("content").style.height = height+'px';
        }



        /**    
        $(document).ready(function() {
            
            //点击事件
            $("div .subMenu").click(function () {
                // 取消当前激活状态
                var $img = $(".active>img");
                //返回被选元素的属性值
                var name = $img.attr("img-name");
                var src = "../static/image/" + name + ".png";
                $img.attr("src", src);            
                $(".active").removeClass("active");
    
                // 添加新状态
                $(this).addClass("active");
                //找到所有 div(subMenu) 的子元素(img)
                $img = $(this).children("img");
                name = $img.attr("img-name");
                src = "../static/image/" + name + "_active.png";
                //设置img的属性和值。
                $img.attr("src", src);
                            
                //content根据点击按钮加载不同的html
                var page = $(this).attr("data-src");
                if(page){
                    $("#content").load(page);
                }
                
                var value = $(this).attr("value"); 
                if(value){
                    $("#title").text(value);
                }
            });
    
            // 自动点击第一个菜单
            var index = $("#index").val();
            $("div .subMenu")[index].click();
        });
    
        /*content高度*/
        function initSize() {
            var height = $(window).height() - $("header").height() - $("#description").height() - $("#menu").height();
            $("#content").height(height + "px");
        }
        */
'''