import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Establish connection to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 1. Create and use database
            cursor.execute("CREATE DATABASE IF NOT EXISTS project1;")
            cursor.execute("USE project1;")

            # 2. Define table creation queries
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                password VARCHAR(100) NOT NULL,
                role ENUM('TEACHER', 'STUDENT') NOT NULL
            );
            """

            create_tests_table = """
            CREATE TABLE IF NOT EXISTS tests (
                test_id INT NOT NULL PRIMARY KEY,
                TITLE VARCHAR(150) NOT NULL,
                DESCRIPTION TEXT
            );
            """

            create_questions_table = """
            CREATE TABLE IF NOT EXISTS questions (
               id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
               test_id INT(11) NOT NULL ,
               QUESTION_TEXT TEXT ,
               OPTION_A VARCHAR(500) NOT NULL,
               OPTION_B VARCHAR(500) NOT NULL,
               OPTION_C VARCHAR(500) NOT NULL,
               OPTION_D VARCHAR(500) NOT NULL,
               CORRECT_OPTION CHAR(1) NOT NULL,
               DIFFICULTY ENUM("EASY","MEDIUM","HARD"),
               TOPIC varchar(100) DEFAULT "GENERAL",
               FOREIGN KEY (test_id) REFERENCES tests(test_id)
            );
            """

            create_attempts_table = """
            CREATE TABLE IF NOT EXISTS TEST_ATTEMPTS (
                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                test_id INT,
                score INT DEFAULT 0,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (test_id) REFERENCES tests(test_id)
            );
            """

            create_attempt_answers_table ="""
            CREATE TABLE IF NOT EXISTS attempt_answers (
                answer_id INT AUTO_INCREMENT PRIMARY KEY,
                attempt_id INT,
                question_id INT,
                selected_option CHAR(1),
                is_correct BOOLEAN,
                FOREIGN KEY (attempt_id) REFERENCES TEST_ATTEMPTS(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            );
            """

            # 3. Execute queries in order (due to foreign key dependencies)
            tables = [
                create_users_table, 
                create_tests_table, 
                create_questions_table, 
                create_attempts_table, 
                create_attempt_answers_table
            ]

            for table_query in tables:
                cursor.execute(table_query)
                
            connection.commit()
            print("Database and tables created successfully.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        
    finally:
        # 4. Close connections
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    setup_database()

##import mysql.connector
##from mysql.connector import Error
##
##def setup_database():
##    try:
##        # Establish connection to MySQL server
##        connection = mysql.connector.connect(
##            host='localhost',
##            user='root',
##            password='root'
##        )
##
##        if connection.is_connected():
##            cursor = connection.cursor()
##
##            # 1. Create and use database
##            cursor.execute("CREATE DATABASE IF NOT EXISTS project1;")
##            cursor.execute("USE project1;")
##
##            # 2. Define table creation queries
##            create_users_table = """
##            CREATE TABLE IF NOT EXISTS users (
##                id INT AUTO_INCREMENT PRIMARY KEY,
##                name VARCHAR(50) NOT NULL,
##                username VARCHAR(50) UNIQUE NOT NULL,
##                password VARCHAR(100) NOT NULL,
##                role ENUM('TEACHER', 'STUDENT') NOT NULL
##            );
##            """
##
##            create_tests_table = """
##            CREATE TABLE IF NOT EXISTS tests (
##                test_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
##                TITLE VARCHAR(150) NOT NULL,
##                DESCRIPTION TEXT
##            );
##            """
##
##            create_questions_table = """
##            CREATE TABLE IF NOT EXISTS questions (
##               id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
##               test_id INT(11) NOT NULL ,
##               QUESTION_TEXT TEXT ,
##               OPTION_A VARCHAR(500) NOT NULL,
##               OPTION_B VARCHAR(500) NOT NULL,
##               OPTION_C VARCHAR(500) NOT NULL,
##               OPTION_D VARCHAR(500) NOT NULL,
##               CORRECT_OPTION CHAR(1) NOT NULL,
##               DIFFICULTY ENUM("EASY","MEDIUM","HARD"),
##               TOPIC varchar(100) DEFAULT "GENERAL",
##               FOREIGN KEY (test_id) REFERENCES tests(test_id)
##            );
##            """
##
##            create_attempts_table = """
##            CREATE TABLE IF NOT EXISTS TEST_ATTEMPTS (
##                id INT(11) AUTO_INCREMENT PRIMARY KEY,
##                student_id INT(11),
##                test_id INT,
##                score INT DEFAULT 0,
##                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
##                FOREIGN KEY (student_id) REFERENCES users(id),
##                FOREIGN KEY (test_id) REFERENCES tests(test_id)
##            );
##            """
##
##            create_attempt_answers_table ="""
##            CREATE TABLE IF NOT EXISTS attempt_answers (
##                answer_id INT AUTO_INCREMENT PRIMARY KEY,
##                attempt_id INT,
##                question_id INT,
##                selected_option CHAR(1),
##                is_correct BOOLEAN,
##                FOREIGN KEY (attempt_id) REFERENCES TEST_ATTEMPTS(id),
##                FOREIGN KEY (question_id) REFERENCES questions(id)
##            );
##            """
##
##            # 3. Execute queries in order (due to foreign key dependencies)
##            tables = [
##                create_users_table, 
##                create_tests_table, 
##                create_questions_table, 
##                create_attempts_table, 
##                create_attempt_answers_table
##            ]
##
##            for table_query in tables:
##                cursor.execute(table_query)
##                
##            connection.commit()
##            print("Database and tables created successfully.")
##
##    except Error as e:
##        print(f"Error while connecting to MySQL: {e}")
##        
##    finally:
##        # 4. Close connections
##        if 'connection' in locals() and connection.is_connected():
##            cursor.close()
##            connection.close()
##            print("MySQL connection is closed.")
##
##if __name__ == '__main__':
##    setup_database()
