$(document).on('ready', function(){
    window.hammer = {}

    $('#upload_link').on('click', function(){
        console.log('clicked');
        $form = $('form.upload_form');
        $form.find('input#id_json_file').click();
        return false;
    });
    $('form.upload_form').find('input#id_json_file').on('change', function(){
        value = $(this).val();
        if(!(value == "") || !(value == null)) {
            $('form.upload_form').submit();
        }
    });

    $('#raw_upload_link').on('click', function(){
        console.log('clicked again');
        $form = $('form.upload_raw_form');
        $form.find('input#id_json_file').click();
        return false;
    });
    $('form.upload_raw_form').find('input#id_json_file').on('change', function(){
        value = $(this).val();
        if(!(value == "") || !(value == null)) {
            $('form.upload_raw_form').submit();
        }
    });

    $('.right_container').hide();
    $(document).on('click','.matches-button', function(event){            
        var object_id, matches, usergroup;
    
        $this = $(this);
        object_id = $this.data("result-id");
        object_string_type = $this.attr("id");
        usergroup = $this.data("group-id");
        
        console.log("object id", object_id);
        console.log("button id", object_string_type);
        console.log("usergroup", usergroup);

        $('.right_container').show();
        console.log(object_id);
        if(object_string_type == "matches"){
            console.log("Clicked Matches");
            populateMatches(object_id);
        }
        else if (object_string_type == "approved"){
            console.log("Clicked Approved");
            populateApprovedMatches(object_id, usergroup);
        }
        else if(object_string_type == "aliases"){
            console.log("Clicked Aliases");
            populateAliases(object_id);
        }
    });


    $(document).on('click','.cls_string_name', function(event){            
        var object_id, matches, usergroup;
    
        $this = $(this);
        object_id = $this.attr("id");
        object_string_type = $this.data("string-type");
        usergroup = $this.data("group-id");
        
        console.log("object id", object_id);
        console.log("string type", object_string_type);
        console.log("usergroup", usergroup);

        $('.right_container').show();
        console.log(object_id);
        if(object_string_type == "reverse_match"){
            console.log("Its working..!!");
            populateNormalizedMatches(object_id);
        }
        else if (object_string_type == "approved"){
            console.log("Its working..!!");
            populateApprovedMatches(object_id, usergroup);
        }
    });

    $(document).on('click','.match-list-container input#matches_submit_button', function(event){
        event.preventDefault();
        console.log("save clicked");

        matchstrings_form_submit();
    });


    $(document).on('click','.match-list-container input#makealias_submit_button', function(event){
        event.preventDefault();
        console.log("save clicked");

        makealias_form_submit();
    });

    $(document).on('click','.search-box input#search_text', function(event){
        
        $this = $(this);
        $this.val('');
    });


    $('.add-new-form').validate({
        
        rules:{
            'inst_name':{
                required:true,
                // nameCheck:true,
                minlength:2,
                maxlength:150
            },
            'city':{
                required:true,
                // nameCheck:true,
                minlength:2,
                maxlength:50
            },
            'state':{
                required:true,
                minlength:2,
                maxlength:50
            },
            'country':{
                required:true,
                minlength:2,
                maxlength:50
            },
            'est':{
                required:true
            },
        },
        messages:{
            'inst_name':{
                required:'Institute Name is required',
                // nameCheck: 'First Name should contain only 3 to 15 alphabets',
                minlength:'First Name should have atleast 2 characters',
                maxlength:'First Name should have less than 150 characters'
            },
            'city':{
                required:'City is required',
                // nameCheck:'Last Name should contain only 3 to 15 alphabets',
                minlength:'Last Name should have atleast 2 characters',
                maxlength:'Last Name should have less than 50 characters'
            },
            'state':{
                required:'State is required',
                minlength:'Last Name should have atleast 2 characters',
                maxlength:'Last Name should have less than 50 characters'
            },
            'country':{
                required:'Country is required',
                minlength:'Last Name should have atleast 2 characters',
                maxlength:'Last Name should have less than 50 characters'
            },
            'est':{
                required:'Established Year is required',
            },
        },
        ignore:[],
        onfocusout:function(element) {
            $(element).valid();
        },
        highlight:function(el) {
            $(el).addClass('redborder');
        },

        unhighlight:function(el){
            $(el).removeClass('redborder');
        },
        invalidHandler: function(event, validator) {
            console.log(event);
        },
        submitHandler: function(form){
            // funct.ajaxLogin(form);
            addnew_inst_form_submit();
            // form.submit();
        }
    });

    $(document).on('click', '.add-new', function(event){
        event.preventDefault();
        console.log("add new clicked");

        var modal = document.getElementById('myModal');
        var span = document.getElementsByClassName("close")[0];
        
        modal.style.display = "block";

        span.onclick = function() {
            modal.style.display = "none";
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        $(document).on('click','.add-new-form-container input#submit_form', function(event){        
            event.preventDefault();
            // validateAddNewForm();
            addnew_inst_form_submit();
        });

    });


});

/**
 * makes an ajax call to the server to get matches
 * for the given object id.
 */
function populateMatches(id) {
    var url = "/get_matches/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            $container.append($("<h5 id='inst-name'>").text(response[0].norm_string));
            $container.append("<h5 id='heading-matches'>Matches</h5>");


            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','match-list-form');
            $(fm).attr('action','#');
            $(fm).attr('method','GET');

            $(fm).append('<input type="submit" id="matches_submit_button" class="submit_button" value="Save">');
            
            var sc = document.createElement('div');
            $(sc).addClass("matches-list-scroll");
            $(sc).attr('id','matches-list-scroll'); 

            var u = document.createElement('ul');
            $(u).addClass("matches-list");
            $(u).attr('id','matches-list'); 
            
            $.each(response,function(){ 

                var d = document.createElement('li');
                $(d).addClass("match-list");
                $(d).attr('id','match-list'); 
            
                $(d).append($("<h4>").text(response[i].match_percentile));
                $(d).append($("<h6>").text("%,     Frequency:"));
                $(d).append($("<h6>").text(response[i].match.frequency));
                $(d).append($("<h3>").text(response[i].match.content));

                var c = document.createElement('div');
                $(c).addClass("check-box");
                $(c).attr('id','check-box');
                $(c).attr('data-id',response[i].match.id)

                var check_1 = document.createElement('input');
                $(check_1).attr('type','radio');
                $(check_1).attr('id','approve');
                $(check_1).attr('value',2);
                $(check_1).attr('name',response[i].match.id);

                var check_2 = document.createElement('input');
                $(check_2).attr('type','radio');
                $(check_2).attr('id','discard');
                $(check_2).attr('value',3)
                $(check_2).attr('name',response[i].match.id);

                var check_3 = document.createElement('input');
                $(check_3).attr('type','radio');
                $(check_3).attr('id','skip');
                $(check_3).attr('value',4)
                $(check_3).attr('name',response[i].match.id);

                // $(c).append('<input type="radio" id="approve" data-val="2" name="ap">');
                $(c).append($(check_1));
                $(c).append($("<p>").text("Approve"));
                // $(c).append('<input type="radio" id="discard" data-val="3" name="di">');
                $(c).append($(check_2));
                $(c).append($("<p>").text("Discard"));
                // $(c).append('<input type="radio" id="skip" data-val="4" name="sk">');
                $(c).append($(check_3));
                $(c).append($("<p>").text("Skip"));

                $(d).append($(c));
                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });
            // $(fm).append('<input type="text" id="test_text" class="test_text" value="Game On" name="game">');
            $(fm).append('<input type="submit" id="matches_submit_button" class="submit_button" value="Save">');
            f.appendChild(fm);

            $container.append(f);
            
            
        } else {
            $container.html("");
            $container.append("<h5>No Match Found</h5>");
        }
    });
}


