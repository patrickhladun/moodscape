from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Custom storage class for static files using S3.

    This class sets the location for static files to the value specified in the
    STATICFILES_LOCATION setting.

    Attributes:
        location (str): The S3 bucket location for static files.
    """

    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files using S3.

    This class sets the location for media files to the value specified in the
    MEDIAFILES_LOCATION setting.

    Attributes:
        location (str): The S3 bucket location for media files.
    """

    location = settings.MEDIAFILES_LOCATION
