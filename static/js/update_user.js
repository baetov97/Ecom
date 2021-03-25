$('.update_button').on('click', function () {
    update_user();
});

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

function update_user() {
    var first_name = $('#first_name').val();
    var last_name = $('#last_name').val();
    var username = $('#username').val();
    $.ajax({
        url: "/user/update/",
        type: "POST",
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        data: {first_name: first_name, last_name: last_name, username: username},
        success: function (json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },
    });
    return false;
}