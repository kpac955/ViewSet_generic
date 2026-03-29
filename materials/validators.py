import re

from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    if value and not re.match(youtube_pattern, value):
        raise ValidationError("Допускаются ссылки только на youtube.com")
