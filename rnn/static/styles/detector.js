/**
 * Created by isao on 13/03/2018.
 */

function close_success() {
    $('#success').hide();
}

function close_fail() {
    $('#fail').hide();
}

var xhttp;

function detect_button() {
    var tweet = $("textarea").val();
    console.log([tweet]);

    $('#bar').show();


    xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
            if(this.responseText == 'spoiler') {
                $('#success').hide();
                $('#fail').show();
                $('#bar').hide();
            }
            else if(this.responseText == 'nonspoiler') {
                $('#fail').hide();
                $('#success').show();
                $('#bar').hide();
            }

        }
    };

    xhttp.open("POST", "main", true);
    xhttp.send(JSON.stringify(tweet));

    // stop link reloading the page
    event.preventDefault();
}

