import os, pytest

from oss_packrat.orm import database


class TestDatabase:
    test_db_name = os.getenv("DB_NAME", "osspackrat_test")
    test_error_log = "test_db_error_log.csv"
    connection = database.Connection(test_db_name, test_error_log)
    q = database.Query(connection)

    def test_query(self):
        sql = "SELECT * FROM repositories"
        results = self.q.query(sql)
        first_row = results[0]
        assert first_row["id"] == 100
        assert first_row["name"] == "TestRepo"
        assert (
            first_row["description"]
            == "This is a record in the repositories table, it is not a real repository"
        )
        assert first_row["html_url"] == "https://fake.website"
        assert first_row["clone_url"] == "https://fake.website"
        assert first_row["ssh_url"] == "https://fake.website"
        assert first_row["git_url"] == "https://fake.website"
        assert first_row["stars"] == 100
        assert first_row["forks"] == 10
        assert first_row["watchers"] == 20
        assert first_row["issues"] == 4

    def test_execute(self):
        insert = "INSERT INTO programming_languages (name) VALUES ('C++');"
        self.q.execute(insert)
        sql = "SELECT * FROM programming_languages WHERE name = 'C++'"
        results = self.q.query(sql)
        first_row = results[0]
        assert first_row["name"] == "C++"
        delete = "DELETE FROM programming_languages WHERE name = 'C++'"
        self.q.execute(delete)
        results = self.q.query(sql)
        assert results == []

    def test_log_error(self):
        insert = "INSERT INTO non_existent_table VALUES ('nothing', 'here')"
        self.q.execute(insert)
        db_error_log = open(self.test_error_log)
        errata = db_error_log.read()
        assert "INSERT INTO non_existent_table VALUES ('nothing', 'here')" in errata

    @pytest.fixture(scope="session", autouse=True)
    def cleanup(self):
        yield
        os.remove(self.test_error_log)
