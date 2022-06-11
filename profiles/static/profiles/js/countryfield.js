// <!-- js to change country field to same placeholder colour as rest of form -->
let countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
// then capture change event - see if has changed from placeholder to text
// then get the value of it and return the correct colour
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});
