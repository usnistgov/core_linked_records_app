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

    $.ajax({
        url: retrieveDataPidUrl,
        data: {"data_id": dataId},
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