$("#login-btn").click(function () {
    $("span.help-block").text('');
    $("form>.form-group").removeClass('has-error');
    if ($("#id_auto_login").is(':checked')){
        auto_login = 1
    }else {
        auto_login = 0
    }
    $.ajax({
    url: "/login/",
    type: "post",
    dataType: "json",
    data: {
        username: $('#id_username').val(),
        password: $('#id_password').val(),
        "csrfmiddlewaretoken": $("input:hidden").val(),
        auto_login: auto_login
    },
    success: function (data) {

        // 用户登陆成功
        if (data["success"]) {
            var redirect = localStorage.getItem("redirect");                // 从localStorage中获取路径
            if (localStorage.getItem("target_url") && redirect==='OK'){
                window.location.href = localStorage.getItem("target_url");  // 登陆后跳转到登陆前的页面
                localStorage.setItem("redirect", "NO")                      // 跳转之后再次设置为NO，相当于一个"开关"
            }else {
                window.location.href = "/home/";                            // 跳转至博客系统主页
            }
        }

        // 用户登陆失败，渲染错误信息
        if (data["form_errors"]) {
            for (var key in data["form_errors"]) {
                $("#" + key).text(data["form_errors"][key]);
                $("#" + key).parent().parent().addClass('has-error');
            }
        }
    }
})
});



