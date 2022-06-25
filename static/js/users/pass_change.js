$(".change_password").submit(function(e){
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
            if ("success_link" in response){
                document.location = response["success_link"]
            }
            else if("form_errors" in response){
                document.querySelector('.form_errors_errors').innerHTML = "<b>Form erors</b></br>"
                for (let key in response["form_errors"]) {
                    document.querySelector('.form_errors_errors').innerHTML += key + ": " + response["form_errors"][key] + "</br>"
                }
            }
            else if("error_link" in response){
                document.location = response["error_link"]
            }
        }
    })
})