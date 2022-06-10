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

            }),
            contentType: "application/json",
            success: function(response){
                alert('預測結果如下');
                $("#num_img").attr("src", "assets/img/num_" + response.index + ".png");
                $("#num_img").show();
                $("#img").show();
                $("#img").attr("value", response.index);
                $("#predictNum").text(response.predictNum);
                /*if(response.msg != "" && response.msg != null){
                    Swal.fire({//登入失敗
                        title: 'Error!',
                        text: response.msg,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                }else{//登入成功
                    localStorage.token = response.access_token;
                    localStorage.name = response.name;
                    Swal.fire({
                        title: 'Correct!',
                        text: 'Jump to upload page',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        window.location.href="../index.html"
                    })
                }*/
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
                    "index" : tempValue
                }),
                contentType: "application/json"
            });
        }
    })
})