//执行购物车飞行函数
$(function () {
    var offset = $("#end").offset();
    $("#add_cart").click(function (event) {
        var e = event || window.event;
        var addcar = $(this);
        var img = addcar.parent().parent().parent().find('img').attr('src');
        var flyer = $('<img class="u-flyer" src="' + img + '">');
        flyer.fly({
            start: {
                left: e.clientX, //点击位置获取
                top: e.clientY,
            },
            end: {
                left: offset.left + 10,
                top: offset.top + 10,
                width: 0,
                height: 0
            },
            speed: 0.8,
            onEnd: function () {
                this.destory();
                $.ajax({
                    url: '/add_cart/',
                    type: 'GET',
                    dataType: 'json',
                    data: {'good_id': $('.add_cart').attr('value'), 'good_count': $('.num_show').val()}
                }).done(function (data) {
                        //获取后台的json数据
                        if(data.login=='no'){
                            alert("请先登录！")
                            window.location.href='/login/' //没有登录就重定向
                        }else {
                            $('#show_count').html(data.number)
                        }
                    }
                ).fail(function () {
                    alert('服务器超时，请重试！');
                });
            }
        });
    });
});