/**
 * Load controllers for the PID list sharing button
 */
$(document).ready(function() {
    initSharingModal(
        configurePIDListSharingModal, "#pid-sharing",
        "#pid-sharing-modal", "#pid-sharing-link",
        "#pid-sharing-submit"
    );
});

let configurePIDListSharingModal = function() {
    let hasError = false;

    $.ajax({
        url: retrievePidUrl,
        data: {"data_list": JSON.stringify(dataList)},
        type: "POST",
        dataType: 'json',
        success: function(data){
            let pid_url = null;
            if(data["pids"].length === 1) {
                pid_url = data["pids"][0];
            }

            $("#pid-sharing-link").val(
                pid_url===null?"PID not available":pid_url
            );
        },
        error:function(){
            showErrorModal("Error while retrieving persistent query.");
            hasError = true;
        }
    });

    return !hasError;
};