jQuery.noConflict();
jQuery(document).ready(function($){
    var dt = new Date();
    
    var d = dt.getDay();
    var days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];
    var day = days[d];
    
    var year = dt.getFullYear();
    
    var m = dt.getMonth();
    var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov", "Dec"];
    var month = months[m];

    var date = dt.getDate();
    document.getElementById("datetime").innerHTML = day + " " + date + " " + month + " " + year;

    //
    // Handling Data Exchanges
    //
    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }
    var control_butts = '<div class="btn-group butts" role="group" aria-label="Basic"><button type="button" id="btn-complete" class="btn btn-secondary"><i class="fas fa-check fa-xs"></i></i></button><button type="button" id="btn-edit" class="btn btn-secondary"><i class="far fa-edit fa-xs"></i></button><button type="button" id="btn-delete" class="btn btn-secondary"><i class="fas fa-trash fa-xs"></i></button></div>';

    var total = 0;
    var current = "";
    $.get("/list", 
        success=function(d, res, xhr){
            if(res=="success"){
                current = d["todo_list"];
                if(current.length == 0){
                    return;
                }
                var container = document.getElementById("list-holder");
                var list = current.split(".:::.");

                var final = "";
                for(el in list){
                    curr = list[el];
                    var t_pri = curr.slice(10, 13);
                    curr = curr + control_butts;

                    curr = `<div class="card-body cardn-${el}">` + curr + '</div>';
                    if(t_pri=='low'){
                        curr = '<div class="card low-pri">' + curr + '</div>';
                    }else if(t_pri=='mod'){
                        curr = '<div class="card mod-pri">' + curr + '</div>';
                    }else if(t_pri=='hig'){
                        curr = '<div class="card hig-pri">' + curr + '</div>';
                    }
                    final = final + curr;
                }
                document.getElementById("list-holder").innerHTML = final;
            }else{
                alert("Not able to get you Todo list... Try refreshing...");
            }
    });

    $("#add-todo").click(function(){
        var txt = $("#FormControlTextarea").val();
        var pri = $("#inputpriority").val();
        
        if(pri == "--Choose Priority--"){
            alert("Choose some priority value");
            return;
        }
        if(txt.length == 0){
            alert("Your ToDo is empty...");
            return;
        }

        txt = `<p class="${pri.toLowerCase().slice(0, 3)}">${txt}</p>`;

        if(current.length != 0){
            current = current + ".:::." + txt;
        }else{
            current = txt;
        }

        $.post({
            url: "/list",
            data: {"new_todo": current},
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success:function(d, res, xhr){
                        if(res=="success"){
                            var container = document.getElementById("list-holder");
                            var list = current.split(".:::.");

                            var final = "";
                            for(el in list){
                                curr = list[el];
                                var t_pri = curr.slice(10, 13);
                                curr = curr + control_butts;

                                curr = `<div class="card-body cardn-${el}">` + curr + '</div>';
                                if(t_pri=='low'){
                                    curr = '<div class="card low-pri">' + curr + '</div>';
                                }else if(t_pri=='mod'){
                                    curr = '<div class="card mod-pri">' + curr + '</div>';
                                }else if(t_pri=='hig'){
                                    curr = '<div class="card hig-pri">' + curr + '</div>';
                                }
                                final = final + curr;
                            }
                            document.getElementById("list-holder").innerHTML = final;
                        }else{
                            alert("Something went wrong...");
                        }
                    }
        });

    });

    $("#list-holder").on('mouseenter', '.card', function(){
        $(this).find(".butts").toggle(true);
    });
    $("#list-holder").on('mouseleave', '.card', function(){
        $(this).find(".butts").toggle(false);
    });

    $("#list-holder").on('click', '#btn-complete', function(){
        var id_cls = $(this).parents(".card-body").attr('class').split(/\s+/)[1];
        var it = parseInt(id_cls.slice(6, id_cls.length));
        var lst = current.split(".:::.");
        lst[it] = `${lst[it].slice(0, 13)} completed${lst[it].slice(13, lst[it].length)}`;
        current = lst.join(".:::.");
        $.post({
            url: "/list",
            data: {"new_todo": current},
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success:function(d, res, xhr){
                        if(res=="success"){
                            var container = document.getElementById("list-holder");
                            var list = current.split(".:::.");

                            var final = "";
                            for(el in list){
                                curr = list[el];
                                var t_pri = curr.slice(10, 13);
                                curr = curr + control_butts;

                                curr = `<div class='card-body cardn-${el}'>` + curr + "</div>";
                                if(t_pri=='low'){
                                    curr = "<div class='card low-pri'>" + curr + "</div>";
                                }else if(t_pri=='mod'){
                                    curr = "<div class='card mod-pri'>" + curr + "</div>";
                                }else if(t_pri=='hig'){
                                    curr = "<div class='card hig-pri'>" + curr + "</div>";
                                }
                                final = final + curr;
                            }
                            document.getElementById("list-holder").innerHTML = final;
                        }else{
                            alert("Something went wrong...");
                        }
                    }
        });
    });

    $("#list-holder").on('click', "#btn-edit", function(){
        var id_cls = $(this).parents(".card-body").attr('class').split(/\s+/)[1];
        document.getElementById("edit-box").innerHTML = `
        <div id="close-edit" style="position:fixed;width:100vw;height:100vh;max-width:100vw;max-height:100vh;margin:0em;border:0em;background-color:rgba(0, 0, 0, 0.4);z-index:9999;"></div>
        <div style="position:relative;width:100vw;height:100vh;max-width:100vw;max-height:100vh;margin:0em;border:0em;">
        <div class="card" style="width: 21rem; z-index:10001; top:calc(50% - 160px); left:calc(50% - 160px); position: absolute;">
            <div class="card-body">
                <h5 class="card-title">Edit</h5>
                <hr style="color:gray;">
                <p class="card-text ${id_cls}"><b>Current: </b>${$(this).parents(".butts").siblings("p").html()}</p>
                <textarea class="form-control" id="edit-submit-area" rows="3" placeholder="Enter ToDo..."></textarea>
                <a class="btn edit-submit-btn btn-primary" style="margin=2rem;">Update</a>
            </div>
        </div>
        </div>
        `;
        $(".edit-box").toggle(true);
    });
    $("#edit-box").on("click", "#close-edit", function(){$("#edit-box").toggle();})
    $("#edit-box").on("click", ".edit-submit-btn", function(){
        var id_cls = $(this).siblings(".card-text").attr('class').split(/\s+/)[1];
        var it = parseInt(id_cls.slice(6, id_cls.length));
        var new_text = $("#edit-submit-area").val();

        if(new_text.length==0){
            alert("Enter some new text or go back and delete...");
            return;
        }

        var lst = current.split(".:::.");
        if(lst[it].slice(14, 23) == "completed"){
            lst[it] = `${lst[it].slice(0, 25)}${new_text}</p>`;
        }else{
            lst[it] = `${lst[it].slice(0, 15)}${new_text}</p>`;
        }
        current = lst.join(".:::.");

        $.post({
            url: "/list",
            data: {"new_todo": current},
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success:function(d, res, xhr){
                        if(res=="success"){
                            var container = document.getElementById("list-holder");
                            var list = current.split(".:::.");

                            var final = "";
                            for(el in list){
                                curr = list[el];
                                var t_pri = curr.slice(10, 13);
                                curr = curr + control_butts;

                                curr = `<div class="card-body cardn-${el}">` + curr + '</div>';
                                if(t_pri=='low'){
                                    curr = '<div class="card low-pri">' + curr + '</div>';
                                }else if(t_pri=='mod'){
                                    curr = '<div class="card mod-pri">' + curr + '</div>';
                                }else if(t_pri=='hig'){
                                    curr = '<div class="card hig-pri">' + curr + '</div>';
                                }
                                final = final + curr;
                            }
                            document.getElementById("list-holder").innerHTML = final;
                            $("#edit-box").toggle(false);
                        }else{
                            alert("Something went wrong...");
                        }
                    }
        });
    });

    $("#list-holder").on('click', "#btn-delete", function(){
        if(!confirm("Are you sure, you want to delete this item?")){
            return;
        }
        var id_cls = $(this).parents(".card-body").attr('class').split(/\s+/)[1];
        var it = parseInt(id_cls.slice(6, id_cls.length));
        var lst = current.split(".:::.");

        lst.splice(it, 1);
        current = lst.join(".:::.");

        $.post({
            url: "/list",
            data: {"new_todo": current},
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success:function(d, res, xhr){
                        if(res=="success"){
                            if(current == ""){
                                document.getElementById("list-holder").innerHTML = "";
                                return;
                            }
                            var container = document.getElementById("list-holder");
                            var list = current.split(".:::.");

                            var final = "";
                            for(el in list){
                                curr = list[el];
                                var t_pri = curr.slice(10, 13);
                                curr = curr + control_butts;

                                curr = `<div class='card-body cardn-${el}'>` + curr + "</div>";
                                if(t_pri=='low'){
                                    curr = "<div class='card low-pri'>" + curr + "</div>";
                                }else if(t_pri=='mod'){
                                    curr = "<div class='card mod-pri'>" + curr + "</div>";
                                }else if(t_pri=='hig'){
                                    curr = "<div class='card hig-pri'>" + curr + "</div>";
                                }
                                final = final + curr;
                            }
                            document.getElementById("list-holder").innerHTML = final;
                        }else{
                            alert("Something went wrong...");
                        }
                    }
        });
    });

    $("#del-comp").click(function(){
        var lst = current.split(".:::.");
        var new_lst = [];

        for(el in lst){
            if(lst[el].slice(14, 23) != "completed"){
                new_lst.push(lst[el]);
            }
        }

        current = new_lst.join(".:::.");

        $.post({
            url: "/list",
            data: {"new_todo": current},
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success:function(d, res, xhr){
                        if(res=="success"){
                            if(current == ""){
                                document.getElementById("list-holder").innerHTML = "";
                                return;
                            }
                            var container = document.getElementById("list-holder");
                            var list = current.split(".:::.");

                            var final = "";
                            for(el in list){
                                curr = list[el];
                                var t_pri = curr.slice(10, 13);
                                curr = curr + control_butts;

                                curr = `<div class='card-body cardn-${el}'>` + curr + "</div>";
                                if(t_pri=='low'){
                                    curr = "<div class='card low-pri'>" + curr + "</div>";
                                }else if(t_pri=='mod'){
                                    curr = "<div class='card mod-pri'>" + curr + "</div>";
                                }else if(t_pri=='hig'){
                                    curr = "<div class='card hig-pri'>" + curr + "</div>";
                                }
                                final = final + curr;
                            }
                            document.getElementById("list-holder").innerHTML = final;
                        }else{
                            alert("Something went wrong...");
                        }
                    }
        });
    });

    $("#del-all").click(function(){
        if(!confirm("Are you sure, you want to delete all your todos?\n100% SURE?")){
            return;
        }
        current = "";

        $.post({
            url: "/list",
            data: {"new_todo": current},
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success:function(d, res, xhr){
                        if(res=="success"){
                            if(current == ""){
                                document.getElementById("list-holder").innerHTML = "";
                                return;
                            }
                            var container = document.getElementById("list-holder");
                            var list = current.split(".:::.");

                            var final = "";
                            for(el in list){
                                curr = list[el];
                                var t_pri = curr.slice(10, 13);
                                curr = curr + control_butts;

                                curr = `<div class='card-body cardn-${el}'>` + curr + "</div>";
                                if(t_pri=='low'){
                                    curr = "<div class='card low-pri'>" + curr + "</div>";
                                }else if(t_pri=='mod'){
                                    curr = "<div class='card mod-pri'>" + curr + "</div>";
                                }else if(t_pri=='hig'){
                                    curr = "<div class='card hig-pri'>" + curr + "</div>";
                                }
                                final = final + curr;
                            }
                            document.getElementById("list-holder").innerHTML = final;
                        }else{
                            alert("Something went wrong...");
                        }
                    }
        });
    });

    $("#logout").click(function(){
        $.post({
            url: "/logout/access",
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success: function(d, res, xhr){
                if(res=="success"){ 
                    location.replace("/logSign");
                }else{
                    alert("Something went wrong.");
                }
            }
        });
    });

    $("#mail1btn").click(function(){
        var extra = $("#Mail1Textarea").val();
        var to = "user_self";
        $.post({
            url: "/mail",
            data: {
                "extra_content": extra + "\n",
                "to": to
            },
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success: function(d, res, xhr){
                if(res=="success"){ 
                    alert("Mail sent successfully")
                }else{
                    alert("Something went wrong.");
                }
            }
        });
    });

    $("#mail2btn").click(function(){
        var extra = $("#Mail2Textarea").val();
        var to = $("#mail2email").val();
        $.post({
            url: "/mail",
            data: {
                "extra_content": extra + "\n",
                "to": to
            },
            headers: {
                'X-CSRF-TOKEN': getCookie("csrf_access_token")
            },
            success: function(d, res, xhr){
                if(res=="success"){ 
                    alert("Mail sent successfully")
                }else{
                    alert("Something went wrong.");
                }
            }
        });
    });

    $("#list-dash-list").click(function(){
        $("#list-dash").toggle(true);
        $("#list-export").toggle(false);
    });
    $("#list-export-list").click(function(){
        $("#list-dash").toggle(false);
        $("#list-export").toggle(true);
    });
});