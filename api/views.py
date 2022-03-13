from json import dumps, loads
from typing import Any, Dict

import requests
from django.http import HttpResponse

from books.models import Author
from settings.models import Setting


def get_book_details(request, search_type: str, search: str):
    """
    Fetch book details from the Google books API.

    Args:
        request: API Request
        search_type: What to search for
        search: Test to search for

    Returns:
         List of dicts
    """
    api_key = Setting.objects.filter(name__exact="GOOGLE_API_KEY")[0].value
    api_url = Setting.objects.filter(name__exact="GOOGLE_BOOKS_API_URL")[0].value
    querystring = f"q={search_type}:{search}&key={api_key}"
    res = requests.get(f"{api_url}{querystring}")
    content_type = "application/json"
    response: Dict[str, Any] = {
        "success": False,
        "records": 0,
    }
    if res.status_code != 200:
        return HttpResponse(dumps(response), content_type=content_type)
    response["success"] = True
    records = []
    content = loads(res.content)
    if "items" in content:
        for item in content["items"]:
            item_details = item["volumeInfo"]
            record = {
                "title": item_details["title"],
                "subtitle": item_details.get("subtitle", ""),
                "authors": [],
                "published": item_details["publishedDate"],
                "description": item_details["description"],
                "pages": item_details["pageCount"],
                "publisher": item_details.get("publisher", ""),
            }

            for author in item_details["authors"]:
                author_res = Author.objects.filter(name__exact=author)
                if len(author_res) == 0:
                    new_author = Author(name=author)
                    new_author.save()
                    author_dict = {
                        "id": new_author.pk,
                        "name": author,
                    }
                    record["authors"].append(author_dict)
                    break
                author_dict = {
                    "id": author_res[0].pk,
                    "name": author_res[0].name,
                }
                record["authors"].append(author_dict)
            try:
                record["thumbnail"] = item_details["imageLinks"]["thumbnail"]
            except KeyError:
                record["thumbnail"] = None
            for isbn_identifier in item_details["industryIdentifiers"]:
                if isbn_identifier["type"] == "ISBN_10":
                    record["isbn10"] = isbn_identifier["identifier"]
                elif isbn_identifier["type"] == "ISBN_13":
                    record["isbn13"] = isbn_identifier["identifier"]
            records.append(record)

    response["records"] = len(records)
    response["data"] = records

    return HttpResponse(dumps(response), content_type=content_type)
