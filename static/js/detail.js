$(function () {
    setTotal();

    $("#number").blur(function () {
        var t = $("#number")
        var num = parseInt(t.val())
        if (num < 1) { //小于0
            alert('购买数量必须大于0');
            t.val(1)
        }
        var left = $("#left").html();
        if (t.val() > parseInt(left)) {
            alert('对不起，库存不足！');
            t.val(parseInt(left))
        }
        $(".num_show").trigger("change");
        setTotal()

    })

    // 点击增加数量按键
    $(".add").click(function () {
        var t = $(this).parent().find('input[class*="num_show"]');
        var left = $("#left").html();
        if (parseInt(t.val()) < parseInt(left)) {
            t.val(parseInt(t.val()) + 1);      // 对数值加1操作
            $(".num_show").trigger("change"); // 调整点击购买button的href
            setTotal(); //设置总价
        }else {
            alert('已经到最大了！')
        }
    });

    // 点击减少数量按键
    $(".minus").click(function () {
        $(".num_show").trigger("change");
        var t = $(this).parent().find('input[class*="num_show"]');
        t.val(parseInt(t.val()) - 1)
        if (parseInt(t.val() - 1) < 1) { // 减1小于0 就设置为1
            t.val(1);
        }
        setTotal();
        $(".num_show").trigger("change");
    });

    // 设置总价
    function setTotal() {
        var s = 0;
        s = (parseInt($(".num_show").val()) * parseFloat($(".show_pirze > em").html())).toFixed(2);
        $(".total").children(":first").html(s);
    }

    // 当数字变化触发事件，数字一遍 btn的href会自动拼接get请求，用于后面点击购买
    $('.num_show').change(function () {
        $('.buy_btn').attr({href: $('.buy_btn').attr('href').split('?')[0] + '?id=' + $('.add_cart').attr('value') + '&count=' + $('.num_show').val()})
    })


})