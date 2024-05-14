import unittest
import requests
from unittest.mock import patch
from wordpress_checker import is_wordpress, check_sites

class TestWordPressChecker(unittest.TestCase):

    @patch('requests.get')
    def test_is_wordpress_site_true(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertTrue(is_wordpress("https://rafflepress.com"))

    @patch('requests.get')
    def test_is_wordpress_site_false(self, mock_get):
        mock_get.return_value.status_code = 404
        self.assertFalse(is_wordpress("https://stackoverflow.com"))

    @patch('requests.get')
    def test_is_wordpress_site_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException
        self.assertFalse(is_wordpress("https://google.com"))

    @patch('wordpress_checker.is_wordpress')
    def test_check_sites(self, mock_is_wordpress_site):
        mock_is_wordpress_site.side_effect = [True, True, False]
        sites = [
            "https://rafflepress.com",
            "https://seashoreflowerfarm.com",
            "https://google.com",
        ]
        expected = [
            "https://rafflepress.com",
            "https://seashoreflowerfarm.com",
        ]
        self.assertEqual(check_sites(sites), expected)

if __name__ == '__main__':
    unittest.main()