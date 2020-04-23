;
var user_login_ops = {
    init:function(){
        this.eventBind()
        console.log("eventBind")
    },
    eventBind:function(){
        $(".login_wrap .do-login").click(function(){
            // btn
            var btn_target = $(this)
            if (btn_target.hasClass("disabled")){
                alert("请不要重复提交")
                return;
            }
            var login_name = $(".login_wrap input[name=login_name]").val()
            var login_pwd = $(".login_wrap input[name=login_pwd]").val()
            
            // console.log(login_name)
            // console.log(login_pwd)
            
        })
    }
}
$(document).ready(function(){
    user_login_ops.init()
})