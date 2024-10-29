import os
from datetime import datetime
from django.utils.text import slugify


def user_directory_path(instance, filename):
    now = datetime.now()
    date_path = now.strftime('%Y/%m/%d')

    title_slug = slugify(instance.title)

    extension = filename.split('.')[-1]
    filename = f"{instance.user.id}_{title_slug}_{now.strftime('%H%M%S')}.{extension}"

    return os.path.join(f"media-upload/{instance.user.id}/{date_path}/", filename)
