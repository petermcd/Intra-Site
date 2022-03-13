"""Views for Downloads."""
from django.http import FileResponse


def book_download(request, book="") -> FileResponse:
    """
    Facilitate the book downloads.

    Args:
        request: http request object
        book: Book filename requested

    Returns:
        FileResponse object with content of the book
    """
    file_path = f"downloads/books/{book}"
    return FileResponse(open(file_path, "rb"))


def document_download(request, document="") -> FileResponse:
    """
    Facilitate the document downloads.

    Args:
        request: http request object
        document: Book filename requested

    Returns:
        FileResponse object with content of the document
    """
    file_path = f"downloads/documents/{document}"
    return FileResponse(open(file_path, "rb"))


def event_ticket_download(request, event_ticket="") -> FileResponse:
    """
    Facilitate the event ticket downloads.

    Args:
        request: http request object
        event_ticket: event ticket filename requested

    Returns:
        FileResponse object with content of the event ticket
    """
    file_path = f"downloads/event-tickets/{event_ticket}"
    return FileResponse(open(file_path, "rb"))


def travel_ticket_download(request, travel_ticket="") -> FileResponse:
    """
    Facilitate the travel ticket downloads.

    Args:
        request: http request object
        travel_ticket: Travel ticket filename requested

    Returns:
        FileResponse object with content of the travel ticket
    """
    file_path = f"downloads/travel-tickets/{travel_ticket}"
    return FileResponse(open(file_path, "rb"))
