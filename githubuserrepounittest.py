import unittest
from unittest.mock import patch
from githubuserrepo import get_user_repos_and_commits  

class TestGitHubAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_user_repos_and_commits(self, mock_get):
        """
        Test the get_user_repos_and_commits function with mocked API responses.
        """
        # Mock the response for the repositories API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"name": "repo1"},  # First repository
            {"name": "repo2"}   # Second repository
        ]

        # Mock the response for the commits API
        mock_get.side_effect = [
            mock_get.return_value,  # First call (repositories)
            type('MockResponse', (), {'status_code': 200, 'json': lambda: [{}] * 5}),  # Second call (commits for repo1)
            type('MockResponse', (), {'status_code': 200, 'json': lambda: [{}] * 3})   # Third call (commits for repo2)
        ]

        # Call the function and verify the result
        result = get_user_repos_and_commits("testuser")
        self.assertEqual(result, {"repo1": 5, "repo2": 3})

    @patch('requests.get')
    def test_get_user_repos_and_commits_failure(self, mock_get):
        """
        Test the get_user_repos_and_commits function with a failed API response.
        """
        # Mock a failed response for the repositories API
        mock_get.return_value.status_code = 404

        # Call the function and verify it raises an exception
        with self.assertRaises(Exception):
            get_user_repos_and_commits("testuser")

if __name__ == "__main__":
    unittest.main()
