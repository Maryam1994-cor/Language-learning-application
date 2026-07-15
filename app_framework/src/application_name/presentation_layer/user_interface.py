"""Implement the command-line user interface."""

from __future__ import annotations

import inspect
from typing import Any

from mysql.connector import Error, IntegrityError

from application_name.application_base import ApplicationBase
from application_name.service_layer.app_services import AppServices


class UserInterface(ApplicationBase):
    """Provide the command-line interface for the application."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the user interface."""
        self._config_dict = config
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )

        self.DB = AppServices(config)

        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: "
            "User interface initialized."
        )

    def start(self) -> None:
        """Start the main command-line interface."""
        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: "
            "User interface started."
        )

        while True:
            self.show_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.show_students()
            elif choice == "2":
                self.add_student()
            elif choice == "3":
                self.show_trainings()
            elif choice == "4":
                print("\nApplication closed.")
                self._logger.log_debug("Application closed by user.")
                break
            else:
                print("\nInvalid choice. Please enter 1, 2, 3, or 4.")

    def show_menu(self) -> None:
        """Display the main menu."""
        app_name = self.META.get(
            "app_name",
            "Language Learning Application",
        )

        print("\n" + "=" * 45)
        print(app_name)
        print("=" * 45)
        print("1. View students")
        print("2. Add student")
        print("3. View language-learning records")
        print("4. Exit")
        print("=" * 45)

    def show_students(self) -> None:
        """Display all students from the database."""
        print("\nStudents")

        try:
            students = self.DB.get_students()

            if not students:
                print("No students found.")
                return

            print("-" * 74)
            print(
                f"{'ID':<6}"
                f"{'Student Name':<28}"
                f"{'Email':<40}"
            )
            print("-" * 74)

            for student in students:
                print(
                    f"{student['student_id']:<6}"
                    f"{student['student_name']:<28}"
                    f"{student['email']:<40}"
                )

            print("-" * 74)
            print(f"Total students: {len(students)}")

        except Error as error:
            print(f"Unable to retrieve students: {error}")
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {error}"
            )

    def add_student(self) -> None:
        """Add a new student to the database."""
        print("\nAdd Student")

        student_name = input("Enter student name: ").strip()
        email = input("Enter email address: ").strip()

        try:
            student_id = self.DB.add_student(
                student_name=student_name,
                email=email,
            )

            print(
                f"Student added successfully with ID {student_id}."
            )

        except ValueError as error:
            print(f"Validation error: {error}")

        except IntegrityError:
            print(
                "A student with this email address already exists."
            )

        except Error as error:
            print(f"Unable to add student: {error}")
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {error}"
            )

    def show_trainings(self) -> None:
        """Display student language-learning records."""
        print("\nLanguage-Learning Records")

        try:
            records = self.DB.get_training_records()

            if not records:
                print("No language-learning records found.")
                return

            print("-" * 102)
            print(
                f"{'Student Name':<24}"
                f"{'Email':<34}"
                f"{'Language':<20}"
                f"{'Proficiency':<20}"
            )
            print("-" * 102)

            for record in records:
                print(
                    f"{record['student_name']:<24}"
                    f"{record['email']:<34}"
                    f"{record['language_name']:<20}"
                    f"{record['proficiency']:<20}"
                )

            print("-" * 102)
            print(f"Total records: {len(records)}")

        except Error as error:
            print(
                f"Unable to retrieve language-learning records: {error}"
            )
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {error}"
            )