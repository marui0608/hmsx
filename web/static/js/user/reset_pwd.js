;
var user_reset_pwd_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        console.log("reset_pwd eventBind")
        $("#save").click(function(){
            var btn_target = $(this)
            if (btn_target.hasClass("disabled")){
                alert("请求正在进行，请稍后再尝试~~~~")
                return
            }
            console.log("reset_pwd click")
            var old_password_value = $("#old_password").val()
            var new_password_value = $("#new_password").val()
            console.log(old_password_value)
            if (!old_password_value || old_password_value.length < 6){
                alert("请输入符合规范的原密码")
                return false;
            }
            if (!new_password_value || new_password_value.length < 6){
                alert("请输入符合规范的新密码")
                return false;
            }
            btn_target.addClass("disabled")

            $.ajax({
                url:common_ops.buildUrl("/user/reset-pwd"),
                type:"POST",
                data:{
                    "old_password":old_password_value,
                    "new_password":new_password_value,
                },
                dataType:"json",
                success:function(resp){
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
    user_reset_pwd_ops.init()
})