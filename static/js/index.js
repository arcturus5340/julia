function compare_inputs(){
    if (($('#Username').val() == $('#Password').val()) &&
        ($('#Username').val()) && ($('#Username').val())) {
        console.log('true');
    }
}

$('#Username').keyup(compare_inputs);

$('#Password').keyup(compare_inputs);
