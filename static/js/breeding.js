$(function(){

	//alert
	function ltalert(msg){
	    if(!msg){
	        return;
	    }	
		if($(".ltalert").length == 0){
			$(".lg-at").append('<div class="ltalert"><div class="ltalertbg"></div><div class="ltalerttxt">'+ msg +'</div></div>');
			setTimeout(function(){$(".ltalert").remove();},2500);
		}
	}
	    
    $(".getcode").removeClass("unclick");
    
   //获取验证码
	$(".getcode").click(function(){
		var phone = $.trim($("#account").val());
		if(!$(this).hasClass("unclick")){
			$(this).addClass("unclick");

			$.ajax({
				url: '/send_code',
				dataType : "text",
				type: 'POST',
				data:{
					account:phone,
				},
				success: function(data){
					if(typeof data == "string"){
						data = $.parseJSON(data);
					}
					if(data.code == 0){
						sendDelayTime($(".getcode"));
					}else{
						ltalert(data.message);
						sendBack($(".getcode"));
					}				    	
				},
				error: function(){
					sendBack($(".getcode"));
					ltalert("请求超时，请重试");
				}
			});
		}
	});

	//倒计时
	var sendDelayTime_s = 60;
	var sendDelay_t;
	function sendDelayTime($obj){
		var $that = $obj;
		(function loop($that){
			var $this = $that;
			sendDelayTime_s--;
			if(sendDelayTime_s == 0){
				sendDelayTime_s = 60;
				$this.removeClass("unclick");
				$this.text("重新获取");
				return false;
			}
			$this.text("已发送(" + sendDelayTime_s + "秒)");
			sendDelay_t = setTimeout(function(){loop($obj)},1000);
		})($obj);
		
	}
	
	//倒计时 还原
	function sendBack($obj){
		var $this = $obj;
		try{
			clearTimeout(sendDelay_t);
		}catch(e){}
		
		$this.text("重新获取");
		$this.removeClass("unclick");
		sendDelayTime_s = 60;
	}

    //购买
	$("#buy").click(function(){
		var goods_id = $.trim($("#goods_id").val());
		var num = $.trim($("#num").val());
		var address_id = $.trim($("#address_id").val());
		
        $.post('/goods/buy',{
			goods_id:goods_id,
			num:num,
			address_id:address_id,
        }).then(function(data) {
			if(typeof data == "string"){
				data = $.parseJSON(data);
			}
            if (data.code == 0) {
                // 后台返回订单信息
                var wePayData = {
                    appId: data.app_id,
                    nonceStr: data.nonce_str,
                    package: data.package,
                    paySign: data.pay_sign,
                    signType: "MD5",
                    timeStamp: data.timestamp
                };
                var order_code = data.order_code;

                window.jsApiCall = function() {
                    WeixinJSBridge.invoke(
                        'getBrandWCPayRequest',
                        wePayData,
                        function(res) {
                            WeixinJSBridge.log(res.err_msg);
                            // alert(res.err_code + res.err_desc + res.err_msg);
                            // alert(res.err_msg)
                            if (res.err_msg == 'get_brand_wcpay_request:ok') {
                                $.get('/pay/result', {order_code: order_code}, function(data) {
									if(typeof data == "string"){
										data = $.parseJSON(data);
									}
                                     if (data.code == 0) {
                                         window.location.href = "/user/order_list";
                                     } else {
                                         alert(data.message);
                                     }
                                });
                            } else {
                                // 其他支付异常微信有显示消息
                                alert(res.err_msg);
                            }
                        }
                    );
                }

                window.callpay = function() {
                    if (typeof WeixinJSBridge == "undefined") {
                        if (document.addEventListener) {
                            document.addEventListener('WeixinJSBridgeReady', jsApiCall, false);
                        } else if (document.attachEvent) {
                            document.attachEvent('WeixinJSBridgeReady', jsApiCall);
                            document.attachEvent('onWeixinJSBridgeReady', jsApiCall);
                        }
                    } else {
                        jsApiCall();
                    }
                }

                // 发起支付
                window.callpay();
            } else {
                alert(data.message);
            }
        }, function(data) {
            alert(data.message);
        });
	});
		
});