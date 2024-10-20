"""Views for Downloads."""
import re
from os.path import join, normpath
from typing import Union

from django.http import FileResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET


@require_GET
def download_view(
    _, directory="", filename=""
) -> Union[FileResponse, HttpResponseNotFound]:
    """
    Facilitate downloads.

    Args:
        _: http request object
        directory: Directory the file is in
        filename: File name of the file to download

    Returns:
        FileResponse object with content of the file or HttpResponseNotFound on failure
    """
    if re.match(r"^[a-zA-Z0-9_-]+$", directory) and re.match(
        r"^[a-zA-Z0-9_-]+\.[a-zA-Z0-9]+$", filename
    ):
        file_path = normpath(join("SiteDocuments", directory, filename))
        return FileResponse(open(file_path, "rb"))

    return HttpResponseNotFound()
