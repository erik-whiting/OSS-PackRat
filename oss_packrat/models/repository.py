from typing import Any

from .db_model import DatabaseModel


class Repository(DatabaseModel):
    """
    The `Repository` model is the class that represents a GitHub
    (or in the future, GitLab) repository. It inherits `DatabaseModel`
    and thus comes with database support such as helper methods for
    inserting and updating `Repository` models into a table called
    `repositories`.

    The `Repository` model can be either built from data returned
    by the GitHub API or from an existing database record. In the
    case of the latter, you are likely building your corpus of
    repositories--that is, you're building a database for future
    data analysis by scraping GitHub. If you're building the object
    from an existing database record, you've likely moved on to the
    data analysis portion of your project, so you're probably building
    `Repository` objects through database records you've previously
    scraped from GitHub.

    One important thing to note about this class and its underlying
    database table is that the ID is not coming from this project,
    it's using the GitHub ID as its unique identifier in the database.
    This will probably have to change once we add the ability to
    scrape other VCS since there's no guarantee a GitHub repo ID
    isn't being used by GitLab for another repository.
    """
    def __init__(self, data: dict[str, Any], database_name: str = "OSSPackRat"):
        """
        This model is instantiated via a dictionary which comes either
        from the GitHub API or from a database record. You can also
        otionally pass a `database_name` parameter if you're not using
        the default database name "OSSPackRat."

        Parameters
        ----------
        data : dict[str, Any]
            Repository data such as its name, description, stars, etc.

        database_name : str (optional)
            Name of the database in which OSSPackRat is operating.
            Default value is OSSPackRat. Test value is osspackrat_test.
        """
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.html_url = data["html_url"]
        self.clone_url = data["clone_url"]
        self.ssh_url = data["ssh_url"]
        self.git_url = data["git_url"]
        self.topics = data["topics"]
        self.stars = data["stars"]
        self.forks = data["forks"]
        self.watchers = data["watchers"]
        self.issues = data["issues"]
        self.language = data["programming_language"]
        self.created = data["created"]
        super().__init__("repositories", database_name)

    def __get_programming_language_id(self) -> str:
        """
        This private method will be used to build
        `programming_languages` records in the database
        as well as `repositories_programming_languages`
        records when the `Repository` model inserts
        itself. This is not yet implemented
        """
        sql = f"SELECT id FROM programming_languages WHERE name = {self.programming_language}"
        return self.query_object.query(sql)[0]

    def insert(self) -> None:
        """
        This method builds a dictionary of key-value pairs
        based on its attributes. Not all of this class's
        attributes have a column in the database, so this
        method builds the dictionary only from attributes
        that have a database representation. It uses that
        dictionary to call the `DatabaseModel` base class's
        `_insert` method. This method will also impelement
        functionality that will add a record to the
        `programming_languages` table if one doesn't exist
        yet. It will also handle inserting a record in the
        `repositories_programming_languages` in the database
        upon insertion. This has not yet been implemented.
        """
        self._insert(
            {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "html_url": self.html_url,
                "clone_url": self.clone_url,
                "ssh_url": self.ssh_url,
                "git_url": self.git_url,
                "stars": self.stars,
                "forks": self.forks,
                "watchers": self.watchers,
                "issues": self.issues,
                "created": self.created,
            }
        )

    def update(self, attributes: dict[str, Any]) -> None:
        """
        The `update` method simply takes in a dictionary
        value of attributes and values to be updated. It
        sends this dictionary to the `DatabaseModel` super
        class's `_update` method.
        """
        self._update(attributes)
