jQuery.noConflict();
jQuery(document).ready(function($){

    $(".btn.signup").click(function(e){
        e.preventDefault();
        e.stopPropagation();

        var pass = $("#reg_password").val();
        var mail = $("#reg_email").val();
        $.post(url="/registration",
                data={"username": mail, "password": pass },
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
});
