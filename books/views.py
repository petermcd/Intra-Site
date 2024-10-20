"""Views for the Books application."""
from json import dumps, loads
from typing import Any

import requests
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.http import require_GET

from books.models import Author, Book
from settings.models import Setting


class AuthorIndexView(generic.ListView):
    """View implementation for Author list."""

    paginate_by = 10
    template_name = "books/authors.html"
    context_object_name = "author_list"

    def get_queryset(self):
        """
        Get author objects to display in index view matching the optional get query.

        Return:
            List of author objects
        """
        term = self.request.GET.get("q")
        objects = Author.objects.all().order_by("name")
        if term:
            objects = Author.objects.filter(title__icontains=term).order_by("title")
        return objects

    def get_context_data(self, **kwargs):
        """
        Retrieve context data ready for output.

        Return:
            Context data ready for output in a template
        """
        term = f'&q={self.request.GET["q"]}' if "q" in self.request.GET else ""
        context = super().get_context_data(**kwargs)
        context["search_term"] = term
        return context


class IndexView(generic.ListView):
    """View implementation for Book list."""

    paginate_by = 10
    template_name = "books/index.html"
    context_object_name = "book_list"

    def get_queryset(self):
        """
        Get book objects to display in index view matching the optional get query.

        Return:
            List of book objects
        """
        term = self.request.GET.get("q")
        objects = Book.objects.all().order_by("title").filter(read=False)
        if term:
            objects = Book.objects.filter(title__icontains=term).order_by("title")
        return objects

    def get_context_data(self, **kwargs):
        """
        Retrieve context data ready for output.

        Return:
            Context data ready for output in a template
        """
        term = f'&q={self.request.GET["q"]}' if "q" in self.request.GET else ""
        context = super().get_context_data(**kwargs)
        context["search_term"] = term
        return context


class DetailView(generic.DetailView):
    """View implementation for Book details."""

    model = Book
    template_name = "books/details.html"

    def get_queryset(self):
        """
        Get book objects to display in detail view.

        Return:
            List of book objects
        """
        return Book.objects.all()


@require_GET
def get_book_details(_, search_type: str, search: str) -> HttpResponse:
    """
    Fetch book details from the Google books API.

    Args:
        _: API Request
        search_type: What to search for
        search: Test to search for

    Returns:
         HttpResponse
    """
    response: dict[str, Any] = {
        "success": False,
        "records": 0,
    }
    content_type = "application/json"
    try:
        api_key = Setting.objects.filter(name__exact="GOOGLE_API_KEY")[0].value
        api_url = Setting.objects.filter(name__exact="GOOGLE_BOOKS_API_URL")[0].value
    except IndexError:
        response["msg"] = "The Google API does not appear to be configured."
        return HttpResponse(dumps(response), content_type=content_type)
    querystring = f"?q={search_type}:{search}&key={api_key}"
    res = requests.get(f"{api_url}{querystring}")
    if res.status_code != 200:
        response["msg"] = "Non OK response received from Google."
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
                "description": item_details.get("description", ""),
                "pages": item_details.get("pageCount", 0),
                "publisher": item_details.get("publisher", ""),
            }

            try:
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
            except KeyError:
                record["authors"] = []
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
