"""Helper methods and classes for Intranet."""

from django.core.files.storage import FileSystemStorage


class OverwriteStorageName(FileSystemStorage):
    """Class to handle file uploads and the deletion of old files."""

    def get_available_name(self, name, max_length=None) -> str:
        """
        Override the given name with tbe new name.

        Args:
            name: The name of the uploaded file
            max_length: The maximum length of the new name

        Returns:
            The new name of the file
        """
        return super().get_available_name(name, max_length)
