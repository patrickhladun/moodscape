from .common import *

DEBUG = False
ALLOWED_HOSTS = ["moodscape-3f1dfd651cc4.herokuapp.com"]
DATABASES = {
    "default": dj_database_url.parse(env("DATABASE_URL")),
}

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "codeinstitutefolder"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = "eu-west-1"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/moodscape/static/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/moodscape/media/"
STATICFILES_LOCATION = "moodscape/static"
MEDIAFILES_LOCATION = "moodscape/media"

DEFAULT_FILE_STORAGE = "config.utils.custom_storages.MediaStorage"
STATICFILES_STORAGE = "config.utils.custom_storages.StaticStorage"
