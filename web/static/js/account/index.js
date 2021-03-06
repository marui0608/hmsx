;
var account_index_ops = {
    init:function(){
        this.eventBind()
    },
    eventBind:function(){
        $(".wrap_search .search").click(function(){
            $(".wrap_search").submit()
        })
        var that = this;
        $(".remove").click(function(){
            id = $(this).attr("data")
            console.log(id)
            that.myAjax(id,"remove")
            // $.ajax({
            //     url:common_ops.buildUrl("/account/remove-or-recover"),
            //     type:"POST",
            //     data:{
            //         "id":id,
            //         "acts":"remove"
            //     },
            //     dataType:"json",
            //     success:function(resp){
            //         if(resp.code == 200){
            //             window.location.href = common_ops.buildUrl("/account/index")
            //         }
            //         alert(resp.msg)
            //         console.log(resp)
            //     },
            //     error:function(error){
            //         console.log(error)
            //     }
            // })
        })

        $(".recover").click(function(){
            id = $(this).attr("data")
            console.log(id)
            that.myAjax(id,"recover")
            // $.ajax({
            //     url:common_ops.buildUrl("/account/remove-or-recover"),
            //     type:"POST",
            //     data:{
            //         "id":id,
            //         "acts":"recover"
            //     },
            //     dataType:"json",
            //     success:function(resp){
            //         if(resp.code == 200){
            //             window.location.href = common_ops.buildUrl("/account/index")
            //         }
            //         alert(resp.msg)
            //         console.log(resp)
            //     },
            //     error:function(error){
            //         console.log(error)
            //     }
            // })
        })
    },

    // 封装ajax操作
    myAjax:function(id,acts){
        $.ajax({
            url:common_ops.buildUrl("/account/remove-or-recover"),
            type:"POST",
            data:{
                "id":id,
                "acts":acts
            },
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
    }
}

$(document).ready(function(){
    account_index_ops.init()
})