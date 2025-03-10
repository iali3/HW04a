import unittest
from unittest.mock import patch
from your_module import get_user_repos_and_commits  # Replace 'your_module' with the actual module name

class TestGitHubAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_user_repos_and_commits(self, mock_get):
        # Mock the response for repositories
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        # Mock the response for commits
        mock_get.side_effect = [
            mock_get.return_value,  # First call (repos)
            type('MockResponse', (), {'status_code': 200, 'json': lambda: [{}] * 5}),  # Second call (commits for repo1)
            type('MockResponse', (), {'status_code': 200, 'json': lambda: [{}] * 3})   # Third call (commits for repo2)
        ]

        result = get_user_repos_and_commits("testuser")
        self.assertEqual(result, {"repo1": 5, "repo2": 3})

    @patch('requests.get')
    def test_get_user_repos_and_commits_failure(self, mock_get):
        # Mock a failed response for repositories
        mock_get.return_value.status_code = 404

        with self.assertRaises(Exception):
            get_user_repos_and_commits("testuser")

if __name__ == "__main__":
    unittest.main()