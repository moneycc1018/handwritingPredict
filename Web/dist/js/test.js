//import CONFIG from "../../js/config.json" assert { type: "json" };

//var userHost = CONFIG.userHost;
//var userPort = CONFIG.userPort;

$(function(){
    //預測
    $("#tryBtn").on("click",function(){
        var tempValue = $("#img").attr("value");//前一張圖index
        $("#num_img_").attr("src", "");
        $("#img").hide();
        $("#predictNum").empty();

        $.ajax({
            type: "post",
            url: "http://0.0.0.0:8888/execute",
            //url: userHost + ":" + userPort + "/login",
            dataType: "json",
            data: JSON.stringify({
                "name": "Money"
            }),
            contentType: "application/json",
            success: function(response){
                $("#num_img").attr("src", "assets/img/num_" + response.index + ".png");
                $("#num_img").show();
                $("#img").show();
                $("#img").attr("value", response.index);
                $("#predictNum").text(response.predictNum);
                //預測成功
                if(response.predictResult == "1"){
                    Swal.fire({
                        title: '預測成功!',
                        text: '預測正確',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    })
                //預測失敗
                }else if(response.predictResult == "0"){
                    Swal.fire({
                        title: '預測失敗!',
                        text: '失敗為成功之母',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                }
            }/*,
            error: function(){
                Swal.fire({
                    title: 'Error!',
                    text: 'Upload error!',
                    icon: 'error',
                    confirmButtonText: 'OK'
                })
            }*/
        });
        
        if(tempValue != ""){
            $.ajax({
                type: "post",
                url: "http://0.0.0.0:8888/deleteImage",
                //url: userHost + ":" + userPort + "/login",
                dataType: "json",
                data: JSON.stringify({
                    "index": tempValue
                }),
                contentType: "application/json"
            });
        }
    })
})