$(document).on('ready', function(){
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
});
