$(document).on('ready', function(){

    $('#upload_link').on('click', function(){
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
        

        $('.right_container').show();
        if(object_string_type == "matches"){
            populateMatches(object_id);
            window.scrollTo(0, 0);
        }
        else if (object_string_type == "approved"){
            populateApprovedMatches(object_id, usergroup);
            window.scrollTo(0, 0);
        }
        else if(object_string_type == "aliases"){
            populateAliases(object_id);
            window.scrollTo(0, 0);
        }
        else if(object_string_type == "discarded"){
            populateDiscarded(object_id, usergroup);
            window.scrollTo(0, 0);
        }
        else if(object_string_type == "skipped"){
            populateSkipped(object_id);
            window.scrollTo(0, 0);
        }
    });


    $(document).on('click','.string-name', function(event){
        $this = $(this);
        $(document).find('.active_string').removeClass('active_string');

        $this.addClass('active_string');    
    });


    $(document).on('click','.cls_string_name', function(event){            
        var object_id, matches, usergroup;
        
        $this = $(this);

        object_id = $this.attr("id");
        object_string_type = $this.data("string-type");
        usergroup = $this.data("group-id");

        $('.right_container').show();
        if(object_string_type == "norm"){
            populateNormalizedDetails(object_id);
        }
        else if(object_string_type == "reverse_match"){
            populateReverseMatches(object_id);
        }
        else if (object_string_type == "approved"){
            populateApprovedMatches(object_id, usergroup);
        }
        window.scrollTo(0, 0);
    });

    $(document).on('click','.match-list-container input#matches_submit_button', function(event){
        event.preventDefault();
        matchstrings_form_submit();
    });


    $(document).on('click','.match-list-container input#makealias_submit_button', function(event){
        event.preventDefault();
        makealias_form_submit();
    });

    $(document).on('click','.match-list-container input#makeapproved_submit_button', function(event){
        event.preventDefault();
        makeapproved_form_submit();
    });

    $(document).on('click','.check-box button#uncheck', function(event){
        event.preventDefault();
        console.log("uncheck clicked");

        $this = $(this);
        button_id = $this.data("button-id");
        console.log(button_id);

        $(".active_radio_button").removeClass("active_radio_button");

        $(".match-list").find("[data-id='" + button_id + "']").addClass("active_radio_button");
        $(".active_radio_button input[type='radio']:checked").prop('checked', false);
        
    });

    $(document).on('click','.search-box input#search_text', function(event){
        $this = $(this);
        $this.val('');
    });



    $('.add-new-form').validate({
        
        rules:{
            'inst_name':{
                required:true,
                minlength:2,
                maxlength:150
            },
            'city':{
                required:true,
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
                minlength:'Institute Name should have atleast 2 characters',
                maxlength:'Institute Name should have less than 150 characters'
            },
            'city':{
                required:'City is required',
                // nameCheck:'Last Name should contain only 3 to 15 alphabets',
                minlength:'City should have atleast 2 characters',
                maxlength:'City should have less than 50 characters'
            },
            'state':{
                required:'State is required',
                minlength:'State should have atleast 2 characters',
                maxlength:'State should have less than 50 characters'
            },
            'country':{
                required:'Country is required',
                minlength:'Country should have atleast 2 characters',
                maxlength:'Country should have less than 50 characters'
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
            addnew_inst_form_submit();
        }
    });

    $(document).on('click', '.add-new', function(event){
        event.preventDefault();

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
            addnew_inst_form_submit();
        });

    });


    $('.add-new-alias-form').validate({
        
        rules:{
            'alias-name':{
                required:true,
                minlength:2,
                maxlength:150
            }
        },
        messages:{
            'alias-name':{
                required:'Alias Name is required',
                minlength:'Alias Name should have atleast 2 characters',
                maxlength:'Alias Name should have less than 150 characters'
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
            addnew_alias_form_submit();
        }
    });


    $(document).on('click', '.add-new-alias', function(event){
        event.preventDefault();

        $this = $(this);
        object_id = $this.data("ins");
        console.log("object id = ", object_id);

        var modal = document.getElementById('alias-modal');
        var span = document.getElementsByClassName("closed")[0];
        
        $("#inst_id").val(object_id);

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

        $(document).on('click','.add-new-alias-form-container input#submit_alias_form', function(event){        
            event.preventDefault();
            addnew_alias_form_submit();
        });
    });

});

/**
 * makes an ajax call to the server to get matches
 * for the given object id.
 */

