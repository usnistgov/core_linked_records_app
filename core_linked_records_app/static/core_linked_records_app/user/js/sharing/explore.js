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
    let hasError = false;
    let dataSourceIndex = $(".tab-pane.active").attr("id").replace("results_", "");
    let queryId = $("#query_id").text();

    $.ajax({
        url: retrieveListPidUrl,
        data: {
            "query_id": queryId,
            "data_source_index": dataSourceIndex
        },
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
        error: function(returnState) {
            let errorMessage = "responseJSON" in returnState?
                returnState.responseJSON["error"]: "";

            showErrorModal(
                "Error while retrieving list of PIDs. " + errorMessage
            );
            hasError = true;
        }
    });

    return !hasError;
};

