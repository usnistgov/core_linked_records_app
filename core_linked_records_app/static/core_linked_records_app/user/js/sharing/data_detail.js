/**
 * Load controllers for the PID list sharing button
 */
$(document).ready(function() {
    initSharingModal(
        configurePIDDataSharingModal, "#pid-sharing",
        "#pid-sharing-modal", "#pid-sharing-link",
        "#pid-sharing-submit"
    );
});

let configurePIDDataSharingModal = function() {
    let hasError = false;
    let ajaxData = {"data_id": dataId};

    if(dataId === "") {
        if (oaiDataId !== "") {
            ajaxData = {"oai_data_id": oaiDataId};
        } else {
            ajaxData = {
                "fede_data_id": fedeDataId,
                "fede_origin": window.location.search.substring(1)
            };
        }
    }

    $.ajax({
        url: retrieveDataPidUrl,
        data: ajaxData,
        type: "GET",
        dataType: 'json',
        success: function(data){
            $("#pid-sharing-link").val(
                data["pid"]===null?"PID not available":data["pid"]
            );
        },
        error:function(){
            $("#pid-sharing-link").val(
                "PID not available"
            );
            $("#pid-sharing-submit").attr("disabled", true)
            hasError = true;
        }
    });

    return !hasError;
};