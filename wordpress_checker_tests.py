import unittest
import requests
from unittest.mock import patch
from wordpress_checker import is_wordpress_site, check_sites

class TestWordPressChecker(unittest.TestCase):

    @patch('requests.get')
    def test_is_wordpress_site_true(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertTrue(is_wordpress_site("https://example.com"))

    @patch('requests.get')
    def test_is_wordpress_site_false(self, mock_get):
        mock_get.return_value.status_code = 404
        self.assertFalse(is_wordpress_site("https://example.com"))

    @patch('requests.get')
    def test_is_wordpress_site_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException
        self.assertFalse(is_wordpress_site("https://example.com"))

    @patch('wordpress_checker.is_wordpress_site')
    def test_check_sites(self, mock_is_wordpress_site):
        mock_is_wordpress_site.side_effect = [True, False, True]
        sites = [
            "https://example1.com",
            "https://example2.com",
            "https://example3.com",
        ]
        expected = [
            "https://example1.com",
            "https://example3.com",
        ]
        self.assertEqual(check_sites(sites), expected)

if __name__ == '__main__':
    unittest.main()