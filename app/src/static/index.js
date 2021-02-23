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

function onSelectProfile(profile_name)
{
    if ($(`#${profile_name}-input`).is(":checked"))
    {
        $(`#divTableRow_${profile_name}`).show("slow")
    } else {
        $(`#divTableRow_${profile_name}`).hide("slow")
    }
}

function loadConfiguredProfiles() {

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load profiles`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    function onSuccess(data) {
        // prepare html for images
        profilesHTML = ""
        imagesHTML = ""
        for (profile of data.profiles) {
            imagesHTML += `<div id="image-stats-${profile.username}-div" class="profile-stats-images"></div>`
            
            profilesHTML += `<input type="checkbox" name="profiles" id="${profile.username}-input" onClick="onSelectProfile('${profile.username}')">`
            profilesHTML += `<label for="${profile.username}-input" >`  
            profilesHTML += `${profile.username}`
            profilesHTML += `</label>`
        }
        $(`#profile-stats-images-div`).html(imagesHTML)

        // prepare html for sessions table
        sessionsHTML = `<div class="divTableHeading">
                            <div class="divTableCell">Name</div>
                            <div class="divTableCell">Game Mode</div>
                            <div class="divTableCell">Matches</div>
                            <div class="divTableCell">Kills</div>
                            <div class="divTableCell">Kill ratio</div>
                            <div class="divTableCell">Eskores</div>
                            <div class="divTableCell">Eskores ratio</div>
                            <div class="divTableCell">trnRating diff</div>
                            <div class="divTableCell">Best Match Kills</div>
                        </div>`
        $('#sessions-info-div').html(sessionsHTML)

        i=0
        for (profile of data.profiles) {
            loadSessionsOfProfile(profile.username, i);
            i++;
            //loadImagesOfProfile(profile.username);
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

function loadSessionsOfProfile(profile_name, index) {
    function onSuccess(data) {
        sessionsHTML = $('#sessions-info-div').html()
        sessionsHTML += `<div class="divTableBody"><div class="divTableRow" id="divTableRow_${profile_name}">`
        sessionsHTML += `<div class="divTableCell">${data.session[0].username}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].game_mode}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].total_matches}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].total_kills}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].kill_ratio.toFixed(2)}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].total_eskores}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].eskores_ratio.toFixed(2)}</div>`
        sessionsHTML += `<div class="divTableCell">${(data.session[0].last_trn_rating - data.session[0].first_trn_rating).toFixed(2)}</div>`
        sessionsHTML += `<div class="divTableCell">${data.session[0].best_match}</div>`
        sessionsHTML += `</div></div>`


        $('#sessions-info-div').html(sessionsHTML)
        //$(`#${profile_name}-input`).prop('checked', false);
        if (index > 0) {
            $(`#divTableRow_${profile_name}`).hide()
        }
    }

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load sessions of ${profile_name}`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    $.get({
        url: `api/v1/${profile_name}/session/last?n=3`,
        dataType: 'json',
        error: onError,
        success: onSuccess
    })
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