function populateNormalizedMatches(id) {
    var url = "/get_normalized_matches/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            $container.append($("<h5 id='inst-name'>").text(response[0].unnorm_string));
            $container.append("<h5 id='heading-matches'>Matches</h5>");


            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','match-list-form');
            $(fm).attr('action','#');
            $(fm).attr('method','GET');

            $(fm).append('<input type="submit" id="matches_submit_button" class="submit_button" value="Save">');
            
            var sc = document.createElement('div');
            $(sc).addClass("matches-list-scroll");
            $(sc).attr('id','matches-list-scroll'); 

            var u = document.createElement('ul');
            $(u).addClass("matches-list");
            $(u).attr('id','matches-list'); 
            
            $.each(response,function(){ 

                var d = document.createElement('li');
                $(d).addClass("match-list");
                $(d).attr('id','match-list'); 
            
                $(d).append($("<h4>").text(response[i].match_percentile));
                $(d).append($("<h6>").text("%"));
                // $(d).append($("<h6>").text(response[i].match.frequency));
                $(d).append($("<h3>").text(response[i].match.content));

                var c = document.createElement('div');
                $(c).addClass("check-box");
                $(c).attr('id','check-box');
                $(c).attr('data-id',response[i].match.id)

                var check_1 = document.createElement('input');
                $(check_1).attr('type','radio');
                $(check_1).attr('id','approve');
                $(check_1).attr('value',2);
                $(check_1).attr('name',response[i].match.id);

                var check_2 = document.createElement('input');
                $(check_2).attr('type','radio');
                $(check_2).attr('id','discard');
                $(check_2).attr('value',3)
                $(check_2).attr('name',response[i].match.id);

                var check_3 = document.createElement('input');
                $(check_3).attr('type','radio');
                $(check_3).attr('id','skip');
                $(check_3).attr('value',4)
                $(check_3).attr('name',response[i].match.id);

                // $(c).append('<input type="radio" id="approve" data-val="2" name="ap">');
                $(c).append($(check_1));
                $(c).append($("<p>").text("Approve"));
                // $(c).append('<input type="radio" id="discard" data-val="3" name="di">');
                $(c).append($(check_2));
                $(c).append($("<p>").text("Discard"));
                // $(c).append('<input type="radio" id="skip" data-val="4" name="sk">');
                $(c).append($(check_3));
                $(c).append($("<p>").text("Skip"));

                $(d).append($(c));
                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });
            // $(fm).append('<input type="text" id="test_text" class="test_text" value="Game On" name="game">');
            $(fm).append('<input type="submit" id="matches_submit_button" class="submit_button" value="Save">');
            f.appendChild(fm);

            $container.append(f);
            
            
        } else {
            $container.html("");
            $container.append("<h5>No Match Found</h5>");
        }
    });
}