function populateNormalizedDetails(id) {
    var url = "/get_normalized_details/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            $container.append("<h5> Institute Details </h5>");

            var f = document.createDocumentFragment();

            var d1 = document.createElement('div');
            $(d1).addClass("inst-id");
            $(d1).attr('id','inst-id');
            $(d1).append("<h3> Institute ID : </h3>");
            $(d1).append($("<h3 id='institute-id'>").text(response[0]));
            
            var d2 = document.createElement('div');
            $(d2).addClass("inst-name");
            $(d2).attr('id','inst-name');
            $(d2).append("<h3> Name : </h3>");
            $(d2).append($("<h3 id='institute-name'>").text(response[1]));
            
            var d3 = document.createElement('div');
            $(d3).addClass("inst-city");
            $(d3).attr('id','inst-city');
            $(d3).append("<h3> City : </h3>");
            $(d3).append($("<h3 id='institute-city'>").text(response[2]));
            
            var d4 = document.createElement('div');
            $(d4).addClass("inst-state");
            $(d4).attr('id','inst-state');
            $(d4).append("<h3> State : </h3>");
            $(d4).append($("<h3 id='institute-state'>").text(response[3]));
            
            var d5 = document.createElement('div');
            $(d5).addClass("inst-country");
            $(d5).attr('id','inst-country');
            $(d5).append("<h3> Country : </h3>");
            $(d5).append($("<h3 id='institute-country'>").text(response[4]));
            
            var d6= document.createElement('div');
            $(d6).addClass("inst-est");
            $(d6).attr('id','inst-est');
            $(d6).append("<h3> Established : </h3>");
            $(d6).append($("<h3 id='institute-est'>").text(response[5]));


            f.appendChild(d1);
            f.appendChild(d2);
            f.appendChild(d3);
            f.appendChild(d4);
            f.appendChild(d5);
            f.appendChild(d6);

            $container.append(f);

             
        } else {
            $container.html("");
            $container.append("<h5>Details Not Found</h5>");
        }
    });
}


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

                var uncheck = document.createElement('button');
                $(uncheck).attr('type', 'button');
                $(uncheck).attr('id', 'uncheck');
                $(uncheck).attr('data-button-id', response[i].match.id);
                $(uncheck).append("Uncheck");

                $(c).append($(check_1));
                $(c).append($("<p>").text("Approve"));

                $(c).append($(check_2));
                $(c).append($("<p>").text("Discard"));
                
                $(c).append($(check_3));
                $(c).append($("<p>").text("Skip"));

                $(c).append($(uncheck));                

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

            if(usergroup !== 'undefined' && usergroup && usergroup == 1){
                $(fm).append('<input type="submit" id="makealias_submit_button" class="makealias_submit_button" value="Save">');
            }

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
                    $(check_1).attr('type','radio');
                    $(check_1).attr('id','alias');
                    $(check_1).attr('value',2);
                    $(check_1).attr('name',response[i].match.id);

                    $(c).append($(check_1));
                    $(c).append($("<p>").text("Make Alias"));

                    var check_2 = document.createElement('input');
                    $(check_2).attr('type','radio');
                    $(check_2).attr('id','discard');
                    $(check_2).attr('value',3);
                    $(check_2).attr('name',response[i].match.id);

                    $(c).append($(check_2));
                    $(c).append($("<p>").text("Make Unapproved"));

                    var uncheck = document.createElement('button');
                    $(uncheck).attr('type', 'button');
                    $(uncheck).attr('id', 'uncheck');
                    $(uncheck).attr('data-button-id', response[i].match.id);
                    $(uncheck).append("Uncheck");

                    $(c).append($(uncheck));

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


function populateDiscarded(id, usergroup) {
    var url = "/get_discarded/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            
            $container.append($("<h5 id='inst-name'>").text(response[0].norm_string));
            $container.append("<h5 id='heading-matches'>Discarded Matches</h5>");

            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','makeapproved-list-form');
            $(fm).attr('action','#');
            $(fm).attr('method','GET');

            if(usergroup !== 'undefined' && usergroup && usergroup == 1){
                $(fm).append('<input type="submit" id="makeapproved_submit_button" class="makeapproved_submit_button" value="Save">');
            }
            
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
                if(response[i].status == 3){
                    $(d).append($("<h6>").text(" (M)"));
                }
                else{
                    $(d).append($("<h6>").text("  (A)"));
                }

                var c = document.createElement('div');
                $(c).addClass("check-box");
                $(c).attr('id','check-box');
                $(c).attr('data-id',response[i].match.id)

                if(usergroup !== 'undefined' && usergroup && usergroup == 1 && response[i].status == 3) {
                    var check_1 = document.createElement('input');
                    $(check_1).attr('type','checkbox');
                    $(check_1).attr('id','approve');
                    $(check_1).attr('value',2);
                    $(check_1).attr('name',response[i].match.id);

                    $(c).append($(check_1));
                    $(c).append($("<p>").text("  Approve Discarded Match"));

                    $(d).append($(c));
                }                

                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });

            if(usergroup !== 'undefined' && usergroup && usergroup == 1){
                $(fm).append('<input type="submit" id="makeapproved_submit_button" class="makeapproved_submit_button" value="Save">');
            }

            f.appendChild(fm);

            $container.append(f);    
            
        } else {
            $container.html("");
            $container.append("<h5>No Discarded Matches Found</h5>");
        }
    });
}


