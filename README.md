# 122A-DB
Final Project for CS 122A
## Setup Instructions
To create the environment that roughly matches the Gradescope testing environment, install these:
1. [MySQL Server Community Edition](https://dev.mysql.com/downloads/mysql/)
2. [mysql-connector python package](https://pypi.org/project/mysql-connector-python/)

*Note: If you  would like to use an environment other than MYSQL Server, that's probably fine, just make sure you set up the database name and 'test' account credentials properly*

Once installed and MySQL Server is running, execute `mysql -u root -p` in a terminal.

Then run the following commands:
```sql
CREATE DATABASE cs122a;
CREATE USER 'test'@'localhost'
  IDENTIFIED BY 'password';
GRANT ALL
  ON cs122a.*
  TO 'test'@'localhost';
```

This will ensure a user account and database will be created that have the same login credentials as the Gradescope environment.

From here, you can run `project.py` to ensure things are working.

More tutorials on using MySQL Server can be found [here](https://dev.mysql.com/doc/mysql-getting-started/en/#mysql-getting-started-installing).