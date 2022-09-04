"""Views for Downloads."""
from os.path import join, normpath

from django.http import FileResponse


def download_view(request, directory="", filename="") -> FileResponse:
    """
    Facilitate downloads.

    Args:
        request: http request object
        directory: Directory the file is in
        filename: File name of the file to download

    Returns:
        FileResponse object with content of the file
    """
    file_path = normpath(join("SiteDocuments", "directory", "filename"))
    return FileResponse(open(file_path, "rb"))
