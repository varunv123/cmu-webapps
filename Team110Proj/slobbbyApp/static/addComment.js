function add_comment_stream(id) {
    event.preventDefault();
    console.log("add commet stream is working!");
    //console.log($('#comment-post').val());
    grumblid = id.toString();
    comid = 'stream-comment-' + grumblid;
    var comform = document.getElementById(comid);
    var text_val = comform.elements["commentfield"].value;
    if (text_val=='')
        text_val = null;
    console.log("text_val: ");
    console.log(text_val);
    commenturl = "/grumblr/comment/" + grumblid
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : commenturl, // the endpoint
        type : "POST", // http method
        data : { commentfield : text_val,csrfmiddlewaretoken: csrftoken}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            comform.elements["commentfield"].value = ''; // remove the value from the input
            //console.log(json); // log the returned json to the console
            grumblNumber = "strmcomment" + grumblid;
            //console.log(grumblNumber)
            var commentList = document.getElementById(grumblNumber);
            //console.log(commentList)
            while (commentList.hasChildNodes()) {
                commentList.removeChild(commentList.firstChild);
            }
            console.log(json);
            for (var i = 0;i < json.length;i++){

                var commentText = json[i]["fields"]["text"];
                var newItem = document.createElement("li");
                newItem.innerHTML = commentText;
                commentList.appendChild(newItem);
            }
            console.log("success stream comment"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + "error stream:" + errmsg + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

    //console.log($('#comment-post').val())
};



function add_comment(id) {
    event.preventDefault();
    //console.log($('#comment-post').val());
    grumblid = id.toString();
    comid = 'post-comment-' + grumblid;
    var comform = document.getElementById(comid);
    var text_val = comform.elements["commentfield"].value;
    if (text_val=='')
        text_val = null;
    commenturl = "/grumblr/comment/" + grumblid;
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url : commenturl, // the endpoint
        type : "POST", // http method
        data : { commentfield : text_val,csrfmiddlewaretoken: csrftoken}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            comform.elements["commentfield"].value = ''; // remove the value from the input
            grumblNumber = "jscomment" + grumblid;
            var commentList = document.getElementById(grumblNumber);
            while (commentList.hasChildNodes()) {
                commentList.removeChild(commentList.firstChild);
            }
            for (var i = 0;i < json.length;i++){

                var commentText = json[i]["fields"]["text"];
                var newItem = document.createElement("li");
                newItem.innerHTML = commentText;
                commentList.appendChild(newItem);
            }
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + "error:" + errmsg + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

    //console.log($('#comment-post').val())
};


// Submit post on submit

$('#post-comment').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
});



// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});