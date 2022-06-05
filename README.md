# Lara's Ark
##### Hypothetical Pet Clinic Project for Information Systems II requirement

### Installation Guide

#### Preliminary Requirements
1. You first need to download the following before being able to execute the file.
- Install Python 3.7.9 using ![this download link](https://www.python.org/downloads/release/python-379/)
- Using your Terminal application, install virtualenv and pip3

```sh
pip install virtualenv
```
or
```sh
pip3 install virtualenv
```

Don't forget to install pip3
```sh
python3 -m pip install --upgrade pip
```
This should enable you to use pip3 as a command in the command line (terminal).

- Download the Git package by following the instructions from ![this website](https://git-scm.com/downloads) depending on the OS that you're currently using.
- Install Visual Studio Code, PostgreSQL, ang pgAdmin4 if you haven't already.

2. Once both packages are secured, the first step is set up a virtual environment folder where you will be placing the files located in this repository onto that directory.

#### Setting up the Virtual Environment
3. Make a folder where you would like to place the virtual environment from. This folder should be a new folder with no files contained in it. For this example, we will make the folder and place it in the desktop.

Input the following line of code in your terminal
```sh
python3 -m virtualenv <pathname/to/folder>
```
As an example, with my folder labeled as "venv_personal_project", we want to put the file inside a venv folder called "projectvenv_folder. We have:
```sh
python3 -m virtualenv ~/Desktop/venv_personal_project/projectvenv_folder
```

4. You should now be able to see the previously empty folder be populated with a projectvenv_folder containing a separate version of Python 3.7.9 that you can use for building your application.

#### Importing the repo and other pertinent files
5. Clone this git repository into the "venv_personal_project" folder by typing in the following command in the Terminal:
```sh
git clone https://github.com/jmcruz14/pet-clinic-project
```
The task should begin executing after this command is registered.

6. Activate the virtual environment by entering the following command in the Terminal.

```sh
source '~/path/to/activate'
```
As an example, my path destination would be `/Users/jccruz/Desktop/venv_personal_project/projectvenv_folder/bin`.

7. The next step is to install all the relevant modules onto the terminal. Be sure that you are still in the same directory where the projectvenv_folder is stored, along with the newly cloned folders from this repository. There should be a `requirements.txt` included in the repository.

Begin importing the necessary modules by executing the following command:
```sh
pip3 install -r requirements.txt
```

After this, the virtual environment Python folder should now have all modules installed. 

#### Importing the Database SQL File

8. To import the Database SQL File, open your PostgreSQL database and your pgAdmin window. From the PostgreSQL server, Create a Database. Label the database as any name you see fit.
9. After creating the database, import the attached .sql file in this repo by right clicking the database and selecting backup and choosing the backed-up SQL file found in your current folder.

After a few seconds, the .sql file should be completely finished for importing.

10. To connect this file to your database, kindly open the `dbconnect.py` file in the Apps folder and notice the following code:

```sh
def getdblocation():

    DATABASE_URL = os.environ['DATABASE_URL']
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    return db
```

This line of code must be changed to the following:

```sh
db = psycopg2.connect(
        host = 'localhost',
        database = <SQL_database_name>,
        user = 'postgres',
        port = 5432,
        password = <password_to_server_containing_database>
    )
```
#### Executing the App
11. Congratulations. You can now execute the Application by opening the `index.py` file using VS Code and pressing F5. I will pushing changes through the next few days so please be prepared to copy-paste updated files into the virtual environment folder when they are made. Good luck to your Final Presentation and User Manual.
