/**
 * Load controllers for the PID list sharing button
 */
$(document).ready(function() {
    initSharingModal(
        configurePIDListSharingModal, "#pid-list-sharing",
        "#pid-list-sharing-modal", "#pid-list-sharing-link",
        "#pid-list-sharing-submit"
    );
});

let configurePIDListSharingModal = function() {
    let dataList = [];
    let $linkList = $(".exporter-checkbox");
    let hasError = false;

    for(const link of $linkList) {
        dataList.push($(link).attr("value").split("=")[1]);
    }

    if(dataList.length===0) {
        $("#pid-list-sharing-link").val("No data available");
        return !hasError;
    }

    $.ajax({
        url: retrievePidUrl,
        data: {"data_list": JSON.stringify(dataList)},
        type: "POST",
        dataType: 'json',
        async: false,
        success: function(data){
            let sharing_link_value = "";
            for(const pid of data["pids"]) {
                sharing_link_value += pid + "\n";
            }
            $("#pid-list-sharing-link").val(sharing_link_value);
        },
        error:function(){
            showErrorModal("Error while retrieving list of PIDs.");
            hasError = true;
        }
    });

    return !hasError;
};

