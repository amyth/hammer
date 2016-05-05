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
    $('.cls_string_name').on('click', function(){            
        var object_id, matches;
    
        $this = $(this);
        object_id = $this.attr("id");
        $('.right_container').show();
        console.log(object_id);

        populateMatches(object_id);
    });


    $(document).on('click','.match-list-container input#submit_button', function(event){
        
        event.preventDefault();
        console.log("save clicked");
        
        /*var child = $('#matches-list').children();
        $(child).each(function(){
            
            //console.log("Outer Block", child);
            var inner_child = $(child).children();
            var the_child = inner_child[3];
            // console.log("Block", the_child);

            $(the_child).each(function(){
                var in_child = $(the_child).children();
                var check_value = 9;
                // console.log("Inner Block", in_child);
                if('in_child[0]:radio:checked'){
                    check_value = 2;
                }
                else if('in_child[1]:radio:checked'){
                    check_value = 3;
                }
                else{
                    check_value = 4;
                }
                console.log(check_value);
            });
        });*/

        matchstrings_form_submit();
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
            $container.append("<h5>Matches</h5>");

            var f = document.createDocumentFragment();

            var fm = document.createElement('form');
            $(fm).attr('id','match-list-form');
            $(fm).attr('action','#');
            $(fm).attr('method','GET');

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

                var ap, di, sk;
                ap = response[i].match.id + "_" + 2;
                di = response[i].match.id + "_" + 3;
                sk = response[i].match.id + "_" + 4;
                // console.log("name: ", ap);

                var check_1 = document.createElement('input');
                $(check_1).attr('type','radio');
                $(check_1).attr('id','approve');
                $(check_1).attr('data-val',2);
                $(check_1).attr('name',ap);

                var check_2 = document.createElement('input');
                $(check_2).attr('type','radio');
                $(check_2).attr('id','discard');
                $(check_2).attr('data-val',3);
                $(check_2).attr('name',di);

                var check_3 = document.createElement('input');
                $(check_3).attr('type','radio');
                $(check_3).attr('id','skip');
                $(check_3).attr('data-val',4);
                $(check_3).attr('name',sk);

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
                $(fm).append($(u));
                i++;
            });
            // $(fm).append('<input type="text" id="test_text" class="test_text" value="Game On" name="game">');
            $(fm).append('<input type="submit" id="submit_button" class="submit_button" value="Save">');
            f.appendChild(fm);

            $container.append(f);
            
            
        } else {
            $container.html("");
            $container.append("<h5>No Match Found</h5>");
        }
    });
}

function matchstrings_form_submit() {
    console.log("string info submit is working!") // sanity check
    var dt = $("#match-list-form").serialize();
    console.log("Data: ", dt);

    $.ajax({
           type: "GET",
           url: "/matchstrings_form_submit/",
           data: $("#match-list-form").serialize(), // serializes the form's elements.
           // dataType: 'json',

           success: function(data){
               console.log("save succesful");    
           }
    });
}

