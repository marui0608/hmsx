;
var account_set_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        console.log("account eventBind")
        $(".wrap_account_set .save").click(function(){
            console.log("account click")
            var nickname = $(".wrap_account_set input[name=nickname]").val();
            var mobile = $(".wrap_account_set input[name=mobile]").val();
            var email = $(".wrap_account_set input[name=email]").val();
            var login_name = $(".wrap_account_set input[name=login_name]").val();
            var login_pwd = $(".wrap_account_set input[name=login_pwd]").val();

            //前端校检
            if (!nickname || nickname.length < 1){
                alert("请输入符合规范的nickname")
                return false
            }
            if (!mobile || mobile.length < 1){
                alert("请输入符合规范的mobile")
                return false
            }
            if (!email || email.length < 1){
                alert("请输入符合规范的email")
                return false
            }
            if (!login_name || login_name.length < 1){
                alert("请输入符合规范的login_name")
                return false
            }
            if (!login_pwd || login_pwd.length < 1){
                alert("请输入符合规范的login_pwd")
                return false
            }
            id = $(".wrap_account_set input[name=id]").val()
            var data = {
                id:id,
                nickname:nickname,
                mobile:mobile,
                email:email,
                login_name:login_name,
                login_pwd:login_pwd,
            }

            $.ajax({
                url:common_ops.buildUrl("/account/set"),
                type:"POST",
                data:data,
                dataType:"json",
                success:function(resp){
                    if(resp.code == 200){
                        window.location.href = common_ops.buildUrl("/account/index")
                    }
                    alert(resp.msg)
                    console.log(resp)
                },
                error:function(error){
                    console.log(error)
                }
            })
        })
    }
}


$(document).ready(function(){
    account_set_ops.init()
})