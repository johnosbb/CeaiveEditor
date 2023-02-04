

from typing import Callable
from PyQt5.QtCore import QTemporaryFile
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# Import necessary modules
import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QVBoxLayout,
                             QMessageBox, QHeaderView)
import logging


class ThesaurusTheo:

    def __init__(
        self
    ):
        self.synonyms = []
        # self.antonyms = []
        # Create connection to database. If db file does not exist,
        # a new db file will be created.
        self.create_connection()

    def suggestions(self, word: str) -> list[str]:
        self.synonyms = []
        # self.antonyms = []
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                self.synonyms.append(l.name())
                # if l.antonyms():
                #     self.antonyms.append(l.antonyms()[0].name())
        logging.debug("thesaurusSqlite {}".format(set(self.synonyms)))
        # print(set(self.antonyms))
        return self.synonyms

    def create_connection(self):
        """
        Set up the connection to the database.
        Check for the tables needed.
        """
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("databases/thesaurus.db")
        if not self.database.open():
            logging.error("Unable to open data source file.")
            sys.exit(1)  # Error code 1 - signifies error
        # Check if the tables we need exist in the database
        tables_needed = {'theo'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            QMessageBox.critical(
                None, 'Error', f'The following tables are missing from the database: {tables_not_found}')
            sys.exit(1)  # Error code 1 – signifies error
        query = QSqlQuery()
        query.exec_("Select * from theo")

# # Erase database contents so that we don't have duplicates
# query.exec_("DROP TABLE accounts")
# query.exec_("DROP TABLE countries")
