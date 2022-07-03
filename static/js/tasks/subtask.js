$(document).on('submit', '.subtask_form', function(e) {
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
            if ("subtask_html" in response){
                document.querySelector(".sub-" + response['task_slug']).innerHTML += '<li class="list-group-item subtask-' + response['pk'] + ' good-list">' + (response["subtask_html"]) + '</li>'
            }
            else if("form_errors" in response){
                for (let key in response["form_errors"]) {
                    document.querySelector('.sub_errors-' + response['task_slug']).innerHTML += key + ": " + response["form_errors"][key] + "</br>"
                }
            }
        }
    })
});


$(document).on('submit', '.subtask_activate_form', function(e) {
    e.preventDefault();
    var action_url = $(this).attr("action")
    $.ajax({
        type: "GET",
        url: action_url,
        contentType: false,
        processData: false,
        success: function(response){
            if ("subtask_finished_html" in response){
                document.querySelector(".subtask-" + response['pk']).innerHTML = (response["subtask_finished_html"])
            }
        }
    })
});

$(document).on('submit', '.subtask_delete_form', function(e) {
    e.preventDefault();
    var action_url = $(this).attr("action")
    $.ajax({
        type: "GET",
        url: action_url,
        contentType: false,
        processData: false,
        success: function(response){
            if ("pk" in response){
                document.querySelector(".subtask-" + response['pk']).remove()
            }
        }
    })
});

document.querySelector("body").addEventListener("click", function(e) {
	const target = e.target;
	if (target.classList.contains("btn_sub_create")) {
        target.classList.toggle('btn-danger')
        target.nextElementSibling.classList.toggle('active')
	}
})

document.querySelector("body").addEventListener("click", function(e) {
	const target = e.target;
	if (target.classList.contains("sub_list_but")) {
        target.classList.toggle('btn-danger')
        target.nextElementSibling.classList.toggle('active')
	}
})