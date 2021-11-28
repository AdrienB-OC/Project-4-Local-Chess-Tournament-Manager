# Projet 4

# Script Installation (Example of Python 3) :


Extract the repository's files in a folder of your choosing

### Setup the virtual environment :


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

### Install the libraries required to run the script :

In the virtual environment (command bash/shell) type : 
```
pip(3) install -r requirements.txt
```



You can now run the script :  
Windows
```
C:\Folder\containing\py\files\main.py

```
Unix/mac
```
python3 main.py
```

# Making use of the script :

You have 2 options :  
## Use the ready to use database in the "exemple_bdd" folder
Simply drag the 2 files (players_db.json and tournaments_db.json) in the main folder (the one with the main.py file) and run the script.  
You can add more data to these 2 files via the script.
## Create your own databases
Run the script, you will then need to add at least 8 players via the 1st main menu option.  
Consulting tournament data will require you to run at least 1 full tournament via the 4th main menu option.

# Generate a new flake8 report :  
Activate the virtual environment then type :
```
flake8 --format=html --htmldir=flake8_report
```
Open the index.hmtl file (located in the flake8_report directory) in your browser to check the newly generated report.