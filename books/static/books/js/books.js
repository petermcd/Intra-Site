$(document).ready(function() {
        $('#id_isbn10').after('<button id="isbn10_lookup">Fetch</button>');
        $('#isbn10_lookup').click(function(event){
                event.preventDefault();
                isbn10_lookup();
        });
});

function isbn10_lookup(){
        let url = '/api/book/isbn/' + $('#id_isbn10').val();
        remove_lookup_message();
        $.ajax({
                url: url,
                context: document.body
        }).done(
            function(data){
                    if (data['success'] === true && data['records'] > 0) {
                            populate_form(data['data'][0]);
                    }
                    else {
                            report_lookup_failure('No book found');
                    }
            }
        ).fail(
            function(){
                    report_lookup_failure('No book found');
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
        let $author_select = $('#id_authors');
        for (let author of form_data['authors']){
                if (!option_exists(author['id'])){
                        $author_select.append(new Option(author['name'].html(), author['id'].html()));
                }
                $author_select.val(author['id']).change();
        }
}

function option_exists($value){
        return $('#id_authors option[value=' + $value + ']').length > 0;
}

function report_lookup_failure($message){
        $('#isbn10_lookup').after('<p style="color: red" id="lookup_failure">' + $message + '</p>');
}

function remove_lookup_message(){
        $('#lookup_failure').remove();
}