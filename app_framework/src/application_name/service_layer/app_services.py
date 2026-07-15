"""Provide application services for students and language records."""

from __future__ import annotations

import inspect
from typing import Any

from application_name.application_base import ApplicationBase
from application_name.persistence_layer.mysql_persistence_wrapper import (
    MySQLPersistenceWrapper,
)


class AppServices(ApplicationBase):
    """Coordinate application operations with the persistence layer."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize application services and database access."""
        self._config_dict = config
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )

        self.DB = MySQLPersistenceWrapper(config)

        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: "
            "Application services initialized."
        )

    def get_students(self) -> list[dict[str, Any]]:
        """Return all students ordered by name."""
        query = """
            SELECT
                student_id,
                student_name,
                email
            FROM students
            ORDER BY
                student_name,
                student_id
        """

        connection = self.DB.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(query)
            students = cursor.fetchall()

            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Retrieved {len(students)} student records."
            )

            return students

        finally:
            cursor.close()
            connection.close()

    def add_student(
        self,
        student_name: str,
        email: str,
    ) -> int:
        """Insert a student and return the generated student ID."""
        normalized_name = student_name.strip()
        normalized_email = email.strip().lower()

        if not normalized_name:
            raise ValueError("Student name is required.")

        if not normalized_email:
            raise ValueError("Student email is required.")

        if "@" not in normalized_email:
            raise ValueError("Enter a valid student email address.")

        query = """
            INSERT INTO students (
                student_name,
                email
            )
            VALUES (%s, %s)
        """

        connection = self.DB.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                query,
                (
                    normalized_name,
                    normalized_email,
                ),
            )
            connection.commit()

            student_id = int(cursor.lastrowid)

            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Created student_id={student_id}."
            )

            return student_id

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_training_records(self) -> list[dict[str, Any]]:
        """Return students and their assigned language records."""
        query = """
            SELECT
                students.student_id,
                students.student_name,
                students.email,
                languages.language_name,
                student_language_xref.proficiency
            FROM student_language_xref
            INNER JOIN students
                ON students.student_id =
                   student_language_xref.student_id
            INNER JOIN languages
                ON languages.language_id =
                   student_language_xref.language_id
            ORDER BY
                students.student_name,
                languages.language_name
        """

        connection = self.DB.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(query)
            records = cursor.fetchall()

            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Retrieved {len(records)} language-learning records."
            )

            return records

        finally:
            cursor.close()
            connection.close()