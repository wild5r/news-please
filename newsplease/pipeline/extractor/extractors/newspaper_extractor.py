import logging

from newspaper import Article

from .abstract_extractor import AbstractExtractor
from ..article_candidate import ArticleCandidate


class NewspaperExtractor(AbstractExtractor):
    """This class implements Newspaper as an article extractor. Newspaper is
    a subclass of ExtractorsInterface
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.name = "newspaper"

    def _article_kwargs(self):
        return {}

    def extract(self, item):
        """Creates an instance of Article without a Download and returns an ArticleCandidate with the results of
        parsing the HTML-Code.

        :param item: A NewscrawlerItem to parse.
        :return: ArticleCandidate containing the recovered article data.
        """
        article_candidate = ArticleCandidate()
        article_candidate.extractor = self._name()

        article = Article('', **self._article_kwargs())
        # old version of newspaper2k
        # article.set_html(item['spider_response'].body)
        # new version
        article.download(input_html=item['spider_response'].body, title=item['html_title'].decode())
        article.parse()
        article_candidate.title = article.title
        article_candidate.description = article.meta_description
        article_candidate.text = article.text
        article_candidate.topimage = article.top_image
        article_candidate.author = article.authors
        if article.publish_date:
            try:
                article_candidate.publish_date = article.publish_date.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError as exception:
                self.log.debug('%s: Newspaper failed to extract the date in the supported format,'
                              'Publishing date set to None' % item['url'])
        article_candidate.language = article.meta_lang
        
        # Extract canonical link
        try:
            article_candidate.canonical_link = article.canonical_link
        except AttributeError:
            # If newspaper3k doesn't provide canonical_link, try to extract it from meta tags
            try:
                canonical_meta = article.clean_doc.find('link', {'rel': 'canonical'})
                if canonical_meta and canonical_meta.get('href'):
                    article_candidate.canonical_link = canonical_meta['href']
            except:
                self.log.debug('%s: Failed to extract canonical link' % item['url'])
                article_candidate.canonical_link = None

        return article_candidate
