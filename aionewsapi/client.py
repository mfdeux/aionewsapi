import logging
import os

from .exceptions import SchemaValidationError
from .http_client import HTTPClient
from .schema import (ArticleSummarySchema,
                     SourceSchema, ValidationError)

log = logging.getLogger(__name__)

headers = {
    'Accept-Encoding':
        'gzip, deflate, sdch',
    'Accept-Language':
        'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests':
        '1',
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

VALIDATION_LEVELS = ('STRICT', 'DROP', 'ALLOW')


def parse_date(date_str):
    from dateutil.parser import parse
    parsed_date = parse(date_str)
    return parsed_date.isoformat()


class NewsAPI:

    def __init__(self, api_key: str = None, user_agent: str = DEFAULT_USER_AGENT, proxy: str = None,
                 validation: str = 'ALLOW'):
        """

        :param api_key:
        :param user_agent:
        :param proxy:
        :param validation:
        """
        if validation in VALIDATION_LEVELS:
            self.validation = validation
        else:
            raise ValueError('Validation level must be one of STRICT, DROP, or ALLOW')
        if api_key:
            self.api_key = api_key
        else:
            if os.environ.get('NEWS_API_KEY'):
                self.api_key = os.environ.get('NEWS_API_KEY')
            else:
                raise ValueError(
                    'News API key must be provided as an argument or as an environment variable NEWS_API_KEY')
        self.user_agent = user_agent
        self.http_client = HTTPClient(user_agent=user_agent, headers=headers, proxy=proxy)

    async def sources(self):
        """
        Retrieve sources from newsapi.org
        """
        url = 'https://newsapi.org/v1/sources?apiKey={}'.format(self.api_key)

        try:
            resp = await self.http_client.get(url=url, is_json=True)
        except Exception as error:
            raise

        sources = resp.get('sources', [])

        if self.validation is 'ALLOW':
            return SourceSchema(strict=False).load(
                sources, many=True).data

        try:
            return SourceSchema(strict=True).load(
                sources, many=True).data
        except ValidationError as error:
            if self.validation is 'DROP':
                loaded_sources = SourceSchema(strict=False).load(
                    sources, many=True).data
                for index in error.messages.keys():
                    del loaded_sources[index]
                return loaded_sources
            raise SchemaValidationError('Unable to validate response schema')

    async def latest_articles(self, source_name: str, sort: str):
        """
        Retrieve articles by source and sort
        :param source_name:
        :param sort:
        :return:
        """

        url = 'https://newsapi.org/v1/articles?source={}&sortBy={}&apiKey={}' \
            .format(source_name, sort, self.api_key)

        try:
            resp = await self.http_client.get(url=url, is_json=True)
        except Exception as error:
            raise

        articles = self._extract_features(resp)

        if self.validation is 'ALLOW':
            return ArticleSummarySchema(strict=False).load(
                articles, many=True).data

        try:
            return ArticleSummarySchema(strict=True).load(
                articles, many=True).data
        except ValidationError as error:
            if self.validation is 'DROP':
                loaded_articles = ArticleSummarySchema(strict=False).load(
                    articles, many=True).data
                for index in error.messages.keys():
                    del loaded_articles[index]
                return loaded_articles
            raise SchemaValidationError('Unable to validate response schema')

    def _extract_features(self, resp):
        parsed_articles = []
        source = resp.get('source')
        articles = resp.get('articles', None)
        for article in articles:
            published = article.get('publishedAt', None)
            try:
                published_dt = parse_date(published)
            except (TypeError, ValueError):
                published_dt = None
            article_dict = dict(
                id=article.get('url'),
                title=article.get('title', None),
                published_at=published_dt,
                author=article.get('author', None),
                summary=article.get('description'),
                url=article.get('url'),
            )
            parsed_articles.append(article_dict)
        return parsed_articles
