jQuery.noConflict();
jQuery(document).ready(function($){

    $(".btn.signup").click(function(e){
        e.preventDefault();
        e.stopPropagation();

        var pass = $("#reg_password").val();
        var mail = $("#reg_email").val();
        var sec_q = $("#security-question").val();
        var sec_a = $("#security-answer").val();

        if(sec_q == "--Select--"){
            alert("Select a security question.");
            return;
        }
        if(sec_a.length == 0){
            alert("You should type some answer.");
            return;
        }
        $.post(url="/registration",
                data={
                    "username": mail,
                    "password": pass,
                    "security-question": sec_q,
                    "security-answer": sec_a
                },
                success=function(d, res, xhr){
                            if(res=="success"){ 
                                location.replace("/dashboard");
                            }else{
                                alert("Something went wrong.");
                            }
                        },
                dataType="json"
        );
    });

    $(".btn.login").click(function(e){
        e.preventDefault();
        e.stopPropagation();

        var pass = $("#log_password").val();
        var mail = $("#log_email").val();
        $.post("/login",
            {
                "username": mail,
                "password": pass
            },
            function(d, res, xhr){
                if(res=="success"){
                    location.replace("/dashboard");
                }else{
                    alert("Something went wrong.");
                }
            }
        );
    });

    $("a.nav-link.login").click(function(){
        $("a.nav-link.login").addClass("active");
        $("a.nav-link.signup").removeClass("active");
    });

    $("a.nav-link.signup").click(function(){
        $("a.nav-link.login").removeClass("active");
        $("a.nav-link.signup").addClass("active");
    });

    $("#forgot-pass-btn").click(function(){
        $("#signup").toggle(false);
        $("#login").toggle(false);
        $("#nav-links").toggle(false);
        $("#forgot-pass-container").toggle(true);
    });

    $("#change-pass").click(function(e){
        e.preventDefault();
        e.stopPropagation();

        var email = $("#yremail").val();
        var sec_q = $("#yrsecurity-question").val();
        var sec_a = $("#yrsecurity-answer").val();
        var new_pass = $("#new-password").val();

        if(sec_q == "--Select--"){
            alert("Selcet a security question.");
            return;
        }
        if(sec_a.length == 0){
            alert("Type some anser.");
            return;
        }
        if(new_pass.length == 0){
            alert("Type some password");
            return;
        }
        if(confirm("Are you sure?")){
            $.post({
                url: "/forgotpass",
                data: {
                    "email": email,
                    "security-question": sec_q,
                    "security-answer": sec_a,
                    "new-password": new_pass
                },
                success: function(d, res, xhr){
                    if(res =="success"){
                        alert("Password changed.");
                    }else{
                        alert("Something went wrong.");
                    }
                }
            });
        }
    });
});