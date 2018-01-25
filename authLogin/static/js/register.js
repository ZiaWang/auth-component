// 前后端Ajax数据交互
$(".btn").click(function () {
        // 每次提交初始化页面错误信息
        $("form span").text('');
        $("div.form-group").removeClass('has-error');

        // 封装表单数据到formData对象中
        var formData = new FormData();
        formData.append("email", $('#id_email').val());
        formData.append("telephone", $('#id_telephone').val());
        formData.append("username", $('#id_username').val());
        formData.append("nick_name", $('#id_nick_name').val());
        formData.append("password", $('#id_password').val());
        formData.append("confirm_password", $('#id_confirm_password').val());
        formData.append("csrfmiddlewaretoken", $('input:hidden').val());
        formData.append("avatar", $('input:file')[0].files[0]);

        // Ajax
        $.ajax({
            url: '/register/',
            type: 'POST',
            data: formData,
            contentType: false,         // 不要忘了这两个参数
            processData: false,
            success: function (data) {
                data = JSON.parse(data);

                // 验证成功
                if (data["success"]){
                    window.location.href = data["location_href"];
                }

                // 验证失败
                if (data["form_errors"]) {
                    for (var key in data["form_errors"]) {
                        for (var key in data["form_errors"]) {

                            // 渲染验证错误信息
                            if (key == "__all__") {
                                $("#confirm_password").text(data["form_errors"][key]);
                                $("#confirm_password").parent().parent().addClass('has-error');
                            } else {
                                $("#" + key).text(data["form_errors"][key]);                // 注意将span标签的id值设置成key，这样可以方便渲染错误信息
                                $("#" + key).parent().parent().addClass('has-error');
                            }
                        }
                    }
                }
            }
        })
    });



// 图片预览
$("input:file").change(function () {
   $("#img_avatar")[0].src = window.URL.createObjectURL($(this)[0].files[0]);
});

