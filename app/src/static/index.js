window.onload = function() {
    setupUI();
    loadConfiguredProfiles();
};

function setupUI() {
    $( "#sample-button" ).click(onSampleButton);
}

function onSampleButton() {
    toast("Sample button pressed", TOAST_OK);
}

function loadConfiguredProfiles() {

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load profiles`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    function onSuccess(data) {
        profilesHTML = "<ul>"
        for (profile of data.profiles) {
            profilesHTML += `<li>${profile.username}</li>`
        }
        profilesHTML += "</ul>"
        $('#profiles-div').html(profilesHTML)
    }

    $.get({
      url: 'api/v1/profiles',
      dataType: 'json',
      error: onError,
      success: onSuccess
    });
}
