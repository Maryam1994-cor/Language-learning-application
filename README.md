# Language Learning Application

A Python and MySQL application for managing students, languages, and student language-learning records.

This project demonstrates relational database concepts from Chapters 23 and 24, including database tables, primary keys, foreign keys, SQL scripts, database users, and Python database connections.

## Project Structure

```text
python/
├── app_framework/
│   ├── config/
│   ├── src/
│   ├── Pipfile
│   └── Pipfile.lock
├── database/
│   ├── create_database.sql
│   ├── create_tables.sql
│   ├── create_user.sql
│   ├── drop_database.sql
│   ├── drop_user.sql
│   ├── initialize_database.sh
│   └── insert_data.sql
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Database Tables

| Table                   | Purpose                          |
| ----------------------- | -------------------------------- |
| `students`              | Stores student information       |
| `languages`             | Stores available languages       |
| `student_language_xref` | Connects students with languages |

The `student_language_xref` table creates a many-to-many relationship between students and languages.

## Database Scripts

| File                     | Purpose                                        |
| ------------------------ | ---------------------------------------------- |
| `create_database.sql`    | Creates the database                           |
| `drop_database.sql`      | Deletes the database                           |
| `create_tables.sql`      | Creates all database tables                    |
| `insert_data.sql`        | Inserts sample data                            |
| `create_user.sql`        | Creates the application database user          |
| `drop_user.sql`          | Deletes the application database user          |
| `initialize_database.sh` | Runs all database scripts in the correct order |

## Application Database User

The application uses a dedicated database user instead of the MySQL root user.

```text
Database: language_learning_db
User: language_learning_app
Host: localhost
Permissions: SELECT, INSERT, UPDATE, DELETE
```

The application user cannot create or drop databases.

## Requirements

Install the following software:

```text
Python 3
MySQL or MariaDB
Pipenv
Bash
```

For XAMPP, make sure MySQL is running.

```bash
sudo /opt/lampp/lampp start
```

## Environment Setup

Create the local environment file:

```bash
cp .env.example .env
```

The `.env` file should contain:

```env
APP_ENV=development
LOG_LEVEL=INFO

DB_HOST=localhost
DB_PORT=3306
DB_NAME=language_learning_db
DB_USER=language_learning_app
DB_PASSWORD=ChangeThisPassword123!

DB_POOL_NAME=language_learning_pool
DB_POOL_SIZE=5
DB_CONNECT_TIMEOUT=10
```

The `.env` file contains local database credentials and must not be committed to Git.

## Install Python Dependencies

Move into the application folder:

```bash
cd app_framework
```

Install the dependencies:

```bash
pipenv install
```

Verify the dependencies:

```bash
pipenv verify
```

## Initialize the Database

Make the initialization script executable:

```bash
chmod +x database/initialize_database.sh
```

Run the script from the project root:

```bash
./database/initialize_database.sh
```

The script runs the database files in this order:

```text
1. drop_user.sql
2. drop_database.sql
3. create_database.sql
4. create_tables.sql
5. insert_data.sql
6. create_user.sql
```

The script stops if any command fails.

> Warning: Running the initialization script deletes the existing database and recreates it.

## Run the Application

Move into the application folder:

```bash
cd app_framework
```

Run the application:

```bash
pipenv run python src/main.py \
  --configfile config/application_name_app_config.json
```

## Application Menu

The application provides these options:

```text
1. View students
2. Add student
3. View language-learning records
4. Exit
```

## Features

The application can:

- show all students;
- add a new student;
- prevent duplicate email addresses;
- show student language-learning records;
- connect to MySQL using a connection pool;
- use a restricted application database user.

## Database Verification

Login using the application database user:

```bash
/opt/lampp/bin/mysql \
  --host=localhost \
  --user=language_learning_app \
  --password \
  language_learning_db
```

Show the tables:

```sql
SHOW TABLES;
```

Expected tables:

```text
languages
student_language_xref
students
```

View students:

```sql
SELECT * FROM students;
```

View language-learning records:

```sql
SELECT
    students.student_name,
    students.email,
    languages.language_name,
    student_language_xref.proficiency
FROM student_language_xref
INNER JOIN students
    ON students.student_id = student_language_xref.student_id
INNER JOIN languages
    ON languages.language_id = student_language_xref.language_id
ORDER BY
    students.student_name,
    languages.language_name;
```

## Security

The project uses the following security practices:

- the application does not use the MySQL root account;
- a dedicated application user is created;
- the user only has `SELECT`, `INSERT`, `UPDATE`, and `DELETE` permissions;
- database passwords are stored in `.env`;
- `.env` is ignored by Git;
- SQL insert queries use parameters;
- unique constraints prevent duplicate emails;
- foreign keys protect relationships between tables.

## Sources and AI Assistance

The relational database concepts and database scripting approach used in this project are based on Chapters 23 and 24 of the assigned course textbook.

## Academic Integrity

The project author is responsible for understanding and explaining all submitted code.

Any code copied or adapted from another source must be identified and credited.

## Git History

Changes should be committed in small logical steps.

Example commit messages:

```text
db: add application database user scripts
db: add database initialization script
config: add environment settings
app: connect application to database
docs: add setup and AI attribution
```

Existing Git history should not be backdated or changed to misrepresent when the work was completed.

## Troubleshooting

### MySQL command not found

Use the XAMPP MySQL path:

```bash
/opt/lampp/bin/mysql
```

### Database connection denied

Check that:

```text
DB_USER=language_learning_app
DB_PASSWORD=ChangeThisPassword123!
```

match the values in `create_user.sql`.

### Database does not exist

Run:

```bash
./database/initialize_database.sh
```

### Environment file not visible

Hidden files can be viewed with:

```bash
ls -la
```

## License

See the `LICENSE` file for license information.
# language-learning-application
# language-learning-application
