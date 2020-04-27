;   //; 防止打包的时候跟其他文件合并

var user_edit_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        console.log("edit eventBind")
        $(".user_edit_wrap .save").click(function(){
            console.log("edit click")
            var btn_target = $(this)
            if (btn_target.hasClass("disabled")) {
                alert("请求正在进行，请稍后再试")
                return
            }
            var nickname_value = $(".user_edit_wrap input[name=nickname]").val()
            var email_value = $(".user_edit_wrap input[name=email]").val()

            console.log(nickname_value)
            console.log(email_value)
            
            if(!nickname_value || nickname_value.length < 2){
                alert("请输入符合规范的nickname")
                return false;
            }
            if(!email_value || email_value.length < 2){
                alert("请输入符合规范的email")
                return false;
            }
            btn_target.addClass("disabled")
            $.ajax({
                url:common_ops.buildPicUrl("/user/edit"),
                type:"POST",
                data:{
                    "nickname":nickname_value,
                    "email":email_value,
                },
                dataType:"json",
                success:function(resp){
                    // common_ops.alert("编辑成功")
                    alert(resp.msg)
                    console.log(resp)
                    btn_target.removeClass("disabled")
                },
                error:function(error){
                    console.log(error)
                }
            })
        })
    }
}

$(document).ready(function(){
    user_edit_ops.init()
})