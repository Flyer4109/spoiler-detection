/**
 * Created by isao on 16/01/2018.
 */


var global_array = [];
var index = 0;
var final_array = [];
var file_name = "";

$(document).keydown(function(e){
    if (e.which === 89){
        yes();
    }
    else if (e.which === 78){
        no();
    }
});

$(document).ready(function() {
    document.getElementById('file-input').addEventListener('change', readSingleFile, false);
    document.getElementById('file-input').addEventListener('change', disable, false);
    document.getElementById('file-input').addEventListener('change', display_features, false);
});

function readSingleFile(e) {
    var file = e.target.files[0];
    if (!file) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function(e) {
        var contents = e.target.result;
        var array = contents.split(/\r\n/);
        global_array = array;
        document.getElementById("tweet").innerHTML = global_array[index];
    };
    reader.readAsText(file);
}

function disable() {
    var input = document.getElementById('file-input');
    file_name = input.files.item(0).name;
    console.log(file_name);
    input.parentNode.removeChild(input);
}

function display_features() {
    document.getElementsByClassName("question")[0].style.display = "block";
    document.getElementsByClassName("hint")[0].style.display = "block";
    document.getElementsByClassName("left-button")[0].style.display = "block";
    document.getElementsByClassName("right-button")[0].style.display = "block";
    document.getElementsByClassName("back-button")[0].style.display = "block";
}

function remove_features() {
    document.getElementsByClassName("question")[0].style.display = "none";
    document.getElementsByClassName("hint")[0].style.display = "none";
    document.getElementsByClassName("left-button")[0].style.display = "none";
    document.getElementsByClassName("right-button")[0].style.display = "none";
    document.getElementsByClassName("back-button")[0].style.display = "none";
}

function yes() {
    if(index < global_array.length-2) {
        final_array[index] = [global_array[index], "s"];
        document.getElementById("tweet").innerHTML = global_array[++index];
        console.log(final_array);
        document.getElementById("back").classList.remove("disabled");

    }
    else if(index === global_array.length-2) {
        final_array[index] = [global_array[index++], "s"];
        console.log(final_array);
        document.getElementById("tweet").style.display = "none";
        document.getElementById("download").style.display = "block";
        document.getElementById("downloadb").style.display = "block";
        document.getElementById("yes").classList.add("disabled");
        document.getElementById("no").classList.add("disabled");
    }
}

function no() {
    if(index < global_array.length-2) {
        final_array[index] = [global_array[index], "ns"];
        document.getElementById("tweet").innerHTML = global_array[++index];
        console.log(final_array);
        document.getElementById("back").classList.remove("disabled");

    }
    else if(index === global_array.length-2) {
        final_array[index] = [global_array[index++], "ns"];
        console.log(final_array);
        document.getElementById("tweet").style.display = "none";
        document.getElementById("download").style.display = "block";
        document.getElementById("downloadb").style.display = "block";
        document.getElementById("yes").classList.add("disabled");
        document.getElementById("no").classList.add("disabled");
    }
}

function back() {
    if(index === global_array.length-1) {
        document.getElementById("download").style.display = "none";
        document.getElementById("downloadb").style.display = "none";
        console.log("pressed back");
        document.getElementById("tweet").style.display = "block";
        document.getElementById("tweet").innerHTML = global_array[--index];
        document.getElementById("yes").classList.remove("disabled");
        document.getElementById("no").classList.remove("disabled");
    }
    else if(index <= global_array.length-2 && index > 0) {
        console.log("pressed back");
        document.getElementById("tweet").innerHTML = global_array[--index];
    }
    if(index === 0) {
        document.getElementById("back").classList.add("disabled");
    }
}

function download() {
    remove_features();
    document.getElementById("yes").classList.remove("disabled");
    document.getElementById("no").classList.remove("disabled");

    var output = [];

    for(var i = 0; i < final_array.length; i++) {
        var line = final_array[i].join(",");
        output.push(i === 0 ? "data:text/csv;charset=utf-8," + line : line)
    }

    var data_to_encode = output.join("\r\n") + "\r\n";

    var csv_content = encodeURI(data_to_encode);

    var link = document.createElement('a');
    link.download = "labelled_" + file_name;
    link.href = csv_content;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    document.getElementById("tweet").style.display = "block";
    document.getElementById("tweet").innerHTML = '<div class="input">' +
        '<input type="file" id="file-input" accept=".csv"/>' +
        '</div>' +
        'Choose the tweet file to label';
    document.getElementById("download").style.display = "none";
    document.getElementById("downloadb").style.display = "none";

    document.getElementById('file-input').addEventListener('change', readSingleFile, false);
    document.getElementById('file-input').addEventListener('change', disable, false);
    document.getElementById('file-input').addEventListener('change', display_features, false);

    global_array = [];
    index = 0;
    final_array = [];
    file_name = "";
}