function populateApprovedMatches(id, usergroup) {
    var url = "/get_approved_matches/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            
            $container.append($("<h5 id='inst-name'>").text(response[0].norm_string));
            $container.append("<h5 id='heading-matches'>Approved Matches</h5>");

            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','makealias-list-form');
            $(fm).attr('action','#');
            $(fm).attr('method','GET');

            var sc = document.createElement('div');
            $(sc).addClass("matches-list-scroll");
            $(sc).attr('id','matches-list-scroll'); 

            var u = document.createElement('ul');
            $(u).addClass("matches-list");
            $(u).attr('id','matches-list'); 
            
            $.each(response,function(){ 

                var d = document.createElement('li');
                $(d).addClass("match-list");
                $(d).attr('id','match-list'); 
            
                $(d).append($("<h4>").text(response[i].match_percentile));
                $(d).append($("<h6>").text("%"));
                $(d).append($("<h3>").text(response[i].match.content));

                var c = document.createElement('div');
                $(c).addClass("check-box");
                $(c).attr('id','check-box');
                $(c).attr('data-id',response[i].match.id)

                // Only add a checkbox if the user has required permission
                if(usergroup !== 'undefined' && usergroup && usergroup == 1) {
                    var check_1 = document.createElement('input');
                    $(check_1).attr('type','checkbox');
                    $(check_1).attr('id','approve');
                    $(check_1).attr('value',2);
                    $(check_1).attr('name',response[i].match.id);                
                    $(c).append($(check_1));
                    $(c).append($("<p>").text("Make Alias"));
                    $(d).append($(c));
                }


                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });
            if(usergroup !== 'undefined' && usergroup && usergroup == 1){
                $(fm).append('<input type="submit" id="makealias_submit_button" class="makealias_submit_button" value="Save">');
            }   

            f.appendChild(fm);
            $container.append(f);    
            
        } else {
            $container.html("");
            $container.append("<h5>No Approved Matches Found</h5>");
        }
    });
}


function populateAliases(id) {
    var url = "/get_aliases/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            
            $container.append($("<h5 id='inst-name'>").text(response[0].norm_string));
            $container.append("<h5 id='heading-matches'>Aliases</h5>");

            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','alias-list-form');
            $(fm).attr('action','#');
            $(fm).attr('method','GET');

            var sc = document.createElement('div');
            $(sc).addClass("matches-list-scroll");
            $(sc).attr('id','matches-list-scroll'); 

            var u = document.createElement('ul');
            $(u).addClass("matches-list");
            $(u).attr('id','matches-list'); 
            
            $.each(response,function(){ 

                var d = document.createElement('li');
                $(d).addClass("match-list");
                $(d).attr('id','match-list'); 
                $(d).append($("<h3>").text(response[i].match.content));

                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });

            f.appendChild(fm);

            $container.append(f);    
            
        } else {
            $container.html("");
            $container.append("<h5>No Aliases Found</h5>");
        }
    });
}


/*function search_form_submit() {
    // console.log("search_form_submit") // sanity check
    var dt = $("#search_form").serialize();
    // console.log("Data: ", dt);

    $.ajax({
           type: "POST",
           url: "/search_form_submit/",
           data: $("#search_form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
                if(alert("Search Complete")){}
                else
                    window.location.reload();

                console.log("searching..!!");    
           }
    });
}*/


function addnew_inst_form_submit() {
    // console.log("string info submit is working!") // sanity check
    var dt = $("#add-new-form").serialize();
    // console.log("Data: ", dt);

    $.ajax({
           type: "POST",
           url: "/addnew_inst_form_submit/",
           data: $("#add-new-form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
                // alert("Changes Saved Succesfully");
                if(alert("Changes Saved Succesfully!!")){}
                else
                    window.location.reload(); 
                console.log("save succesful");    
           }
    });
}

function matchstrings_form_submit() {
    // console.log("string info submit is working!") // sanity check
    var dt = $("#match-list-form").serialize();
    // console.log("Data: ", dt);

    $.ajax({
           type: "GET",
           url: "/matchstrings_form_submit/",
           data: $("#match-list-form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
                // alert("Changes Saved Succesfully");
                if(alert("Changes Saved Succesfully!!")){}
                else
                    window.location.reload(); 
                console.log("save succesful");    
           }
    });
}

function makealias_form_submit() {

    var dt = $("#makealias-list-form").serialize();
    // console.log("Data: ", dt);

    $.ajax({
           type: "GET",
           url: "/makealias_form_submit/",
           data: $("#makealias-list-form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
                // alert("Changes Saved Succesfully");
                if(alert("Changes Saved Succesfully!!")){}
                else
                    window.location.reload(); 
                console.log("save succesful");    
           }
    });
}

