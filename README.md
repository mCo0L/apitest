# apitest
## SETTING UP!

1. Clone the repo

## Activate Virtual Environment

2. Open Command Prompt and cd to cloned folder, cd into scripts.
3. run activate. - this will activate the virtual environment.

## To install the Requirements:

4. pip freeze > requirements.txt
5. pip install requirements.txt

## To setup server

6. Open PostgreSQL (PG ADMIN), create a database named => locinfo
7. change postgres database password in script.py and serversetup.py files.
8. on command prompt cd back to the root directory (apitest) of virtual env and run "python serversetup.py"

## Run the script

9. on command prompt run "python script.py".

## Working

There are 4 API's:

### 1. /post_location :

This API can be used to enter a new entry in the geo_info table of the database.
This API checks if the PINCODE is already present in the database or if there is any nearby latitude+longitude location already available in database. if both conditions are not present then a new entry in made in the database.

Working:
