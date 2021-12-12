// jshint esversion: 6


window.addEventListener("load", function() {
    (function ($) {
        django.jQuery('#id_isbn10').after('<button id="isbn10_lookup">Fetch</button>');
        django.jQuery('#isbn10_lookup').click(function (event) {
            event.preventDefault();
            isbn10_lookup();
        });
    })(django.jQuery);
});

function isbn10_lookup() {
    let url = '/api/book/isbn/' + django.jQuery('#id_isbn10').val();
    remove_lookup_message();
    django.jQuery.ajax({
        url: url,
        context: document.body
    }).done(
        function (data) {
            if (data['success'] === true && data['records'] > 0) {
                populate_form(data['data'][0]);
            } else {
                report_lookup_failure('No book found');
            }
        }
    ).fail(
        function () {
            report_lookup_failure('No book found');
        }
    );
}

function populate_form(form_data) {
    django.jQuery('#id_title').val(form_data['title']);
    django.jQuery('#id_subtitle').val(form_data['subtitle']);
    django.jQuery('#id_publisher').val(form_data['publisher']);
    django.jQuery('#id_published').val(form_data['published']);
    django.jQuery('#id_description').val(form_data['description']);
    django.jQuery('#id_pages').val(form_data['pages']);
    django.jQuery('#id_thumbnail').val(form_data['thumbnail']);
    django.jQuery('#id_isbn10').val(form_data['isbn10']);
    django.jQuery('#id_isbn13').val(form_data['isbn13']);
    let $author_select = django.jQuery('#id_authors');
    for (let author of form_data['authors']) {
        if (!option_exists(author['id'])) {
            $author_select.append(new Option(author['name'], author['id']));
        }
        $author_select.val(author['id']).change();
    }
}

function option_exists($value) {
    return django.jQuery('#id_authors option[value=' + $value + ']').length > 0;
}

function report_lookup_failure($message) {
    django.jQuery('#isbn10_lookup').after('<p style="color: red" id="lookup_failure">' + $message + '</p>');
}

function remove_lookup_message() {
    django.jQuery('#lookup_failure').remove();
}

String.prototype.htmlEscape = function () {
    let span = document.createElement('span');
    let txt = document.createTextNode('');
    span.appendChild(txt);
    txt.data = this;
    return span.innerHTML;
};
