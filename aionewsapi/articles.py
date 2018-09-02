import asyncio

from goose3 import Goose

from .http_client import HTTPClient

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
VALIDATION_LEVELS = ('STRICT', 'DROP', 'ALLOW')


class Article:

    def __init__(self, url: str, user_agent: str = DEFAULT_USER_AGENT, headers: dict = None, proxy: str = None,
                 validation: str = 'STRICT', loop: asyncio.AbstractEventLoop = None):
        self.url = url
        if validation in VALIDATION_LEVELS:
            self.validation = validation
        else:
            raise ValueError('Validation level must be one of STRICT, DROP, or ALLOW')
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.user_agent = user_agent
        self.http_client = HTTPClient(user_agent=user_agent, headers=headers, proxy=proxy)

    async def fetch(self):

        resp = await self.http_client.get(url=self.url, is_text=True)

        article = await self.loop.run_in_executor(None, self._parse_text, resp)

        self.raw_text = article.raw_html
        self.cleaned_text = article.cleaned_text

        article_dict = {
            'url': self.url,
            'title': article.title,
            'authors': article.authors,
            'body': article.cleaned_text,
            'videos': article.movies,
            'images': article.images,
            'tags': article.tags,
            'links': article.links,
            'top_image': article.top_image,
            'tweets': article.tweets,
            'date': article.publish_date
        }

        return article_dict

        # try:
        #     return ArticleSchema(strict=True).load(article_dict).data
        # except ValidationError:
        #     raise SchemaValidationError('Unable to validate response schema')

    def _parse_text(self, text: str):
        g = Goose()
        return g.extract(raw_html=text)

    # async def fetch(self, url: str):
    #     from newspaper import Article, ArticleException
    #
    #     try:
    #         article = Article(url)
    #         article.download()
    #         article.parse()
    #         article.nlp()
    #
    #         article_dict = {
    #             'url': url,
    #             'title': article.title,
    #             'authors': article.authors,
    #             'body': article.text,
    #             'videos': article.movies,
    #             'images': article.images,
    #             'keywords': article.keywords,
    #             'tags': article.tags,
    #             'summary': article.summary
    #         }
    #
    #     except ArticleException:
    #         raise
    #
    #     try:
    #         return ArticleSchema(strict=True).load(article_dict).data
    #     except ValidationError:
    #         raise SchemaValidationError('Unable to validate response schema')
