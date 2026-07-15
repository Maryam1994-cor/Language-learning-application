"""Provide MySQL connection-pool management for the application."""

from __future__ import annotations

import inspect
import os
from typing import Any

from application_name.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool


class MySQLPersistenceWrapper(ApplicationBase):
    """Create and manage the application's MySQL connection pool."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize database configuration and the connection pool."""
        self._config_dict = config
        self.META = config["meta"]
        self.DATABASE = config["database"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )

        self.DB_CONFIG = self._build_database_config()
        self._connection_pool = self._initialize_database_connection_pool(
            self.DB_CONFIG
        )

        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: "
            "MySQL persistence wrapper initialized."
        )

    def get_connection(self):
        """Return one connection from the configured MySQL pool."""
        try:
            connection = self._connection_pool.get_connection()

            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                "Database connection acquired from pool."
            )

            return connection
        except connector.Error as error:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Unable to acquire database connection: {error}"
            )
            raise

    def _build_database_config(self) -> dict[str, Any]:
        """Build database configuration from environment variables.

        Values from environment variables take precedence over values stored
        in the JSON configuration file. The database password must be supplied
        through the DB_PASSWORD environment variable.
        """
        connection_config = self.DATABASE["connection"]["config"]

        database_password = os.getenv("DB_PASSWORD")

        if not database_password:
            raise ValueError(
                "DB_PASSWORD is required. Copy .env.example to .env and "
                "export the environment variables before starting the "
                "application."
            )

        try:
            database_port = int(
                os.getenv(
                    "DB_PORT",
                    str(connection_config.get("port", 3306)),
                )
            )
        except ValueError as error:
            raise ValueError("DB_PORT must be a valid integer.") from error

        database_config: dict[str, Any] = {
            "host": os.getenv(
                "DB_HOST",
                connection_config.get("host", "localhost"),
            ),
            "port": database_port,
            "database": os.getenv(
                "DB_NAME",
                connection_config["database"],
            ),
            "user": os.getenv(
                "DB_USER",
                connection_config["user"],
            ),
            "password": database_password,
        }

        self._logger.log_debug(
            f"{inspect.currentframe().f_code.co_name}: "
            f"Database host={database_config['host']}, "
            f"port={database_config['port']}, "
            f"database={database_config['database']}, "
            f"user={database_config['user']}"
        )

        return database_config

    def _initialize_database_connection_pool(
        self,
        config: dict[str, Any],
    ) -> MySQLConnectionPool:
        """Create and return the MySQL connection pool."""
        pool_config = self.DATABASE["pool"]

        try:
            pool_size = int(
                os.getenv(
                    "DB_POOL_SIZE",
                    str(pool_config.get("size", 5)),
                )
            )
        except ValueError as error:
            raise ValueError("DB_POOL_SIZE must be a valid integer.") from error

        pool_name = os.getenv(
            "DB_POOL_NAME",
            pool_config.get("name", "language_learning_db_pool"),
        )

        try:
            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                "Creating MySQL connection pool."
            )

            connection_pool = MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=pool_config.get(
                    "reset_session",
                    True,
                ),
                use_pure=pool_config.get("use_pure", True),
                **config,
            )

            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: "
                "MySQL connection pool created successfully."
            )

            return connection_pool

        except connector.Error as error:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Unable to create MySQL connection pool: {error}"
            )
            raise

        except Exception as error:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: "
                f"Unexpected connection-pool error: {error}"
            )
            raise