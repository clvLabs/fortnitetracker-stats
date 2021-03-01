var session_num = 0;

window.onload = function() {
    //setupUI();
    loadConfiguredProfiles(true);
    loadBackground();
    startTimer();
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

// function setupUI() {
//     $( "#sample-button" ).click(onSampleButton);
//     $( ".profile-button" ).click(onSampleButton);
// }

// function onSampleButton() {
//     toast("Sample button pressed", TOAST_OK);
// }

function onSelectProfile(profile_name)
{
    if ($(`#${profile_name}-input`).is(":checked"))
    {
        $(`.${profile_name}_session_${session_num}`).show("slow")
        
        $(`#divTable_${profile_name}`).show("slow");
    } else {
        $(`.${profile_name}_session_${session_num}`).hide("slow")
        $(`#divTable_${profile_name}`).hide("slow");
    }
}

function loadConfiguredProfiles(is_first_load) {

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load profiles`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    function onSuccess(data) {
        if (is_first_load) {
            // prepare html for images
            profilesHTML = ""
            imagesHTML = ""
            for (profile of data.profiles) {
                _username = profile.username.replace(/ /g, "")
                imagesHTML += `<div id="image-stats-${_username}-div" class="profile-stats-images"></div>`
                
                profilesHTML += `<input type="checkbox" name="profiles" id="${_username}-input" onClick="onSelectProfile('${_username}')">`
                profilesHTML += `<label for="${_username}-input" >`  
                profilesHTML += `${profile.username}`
                profilesHTML += `</label>`
            }
            $(`#profile-stats-images-div`).html(imagesHTML)
            $('#profiles-div').html(profilesHTML)
    
        }
        // prepare html for sessions table (clean in reloads)
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
        // prepare html for matches table (clean in reloads)
        matchesHTML = ``
        $('#matches-info-div').html(matchesHTML)

        i=0
        for (profile of data.profiles) {
            loadSessionsOfProfile(profile.username, i, is_first_load, 0);
            i++;
            //loadImagesOfProfile(profile.username);
        }
    }

    $.get({
      url: 'api/v1/profiles',
      dataType: 'json',
      error: onError,
      success: onSuccess
    });
}

function loadSessionsOfProfile(profile_name, index, is_first_load) {
    function onSuccess(data) {
        _username = profile_name.replace(/ /g, "");
        lastSessionHTML = getLastSessionTable(data);
        matchesHTML = getLastMatchesTable(data);
        
        $('#sessions-info-div').html(lastSessionHTML);
        $('#matches-info-div').html(matchesHTML);
        
        if (is_first_load) {
            if (index > 0) {
                $(`.${_username}_session_0`).hide()
                $(`#divTable_${_username}`).hide();
            } else {
                $(`#${_username}-input`).prop('checked', true);
            }
        } else {
            if (!$(`#${_username}-input`).is(":checked")) {
                $(`.${_username}_session_0`).hide()
                $(`#divTable_${_username}`).hide();
            }
        }
        
        for (i=1;i<10;i++) {
            $(`.${_username}_session_${i}`).hide();
            $(`#divTableRow_${_username}_session_${i}`).hide();
        }
    }

    function onError(xhr, ajaxOptions, thrownError) {
        toast(`Can't load sessions of ${profile_name}`, TOAST_ERROR);
        console.log(xhr.status);
        console.log(thrownError);
    }

    $.get({
        url: `api/v1/${profile_name}/session/last?n=10`,
        dataType: 'json',
        error: onError,
        success: onSuccess
    })
}

// function loadImagesOfProfile(profile_name) {
//     function onSuccess(data) {
//         imageProfileHTML = `<img src="${data.profile.stats_image}" width="380">`
//         $(`#image-stats-${profile_name}-div`).html(imageProfileHTML)
//     }

//     function onError(xhr, ajaxOptions, thrownError) {
//         toast(`Can't load picture`, TOAST_ERROR);
//         console.log(xhr.status);
//         console.log(thrownError);
//     }

//     $.get({
//         url: `api/v1/${profile_name}/profile`,
//         dataType: 'json',
//         error: onError,
//         success: onSuccess
//     });
// }

function startTimer() {
    var count = 180;
    var counter = setInterval(timer, 1000);

    function timer() {
        count--;
        if (count <= 0) {
            //clearInterval(counter);
            count = 180;
            //timer is over
            loadConfiguredProfiles(false);
            return;
        }
        // mostramos el tiempo que queda hasta el siguiente refresco
        //$(`#matches-info-div`).html(count)
    }
}

