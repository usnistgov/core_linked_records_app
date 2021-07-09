let configureGenericPIDSharingModal = function(retrievPidUrl, pidData) {
    $("#pid-sharing-submit").attr("disabled", false)

    $.ajax({
        url: retrievPidUrl,
        data: pidData,
        type: "GET",
        dataType: 'json',
        success: function(data){
            $("#pid-sharing-link").val(
                data["pid"]===null?"PID not available":data["pid"]
            );

            if(data["pid"]===null) {
                $("#pid-sharing-submit").attr("disabled", true)
            }
        },
        error:function(){
            $("#pid-sharing-link").val(
                "PID not available"
            );
            $("#pid-sharing-submit").attr("disabled", true)
        }
    });

    return true;
};