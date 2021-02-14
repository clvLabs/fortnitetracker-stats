window.onload = function() {
    setupUI();
    loadConfiguredProfiles();
    loadBackground();
};

function loadBackground() {  
    $('#bg_canvas').drawLine({
        strokeStyle: '#333',
        strokeWidth: 10,
        x1: 100, y1: 50,
        x2: 100, y2: 150,
        x3: 200, y3: 100,
        x4: 150, y4: 200
      });

    $('.mainDiv').css('background-image', `url("${$('#bg_canvas').getCanvasImage()}")`);
}

function setupUI() {
    $( "#sample-button" ).click(onSampleButton);
    $( ".profile-button" ).click(onSampleButton);
}

function onSampleButton() {
    toast("Sample button pressed", TOAST_OK);
}

function onActivateProfile(profile_name)
{
    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load matches for ${profile_name}`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    function onSuccess(data)
    {
        if ($(`#${profile_name}-input`).is(":checked"))
        {
            profile_activeHTML = `<div id=${profile_name}-last-match` 
            profile_activeHTML += `class="profile_item"`
            profile_activeHTML += `title="${profile_name}">KILLS: ${data.match.kills}`
            profile_activeHTML += `</div>`
            
            $('#profile-info-div').html(profile_activeHTML)
            $('#profile-info-div').show("slow")
        } else {
            profile_activeHTML = `inactive` 
            $('#profile-info-div').hide("slow")
        }
    }
    
    $.get({
        url: `api/v1/${profile_name}/match/last`,
        dataType: 'json',
        error: onError,
        success: onSuccess
      });
}

function loadConfiguredProfiles() {

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load profiles`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    function onSuccess(data) {
        profilesHTML = ""
        imagesHTML = ""
        for (profile of data.profiles) {
            imagesHTML += `<div id="image-stats-${profile.username}-div" class="profile-stats-images"></div>`
            
            profilesHTML += `<input type="checkbox" name="profiles" id="${profile.username}-input" onClick="onActivateProfile('${profile.username}')">`
            profilesHTML += `<label for="${profile.username}-input" >`  
            profilesHTML += `${profile.username}`
            profilesHTML += `</label>`
        }
        $(`#profile-stats-images-div`).html(imagesHTML)

        for (profile of data.profiles) {
            loadImagesOfProfile(profile.username);
        }
        
        $('#profiles-div').html(profilesHTML)
        
    }

    $.get({
      url: 'api/v1/profiles',
      dataType: 'json',
      error: onError,
      success: onSuccess
    });
}

function loadImagesOfProfile(profile_name) {
    function onSuccess(data) {
        imageProfileHTML = `<img src="${data.profile.stats_image}" width="380">`
        $(`#image-stats-${profile_name}-div`).html(imageProfileHTML)
    }

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load picture`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    $.get({
        url: `api/v1/${profile_name}/profile`,
        dataType: 'json',
        error: onError,
        success: onSuccess
    });
}
