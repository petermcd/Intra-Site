$(document).ready(function() {
        $('#id_isbn10').after('<button id="isdn10_lookup">Fetch</button>');
        $('#isdn10_lookup').click(function(event){
                event.preventDefault();
                isdn10_lookup();
        });
});

function isdn10_lookup(){
        let url = '/api/book/isbn/' + $('#id_isbn10').val();

        $.ajax({
                url: url,
                context: document.body
        }).done(
            function(data){
                    if (data['success'] === true && data['data'].length > 0) {
                            populate_form(data['data'][0]);
                    }
            }
        ).fail(
            function(){
                    alert('fail called');
                    alert('Lookup failed');
            });
}

function populate_form(form_data){
        $('#id_title').val(form_data['title']);
        $('#id_subtitle').val(form_data['subtitle']);
        $('#id_publisher').val(form_data['publisher']);
        $('#id_published').val(form_data['published']);
        $('#id_description').val(form_data['description']);
        $('#id_pages').val(form_data['pages']);
        $('#id_thumbnail').val(form_data['thumbnail']);
        $('#id_isbn10').val(form_data['isbn10']);
        $('#id_isbn13').val(form_data['isbn13']);
        for (let author of form_data['authors']){
                $('#id_authors').val(author['id']).change();
        }
}