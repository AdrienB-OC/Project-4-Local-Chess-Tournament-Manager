# Projet 4

# Script Installation (Example of Python 3) :


Extract the repository's files in a folder of your choosing

### 1 - Setup the virtual environment :


In your command bash/shell go in the folder containing the files

Type :  
Windows :
```
py -m venv venv
```
Unix/mac :
```
python3 -m venv venv
```


You then need to activate the virtual environment :  
Windows :
```
.\venv\Scripts\activate
```
Unix/mac :  
```
source venv/bin/activate
```
(venv) should now be displayed to the left of your command line :
```
(venv) C:\>
```

### 2 - Install the libraries required to run the script :

In the virtual environment (command bash/shell), go in the project's main folder (with the main.py file) and type : 
```
pip(3) install -r requirements.txt
```
If you get an importlib-metadata version related error, remove the "==4.8.2" part from "importlib-metadata==4.8.2" in the requirements.txt file.


### You can now run the script :  
Windows
```
C:\Folder\containing\py\files\main.py

```
Unix/mac
```
python3 main.py
```
See below for more details on how to use the script.  
# Making use of the script :

You have 2 options :  
## 1 - Use the ready to use database in the "exemple_bdd" folder
Simply drag/copy the 2 files (players_db.json and tournaments_db.json) in the main folder (the one with the main.py file) and run the script.  
You can add more data to these 2 files via the script.
## 2 - Create your own databases
Run the script, you will then need to add at least 8 players via the 1st main menu option.  
Consulting tournament data will require you to run at least 1 full tournament via the 4th main menu option.

# Generate a new flake8 report :  
Activate the virtual environment then type :
```
flake8 --format=html --htmldir=flake8_report
```
Open the index.html file (located in the flake8_report directory) in your browser to check the newly generated report.  
flake8 is configured to ignore anything located in the .git and venv folder, check and modify "setup.cfg" if needed.