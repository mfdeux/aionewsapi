from marshmallow import Schema, ValidationError, fields


class SchemaValidationError(ValidationError):
    pass


class SourceSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    url = fields.Url(required=True)
    category = fields.Str(required=True)
    langugage = fields.Str(required=True)
    country = fields.Str(required=True)
    sorts_available = fields.List(fields.Str(), load_from='sortBysAvailable')


class ArticleSummarySchema(Schema):
    published_at = fields.DateTime(required=True)
    author = fields.Str(required=True)
    title = fields.Str(required=True)
    summary = fields.Str(required=True)
    url = fields.Url(required=True)


class ArticleSchema(Schema):
    url = fields.Url(required=True)
    body = fields.Str(required=True)
    title = fields.Str(required=True)
    authors = fields.List(fields.Str(required=True))
    videos = fields.List(fields.Str(required=True))
    images = fields.List(fields.Str(required=True))
    keywords = fields.List(fields.Str(required=True))
    tags = fields.List(fields.Str(required=True))
    summary = fields.Str(required=True)
