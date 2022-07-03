$(document).on('submit', '.comment_form', function(e) {
    e.preventDefault();
    var action_url = $(this).attr("action")
    formData = new FormData($(this).get(0));
    $.ajax({
        type: "POST",
        url: action_url,
        data: formData,
        contentType: false,
        processData: false,
        success: function(response){
            if ("comment_html" in response){
                document.querySelector(".comments-" + response['task_slug']).innerHTML += '<li class="list-group-item comment-' + response['pk'] + ' good-list">' + (response["comment_html"]) + '</li>'
            }
            else if("form_errors" in response){
                for (let key in response["form_errors"]) {
                    document.querySelector('.comm_errors-' + response['task_slug']).innerHTML += key + ": " + response["form_errors"][key] + "</br>"
                }
            }
        }
    })
});
$(document).on('submit', '.comment_delete_form', function(e) {
    e.preventDefault();
    var action_url = $(this).attr("action")
    $.ajax({
        type: "GET",
        url: action_url,
        contentType: false,
        processData: false,
        success: function(response){
            if ("pk" in response){
                document.querySelector(".comment-" + response['pk']).remove()
            }
        }
    })
});