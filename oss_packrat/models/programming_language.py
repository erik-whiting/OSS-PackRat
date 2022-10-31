from .db_model import DatabaseModel


class ProgrammingLanguage(DatabaseModel):
    """
    The `ProgrammingLanguage` model is the class that represents
    a programming language. The only qualities this models has
    is an `id` and `name`.
    """

    def __init__(self, name: str, database_name: str = "OSSPackRat"):
        """
        This model is instantiated with a name and optional
        `database_name` parameter. The `name` parameter should
        be the name of the programming language.

        Parameters
        ----------
        name : str
            The name of the programming language (Python, C, etc.)

        database_name : str (optional)
            Name of the database in which OSSPackRat is operating.
            Default value is OSSPackRat. Test value is osspackrat_test.
        """
        self.name = name
        super().__init__("programming_languages", database_name)
        self.get_or_insert()

    def get_or_insert(self) -> None:
        """
        This method is used to add a record to `programming_languages`
        if one doesn't yet exist for this language. If a record doesn't
        exist, this method inserts it. Then, it sets the `ProgrammingLanguage`
        object's `id` attribute to the database ID. This is helpful back
        in the `Repository` model where the `insert` method finishes by
        creating a `repositores_programming_languages` recokrd with
        the programming language ID and repository ID.
        """
        sql = f"SELECT id from programming_languages WHERE name = '{self.name}'"
        results = self.query_object.query(sql)
        if not results:
            self._insert({"name": self.name})
            results = self.query_object.query(sql)
        self.id = results[0]["id"]

    def get_identifier(self):
        return self.id
