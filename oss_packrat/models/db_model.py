from typing import Any, Dict

from oss_packrat.orm import database


class DatabaseModel:
    def __init__(self, table_name: str, database_name: str = "OSSPackRat"):
        """
        DatabaseModel is a base class that should be
        inherited by all models that are persisted
        in the database. This model provides some core
        databse functionality like saving or updating
        a database record.

        Parameters
        ----------
        table_name : str
            The name of the model's equivalent database table

        database_name : str (optional)
            The name of the database to be used. The default
            value is OSSPackRat.
        """
        self.table_name = table_name
        self.database_name = database_name
        self.query_object = database.Query(database.Connection(database_name))

    def get_identifier(self):
        """
        The `get_identifier` method needs to be implemented
        on each inheriting class of `DatabaseModel`. This
        is the property--most likely an ID--that the database
        uses to uniquely identify a record.
        """
        raise NotImplementedError

    def _insert(self, attributes: Dict[str, Any]) -> None:
        """
        The protected insert method is how a DatabaseModel
        class will initially insert itself into the database.
        It takes a dictionary of keys and any values.

        Parameters
        ----------
        attributes : dict[str, Any]
            Key value pairs of column: value
        """
        columns = list(attributes.keys())
        values = list(attributes.values())
        # Have to make values into string object
        stringy_values = []
        for v in values:
            if type(v) not in [int, float]:
                v = f"'{v}'"
            stringy_values.append(str(v))
        col_string = f"({', '.join(columns)})"
        val_string = f"({', '.join(stringy_values)})"
        sql = f"INSERT INTO {self.table_name} {col_string} VALUES {val_string}"
        self.query_object.command(sql)

    def _update(self, attributes: Dict[str, str]) -> None:
        """
        The protected _update method is how a DatabaseModel
        class can update itself in the database. It assumes
        that the object already knows its ID. This means
        that you cannot run `update` on an object that
        does not exist in the database.
        """
        sql = f"UPDATE {self.table_name} SET "
        updates = []
        for attribute in attributes:
            val = attributes[attribute]
            if type(val) == str:
                val = f"'{val}'"
            updates.append(f"{attribute} = {val}")
        sql += ", ".join(updates)
        sql += f" WHERE id = {self.get_identifier()}"
        self.query_object.command(sql)
