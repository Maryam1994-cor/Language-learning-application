-- File: create_database.sql
-- Purpose: Create the database used by the Language Learning application.
-- Database design and scripting concepts are based on Chapters 23 and 24
-- of the assigned course textbook.


CREATE DATABASE IF NOT EXISTS language_learning_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE language_learning_db;