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
        ajaxData = {"oai_data_id": oaiDataId};
    }

    $.ajax({
        url: retrieveDataPidUrl,
        data: ajaxData,
        type: "POST",
        dataType: 'json',
        success: function(data){
            $("#pid-sharing-link").val(
                data["pid"]===null?"PID not available":data["pid"]
            );
        },
        error:function(){
            showErrorModal("Error while retrieving persistent query.");
            hasError = true;
        }
    });

    return !hasError;
};