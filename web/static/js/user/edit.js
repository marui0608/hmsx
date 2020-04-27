;   //; 防止打包的时候跟其他文件合并

var user_edit_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        console.log("edit eventBind")
        $(".user_edit_wrap .save").click(function(){
            console.log("edit click")
        })
    }
}

$(document).ready(function(){
    user_edit_ops.init()
})