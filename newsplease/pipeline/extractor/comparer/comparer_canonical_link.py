from ..article_candidate import ArticleCandidate


class ComparerCanonicalLink:
    """This class implements the strategy to extract the canonical link from a list of ArticleCandidates."""

    def extract(self, item, article_candidates):
        """Compares the canonical link of the article candidates and returns the best one.

        :param item: The NewscrawlerItem related to the ArticleCandidates
        :param article_candidates: The list of ArticleCandidate-Objects which have been extracted
        :return: The best canonical link according to the implemented strategy
        """
        canonical_links = []
        for article_candidate in article_candidates:
            if article_candidate.canonical_link:
                canonical_links.append(article_candidate.canonical_link)

        if not canonical_links:
            return None

        # Return the first non-empty canonical link
        return canonical_links[0] 