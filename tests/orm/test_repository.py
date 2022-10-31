import os, pytest, datetime

from oss_packrat.models import repository
from oss_packrat.orm import database


class TestRepository:
    test_db_name = "osspackrat_test"
    test_error_log = "test_db_error_log.csv"
    connection = database.Connection(test_db_name, test_error_log)
    q = database.Query(connection)

    def test_insert(self):
        data = {
            "id": 101,
            "name": "fake_repo",
            "description": "Fake repository for testing purposes",
            "html_url": "https://fake.website",
            "clone_url": "https://fake.website",
            "ssh_url": "https://fake.website",
            "git_url": "https://fake.website",
            "topics": "testing, automation, selenium",
            "stars": 100,
            "forks": 3,
            "watchers": 12,
            "issues": 5,
            "programming_language": "C",
            "created": datetime.date.today(),
        }
        repo = repository.Repository(data, self.test_db_name)
        repo.insert()
        new_repo = self.q.query("SELECT * FROM repositories WHERE id = 101")[0]
        assert new_repo["id"] == 101
        assert new_repo["name"] == "fake_repo"
        assert new_repo["description"] == "Fake repository for testing purposes"
        assert new_repo["html_url"] == "https://fake.website"
        assert new_repo["clone_url"] == "https://fake.website"
        assert new_repo["ssh_url"] == "https://fake.website"
        assert new_repo["git_url"] == "https://fake.website"
        assert new_repo["stars"] == 100
        assert new_repo["forks"] == 3
        assert new_repo["watchers"] == 12
        assert new_repo["issues"] == 5
        # Ensure we didn't create an extra programming_languages record for C
        pl_sql = "SELECT * FROM programming_languages WHERE name = 'C'"
        pl_results = self.q.query(pl_sql)
        assert len(pl_results) == 1
        # Ensure repositories_programming_language record was inserted
        pl_repo_sql = """
          SELECT * FROM repositories_programming_languages
          WHERE repository_id = 101 AND programming_language_id = 1
        """
        pl_repo_results = self.q.query(pl_repo_sql)
        assert len(pl_repo_results) == 1

    def test_insert_pl(self):
        data = {
            "id": 103,
            "name": "fake_repo_pl",
            "description": "Fake repository for testing purposes",
            "html_url": "https://fake.website",
            "clone_url": "https://fake.website",
            "ssh_url": "https://fake.website",
            "git_url": "https://fake.website",
            "topics": "testing, automation, selenium",
            "stars": 100,
            "forks": 3,
            "watchers": 12,
            "issues": 5,
            "programming_language": "Python",
            "created": datetime.date.today(),
        }
        repo = repository.Repository(data, self.test_db_name)
        repo.insert()
        pl_sql = "SELECT * FROM programming_languages WHERE name = 'Python'"
        pl_results = self.q.query(pl_sql)[0]
        assert pl_results["name"] == "Python"
        # Ensure repositories_programming_language record was inserted
        pl_repo_sql = """
          SELECT *
          FROM repositories_programming_languages
          WHERE repository_id = 103
        """
        pl_repo_results = self.q.query(pl_repo_sql)
        assert len(pl_repo_results) == 1

    def test_update(self):
        data = {
            "id": 102,
            "name": "another_repo",
            "description": "Fake repository for testing purposes",
            "html_url": "https://fake.website",
            "clone_url": "https://fake.website",
            "ssh_url": "https://fake.website",
            "git_url": "https://fake.website",
            "topics": "testing, automation, selenium",
            "stars": 100,
            "forks": 3,
            "watchers": 12,
            "issues": 5,
            "programming_language": "C",
            "created": datetime.date.today(),
        }
        repo = repository.Repository(data, self.test_db_name)
        repo.insert()
        repo.update({"forks": 4, "html_url": "https://anewfake.website"})
        new_repo = self.q.query("SELECT * FROM repositories WHERE id = 102")[0]
        assert new_repo["forks"] == 4
        assert new_repo["html_url"] == "https://anewfake.website"

    @pytest.fixture(scope="session", autouse=True)
    def cleanup(self):
        yield
        self.q.command("DELETE FROM repositories_programming_languages;")
        self.q.command("DELETE FROM repositories WHERE id IN (101, 102, 103);")
        self.q.command("DELETE FROM programming_languages WHERE name != 'C'")
