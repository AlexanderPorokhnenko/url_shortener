from . import ma
from .models import Link


class LinkSchema(ma.Schema):
    class Meta:
        fields = ('url', 'short_url', 'lifespan')
        model = Link