function getLastSessionTable(profiles_data) {
    sessionsHTML = $('#sessions-info-div').html();
    sessionsHTML += `<div class="divTableBody">`
    for (i=0; i < 10; i++) {
        sessionsHTML += `<div class="divTableRow ${profiles_data.session[session_num].username.replace(/ /g, "")}_session_${i}">`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].username}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].game_mode}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].total_matches}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].total_kills}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].kill_ratio.toFixed(2)}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].total_eskores}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].eskores_ratio.toFixed(2)}</div>`;
        sessionsHTML += `<div class="divTableCell">${(profiles_data.session[i].last_trn_rating - profiles_data.session[i].first_trn_rating).toFixed(2)}</div>`;
        sessionsHTML += `<div class="divTableCell">${profiles_data.session[i].best_match}</div>`;
        sessionsHTML += `</div>`;
    }
    sessionsHTML += `</div>`;
    return sessionsHTML;
}

function getLastMatchesTable(profiles_data) {
    matchesHTML = $('#matches-info-div').html();
    matchesHTML += `<div id="divTable_${profiles_data.session[0].username.replace(/ /g, "")}">`
    matchesHTML += `<div class="divTitleTable">${profiles_data.session[0].username}
                    <a href="#" class="prev_page_btn" onClick='onChangeSessionInfo("${profiles_data.session[0].username.replace(/ /g, "")}", "next")'><<</a>
                    <a href="#" class="next_page_btn" onClick='onChangeSessionInfo("${profiles_data.session[0].username.replace(/ /g, "")}", "prev")'>>></a>
                    </div>`
    matchesHTML += `<div class="divTable steelBlueCols" >
                    <div class="divTableRow divTableSemiHeading">
                    <div class="divTableCell"></div>
                    <div class="divTableCell"></div>
                    <div class="divTableCell">Mode</div>
                    <div class="divTableCell">Matches</div>
                    <div class="divTableCell">Kills</div>
                    <div class="divTableCell">Eskores</div>
                    <div class="divTableCell">TrnRating</div>
                    </div>
                    <div class="divTableBody">`
    num_sess = 0
    for (session of profiles_data.session) {
        //matchesHTML += `<div class="divTableBody" id=${profiles_data.session[0].username.replace(/ /g, "")}_session_${num_sess}">`
        for (entry of session.entries) {
            var match_date = new Date(entry.date_collected)
            var diff = getDifferenceBetweenDates( match_date);
            matchesHTML += `<div class="divTableRow ${profiles_data.session[0].username.replace(/ /g, "")}_session_${num_sess}">`;
            matchesHTML += `<div class="divTableCell ${entry.top_display}">${entry.top_display}</div>`;
            matchesHTML += `<div class="divTableCell"> ${diff}</div>`;
            matchesHTML += `<div class="divTableCell">${entry.game_mode}</div>`;
            matchesHTML += `<div class="divTableCell">${entry.matches}</div>`;
            matchesHTML += `<div class="divTableCell">${entry.kills}</div>`;
            matchesHTML += `<div class="divTableCell">${entry.eskores}</div>`;
            matchesHTML += `<div class="divTableCell">${entry.trn_Rating}</div>`;
            matchesHTML += `</div>`
        }
        //matchesHTML += `</div>`
        num_sess++;
    }
    matchesHTML += `</div></div></div>`;
    return matchesHTML;
}

function getDifferenceBetweenDates(match_date) {
    
    ahora = Date.now()
    diff = ahora - match_date;
    if (diff < 60*1000) {
        truncated = (diff/(60*1000)) | 0
        retval = truncated + "seconds ago"
    } else if (diff < 60*60*1000) {
        truncated = (diff/(60*1000)) | 0
        retval = truncated + " minutes ago"
    } else if (diff < 24*60*60*1000) {
        truncated = (diff/(60*60*1000)) | 0
        retval = truncated + " hours ago"
    } else {
        truncated = (diff/(24*60*60*1000)) | 0
        retval = truncated + " days ago"
    }
    return retval;
}

function onChangeSessionInfo(username, action) {
    if (action == "prev") {
        session_num--;
    } else {
        session_num++;
    }
    if (session_num <= 0) {
        session_num = 0;
    } else if (session_num >= 9){
        session_num = 9
    }
    for (i=0; i < 10; i++) {
        if (session_num == i) {
            //$(`#divTableRow_${_username}_session_${i}`).show();
            $(`.${username.replace(/ /g, "")}_session_${i}`).show();
        } else {
            //$(`#divTableRow_${_username}_session_${i}`).hide();
            $(`.${username.replace(/ /g, "")}_session_${i}`).hide();
        }
    }

}