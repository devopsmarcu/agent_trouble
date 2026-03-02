import unittest
from web_search_provider.normalizer import clean_url, deduplicate_results
from web_search_provider.models import SearchResultItem

class TestNormalizer(unittest.TestCase):
    
    def test_clean_url(self):
        url = "https://example.com/page?utm_source=google&utm_medium=cpc&id=123#section1"
        cleaned = clean_url(url)
        self.assertEqual(cleaned, "https://example.com/page?id=123")
        
        # Upper case UTM + case insensitive scheme + fragment removal
        url2 = "HTTPS://example.com/page?UTM_CAMPAIGN=summer#top"
        self.assertEqual(clean_url(url2), "https://example.com/page")
        
    def test_deduplicate_results(self):
        results = [
            SearchResultItem(title="One", url="https://example.com/page?utm_source=a#frag1", snippet="1"),
            SearchResultItem(title="Two", url="https://example.com/page?utm_source=b#frag2", snippet="2"),
            SearchResultItem(title="Three", url="https://example.com/other", snippet="3")
        ]
        
        deduped = deduplicate_results(results)
        self.assertEqual(len(deduped), 2)
        self.assertEqual(deduped[0].title, "One") # Mantém a primeira ocorrência
        self.assertEqual(deduped[1].title, "Three")

if __name__ == "__main__":
    unittest.main()
