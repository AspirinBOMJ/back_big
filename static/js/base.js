
$(".signup").submit(function(e){
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
            if ("success" in response){
                document.querySelector('.form-erros-signup').innerHTML = "<b>All done</b>"
            }
            else if("form_errors" in response){
                document.querySelector('.form-erros-signup').innerHTML = "<b>Form erors</b>"
                for (let key in response["form_errors"]) {
                    document.querySelector('.form-erros-signup').innerHTML += key + ": " + response["form_errors"][key] + "</br>"
                }
            }
        }
    })
})
$(".login").submit(function(e){
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
            if ("success" in response){
                location.reload()
            }
            else if("authenticate_error" in response){
                document.querySelector('.form-erros-login').innerHTML = "<b>" + response["authenticate_error"] + "</b>"
            }
        }
    })
})

const form_container = document.querySelector("header")
if (form_container){
form_container.addEventListener("click", function(e) {
	const target = e.target;
	if (target.classList.contains("login-button") || target.classList.contains("signup-button")) {
        if (target.classList.contains("login-button")) {
            form = document.querySelector(".form-login")
            form.classList.toggle("active")
        }
        else if(target.classList.contains("signup-button")){
            form = document.querySelector(".form-signup")
            form.classList.toggle("active")
        }
        all_forms = document.querySelectorAll(".form")
        for (let i = 0; i < all_forms.length; i++) {
            if(form != all_forms[i]){
                all_forms[i].classList.remove("active")
            }    
        }
	}
})
}