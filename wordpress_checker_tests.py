from unittest.mock import patch, MagicMock
import unittest

# Assuming the module name is wordpress_checker, adjust if it's different
from wordpress_checker import is_wordpress_site, check_sites

class TestWordPressChecker(unittest.TestCase):

    @patch('requests.get')
    def test_is_wordpress_site_wp_admin(self, mock_get):
        mock_response_wp_admin = MagicMock()
        mock_response_wp_admin.status_code = 200

        mock_response_main = MagicMock()
        mock_response_main.status_code = 200
        mock_response_main.text = ''
        mock_response_main.headers = {}

        mock_get.side_effect = [mock_response_wp_admin, mock_response_wp_admin, mock_response_main]

        self.assertTrue(is_wordpress_site("https://seashoreflowerfarm.com"))

    @patch('requests.get')
    def test_is_wordpress_site_wp_login(self, mock_get):
        mock_response_wp_login = MagicMock()
        mock_response_wp_login.status_code = 200

        mock_response_main = MagicMock()
        mock_response_main.status_code = 200
        mock_response_main.text = ''
        mock_response_main.headers = {}

        mock_get.side_effect = [mock_response_wp_login, mock_response_wp_login, mock_response_main]

        self.assertTrue(is_wordpress_site("https://seashoreflowerfarm.com"))

    @patch('requests.get')
    def test_is_wordpress_site_wp_content(self, mock_get):
        mock_response_404 = MagicMock()
        mock_response_404.status_code = 404

        mock_response_main = MagicMock()
        mock_response_main.status_code = 200
        mock_response_main.text = 'wp-content'
        mock_response_main.headers = {'set-cookie': 'wordpress_logged_in=1'}

        mock_get.side_effect = [mock_response_404, mock_response_404, mock_response_main]

        self.assertTrue(is_wordpress_site("https://seashoreflowerfarm.com"))

    @patch('requests.get')
    def test_is_wordpress_site_meta_tag(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<meta name="generator" content="WordPress 5.0">'
        mock_response.headers = {}

        mock_get.side_effect = [mock_response, mock_response, mock_response]

        self.assertTrue(is_wordpress_site("https://seashoreflowerfarm.com"))

    @patch('requests.get')
    def test_is_wordpress_site_cookie(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ''
        mock_response.headers = {'set-cookie': 'wordpress_logged_in=1'}

        mock_get.side_effect = [mock_response, mock_response, mock_response]

        self.assertTrue(is_wordpress_site("https://seashoreflowerfarm.com"))

    @patch('requests.get')
    def test_is_wordpress_site_false(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = ''
        mock_response.headers = {}
        mock_get.side_effect = [mock_response, mock_response, mock_response]

        self.assertFalse(is_wordpress_site("https://stackoverflow.com"))

    @patch('requests.get')
    def test_is_wordpress_site_false_with_headers(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.headers = {'server': 'Apache'}
        mock_response.text = ''
        mock_get.side_effect = [mock_response, mock_response, mock_response]

        self.assertFalse(is_wordpress_site("https://stackoverflow.com"))

    @patch('wordpress_checker.is_wordpress_site')
    def test_check_sites(self, mock_is_wordpress_site):
        mock_is_wordpress_site.side_effect = [True, False, True]
        sites = [
            "https://seashoreflowerfarm.com",
            "https://stackoverflow.com",
            "https://rafflepress.com",
        ]
        expected = [
            "https://seashoreflowerfarm.com",
            "https://rafflepress.com",
        ]
        self.assertEqual(check_sites(sites), expected)

if __name__ == '__main__':
    unittest.main()
