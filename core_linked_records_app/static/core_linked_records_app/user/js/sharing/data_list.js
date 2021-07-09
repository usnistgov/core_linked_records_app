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

let configurePIDDataSharingModal = function(button_clicked) {
    return configureGenericPIDSharingModal(
        retrieveDataPidUrl,
        {
            "data_id": $(button_clicked).closest("tr").attr("objectid")
        }
    )
};