function populateSkipped(id) {
    var url = "/get_skipped/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            
            $container.append($("<h5 id='inst-name'>").text(response[0].norm_string));
            $container.append("<h5 id='heading-matches'>Skipped Matches</h5>");

            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','skip-list-form');
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

                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });

            f.appendChild(fm);

            $container.append(f);    
            
        } else {
            $container.html("");
            $container.append("<h5>No Skipped Matches Found</h5>");
        }
    });
}


function populateAliases(id) {
    var url = "/get_aliases/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;
        $container.html("");
        
        var r = document.createElement('div');
        $(r).attr('class', 'add-new-alias');
        $(r).attr('id', 'add-new-alias');
        $(r).attr('data-ins', id);

        var p = document.createElement('a');

        $(p).attr('class','add-alias icon');
        $(p).attr('id', 'add-alias');
        $(p).attr('href','#');

        var q = document.createElement('span');

        $(q).attr('class', 'iconicfill-plus-alt');
        $(q).text('  Add New Alias');

        $(p).append($(q));
        $(r).append($(p));

        if (response.length > 0) { 
            
            $container.append($("<h5 id='inst-name'>").text(response[0].norm_string));
            $container.append("<h5 id='heading-matches'>Aliases</h5>");

            if(window.hammer.usergroup == 1){
                $container.append($(r));        
            }

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
            // $container.html("");
            $container.append("<h5>No Aliases Found</h5>");
            if(window.hammer.usergroup == 1){
                $container.append($(r));        
            }
        }
    });
}

function populateReverseMatches(id) {
    var url = "/get_reverse_matches/?s=" + id;
    $.get(url, function(response) {
        $container = $('.match-list-container');

        var i = 0;

        if (response.length > 0) { 
            $container.html("");
            $container.append($("<h5 id='inst-name'>").text(response[0].unnorm_string));
            $container.append("<h5 id='heading-matches'>Unapproved Matches</h5>");


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

                var uncheck = document.createElement('button');
                $(uncheck).attr('type', 'button');
                $(uncheck).attr('id', 'uncheck');
                $(uncheck).attr('data-button-id', response[i].match.id);
                $(uncheck).append("Uncheck");

                $(c).append($(check_1));
                $(c).append($("<p>").text("Approve"));

                $(c).append($(check_2));
                $(c).append($("<p>").text("Discard"));
                
                $(c).append($(check_3));
                $(c).append($("<p>").text("Skip"));

                $(c).append($(uncheck));

                $(d).append($(c));
                $(u).append($(d));
                $(sc).append($(u));
                $(fm).append($(sc));
                i++;
            });
            
            $(fm).append('<input type="submit" id="matches_submit_button" class="submit_button" value="Save">');
            f.appendChild(fm);

            $container.append(f);
            
            
        } else {
            $container.html("");
            $container.append("<h5>No Match Found</h5>");
        }
    });
}



function addnew_inst_form_submit() {
    // console.log("string info submit is working!") // sanity check

    $.ajax({
           type: "POST",
           url: "/addnew_inst_form_submit/",
           data: $("#add-new-form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
                if(alert("New Institute Added Succesfully!!")){}
                else
                    window.location.reload(); 
           }
    });
}


function addnew_alias_form_submit() {
    // console.log("string info submit is working!") // sanity check

    $.ajax({
           type: "POST",
           url: "/addnew_alias_form_submit/",
           data: $("#add-new-alias-form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
                if(alert("New Alias Added Succesfully!!")){}
                else
                    window.location.reload(); 
           }
    });
}


function matchstrings_form_submit() {
    // console.log("string info submit is working!") // sanity check

    $.ajax({
           type: "GET",
           url: "/matchstrings_form_submit/",
           data: $("#match-list-form").serialize(), // serializes the form's elements.

           success: function(data){
                if(alert("Changes Saved Succesfully!!")){}
                else
                    window.location.reload();     
           }
    });
}


function makealias_form_submit() {

    $.ajax({
           type: "GET",
           url: "/makealias_form_submit/",
           data: $("#makealias-list-form").serialize(), // serializes the form's elements.

           success: function(data){
                if(alert("Changes Saved Succesfully!!")){}
                else
                    window.location.reload();   
           }
    });
}

function makeapproved_form_submit() {

    $.ajax({
           type: "GET",
           url: "/makeapproved_form_submit/",
           data: $("#makeapproved-list-form").serialize(), // serializes the form's elements.

           success: function(data){
                if(alert("Changes Saved Succesfully!!")){}
                else
                    window.location.reload();   
           }
    });
}