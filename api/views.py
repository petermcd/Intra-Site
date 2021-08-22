from django.http import HttpResponse

from json import dumps, loads
import requests
from books.models import Author

API_KEY = 'AIzaSyAemadkCuLLWhPAI7jBgLQIOC56yGjSNXU'
URL = 'https://www.googleapis.com/books/v1/volumes?'


def get_book_details(request, search_type: str, search: str):
    querystring = f'q={search_type}:{search}&key={API_KEY}'
    res = requests.get(f'{URL}{querystring}')
    content_type = 'application/json'
    if res.status_code != 200:
        response = {
            'success': False,
            'records': 0
        }
        return HttpResponse(dumps(response), content_type=content_type)

    content = loads(res.content)
    if 'items' not in content or len(content['items']) == 0:
        print('reached')
        response = {
            'success': True,
            'records': 0
        }
    else:
        records = []
        for item in content['items']:
            item_details = item['volumeInfo']
            record = {'title': item_details['title'], 'subtitle': item_details['subtitle'], 'authors': [],
                      'publisher': item_details['publisher'], 'published': item_details['publishedDate'],
                      'description': item_details['description'], 'pages': item_details['pageCount']}
            for author in item_details['authors']:
                author_res = Author.objects.filter(name__exact=author)
                if len(author_res) == 0:
                    record = Author(name=author)
                    record.save()
                    author_dict = {
                        'id': record.pk,
                        'name': author,
                    }
                    record['authors'].append(author_dict)
                    continue
                author_dict = {
                    'id': author_res[0].pk,
                    'name': author_res[0].name,
                }
                record['authors'].append(author_dict)
            try:
                record['thumbnail'] = item_details['imageLinks']['thumbnail']
            except KeyError:
                record['thumbnail'] = None
            for isbn_identifier in item_details['industryIdentifiers']:
                if isbn_identifier['type'] == 'ISBN_10':
                    record['isbn10'] = isbn_identifier['identifier']
                    continue
                if isbn_identifier['type'] == 'ISBN_13':
                    record['isbn13'] = isbn_identifier['identifier']
            records.append(record)
        response = {
            'success': True,
            'records': len(records),
            'data': records
        }
    return HttpResponse(dumps(response), content_type=content_type)
