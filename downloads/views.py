"""Views for Downloads."""
from django.http import FileResponse


def DownloadView(request, directory="", filename="") -> FileResponse:
    """
    Facilitate downloads.

    Args:
        request: http request object
        directory: Directory the file is in
        filename: File name of the file to download

    Returns:
        FileResponse object with content of the file
    """
    file_path = f"documents/{directory}/{filename}"
    return FileResponse(open(file_path, "rb"))
