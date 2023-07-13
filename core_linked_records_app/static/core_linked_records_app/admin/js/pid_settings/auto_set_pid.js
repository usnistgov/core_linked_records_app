let $autoSetPidError = $("#auto-set-pid-error");
let $autoSetPidControl = $("#auto-set-pid-control");
let $autoSetPidLabel = $("#auto-set-pid-label");
let $autoSetPidSwitch = $("#auto-set-pid-switch");

let displayError = (message) => {
    $autoSetPidError.show();
    $autoSetPidControl.hide();
    $autoSetPidError.text(message);
}

let setAutoSetPidSwitch = () => {
    $autoSetPidError.hide();
    let autoSetPidValue = $autoSetPidLabel.text().trim();

    if (autoSetPidValue === "True") {
        $autoSetPidSwitch.prop("checked", true);
    } else if (autoSetPidValue === "False") {
        $autoSetPidSwitch.prop("checked", false);
    } else {
        displayError(
            "Invalid value for 'auto_set_pid'. Contact an administrator for more " +
            "information."
        );
    }
};

let initAutoSetPidSwitch = () => {
    $autoSetPidError.hide();
    setAutoSetPidSwitch();
};

let processAutoSetPidClick = (event) => {
    $autoSetPidError.hide();

    $.ajax({
        url: "/pid/rest/settings/",
        data: {
            "auto_set_pid": $autoSetPidSwitch.prop("checked")
        },
        dataType:"json",
        type: "patch",
        success: function(data) {
            $autoSetPidLabel.text(data.auto_set_pid? "True": "False")
            setAutoSetPidSwitch();
        },
        error: function() {
            displayError(
                "An error occured while switching 'auto_set_pid' value. Contact an " +
                "administrator for more information."
            )
        }
    });
}

$( document ).ready(function() {
    initAutoSetPidSwitch();
    $autoSetPidControl.on("change.bootstrapSwitch", processAutoSetPidClick)
});
