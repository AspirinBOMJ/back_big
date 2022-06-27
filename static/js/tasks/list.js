$(".sort_form").submit(function(e){
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
            if ("html" in response){
                if(response["finished"] == "True"){
                    document.querySelector(".finished_tasks").innerHTML = ' '
                    document.querySelector(".finished_tasks").innerHTML = response["html"]
                }
                else{
                    document.querySelector(".unfinished_tasks").innerHTML = ' '
                    document.querySelector(".unfinished_tasks").innerHTML = response["html"]
                }
            }
            else if("form_errors" in response){
                for (let key in response["form_errors"]) {
                    document.querySelector('.tasks_logo').innerHTML += key + ": " + response["form_errors"][key] + "</br>"
                }
            }
        }
    })
})
