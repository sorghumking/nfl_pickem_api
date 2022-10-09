$(document).ready(init);

function init() {
    $('#submitButton').click(submitPicks);
    preparePicks();
}

var week3matchups = [
    ["NO", "CAR"],
    ["HOU", "CHI"],
    ["KC", "IND"],
    // ["BUF", "MIA"],
    // ["DET", "MIN"],
    // ["BAL", "NE"],
    // ["CIN", "NYJ"],
    // ["LV", "TEN"],
    // ["PHI", "WSH"],
    // ["JAX", "LAC"],
    // ["LAR", "ARI"],
    // ["ATL", "SEA"],
    // ["GB", "TB"],
    // ["SF", "DEN"],
    // ["DAL", "NYG"],
];

function preparePicks() {
    for (var matchup of week3matchups) {
        $('#pickz tbody').append(makePickRowHtml(matchup[0], matchup[1]));
    }
    $('#pickz').trigger('create');
}

function makePickRowHtml(away, home) {
    const matchup = away+home;
    var row = "<tr><td>"
        + makeTeamInput(away, matchup) + "</td><td>"
        + makeTeamInput(home, matchup)
        + "</td></tr>";
    return row;
}

function makeTeamInput(team, matchup) {
    var template = '<label for="@">@&nbsp;&nbsp;&nbsp;</label><input type="radio" id="@" name="' +
        matchup + ' value="@"></input>';
    return template.replaceAll("@", team);
}

function checkPicks() {
    for (var m of week3matchups) {
        const away = m[0];
        const home = m[1];
        const home_checked = $("#" + home).is(":checked");
        const away_checked = $("#" + away).is(":checked");
        if (!home_checked && !away_checked) {
            alert("Incomplete picks.");
            return false;
        }
    }
    return true;
}

function submitPicks() {
    if (!checkPicks()) return;
    var picks = []
    for (var m of week3matchups) {
        const away = m[0];
        const home = m[1];
        const matchup = away + home;
        const pick_str = "#" + home;
        const picked = $(pick_str).is(":checked");
        // console.log(home, picked);
        // console.log(createPick(home, away, 3, picked));
        picks.push(createPick(home, away, 3, picked));
    }

    var picksetData = {
        'name': "Week Three Picks of Some New Guy",
        'pool_id': 1,
        'picks': picks
    };

    ajax("http://localhost:5000/api/picksets/", "POST", picksetData).done(
        (data) => { console.log(data); }
    );
}

function createPick(home, away, week, home_win) {
    return {
        'home_team': home,
        'away_team': away,
        'week': week,
        'home_win': home_win
    };
}

var username = "brian", password = "brian";
function ajax(uri, method, data) {
    var request = {
        url: uri,
        type: method,
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: JSON.stringify(data),
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", 
                "Basic " + btoa(username + ":" + password));
        },
        error: function(jqXHR) {
            console.log("ajax error " + jqXHR.status);
        }
    };
    return $.ajax(request);
}