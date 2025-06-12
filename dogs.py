# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'dog_shelter.db'
TABLES = (" dogs_data "
           "LEFT JOIN genders ON dogs_data.gender_id = genders.gender_id "
           "LEFT JOIN breeds ON dogs_data.breed_id = breeds.breed_id "
           "LEFT JOIN adopters ON dogs_data.adopter_id = adopters.adopter_id " )
from easygui import *

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    codebox('Here are the results:', "Results", tabulate(results, fields.split(",")))
    title = "Dog Shelter"
    choices = ['All information',
            'Dogs who are fully vaccinated',
            'Dogs of a specific breed',
            'The health of all dogs',
            'Dogs of a certain gender',
            'Unadopted dogs who recently came to the shelter',
            'All unadopted dogs',
            'Fully vaccinated and unadopted dogs']
    choice = choicebox(msg, title, choices)
    db.close()  

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    codebox('Here are the results:', "Results", tabulate(results, headings))
    title = "Dog Shelter"
    choices = ['All information',
            'Dogs who are fully vaccinated',
            'Dogs of a specific breed',
            'The health of all dogs',
            'Dogs of a certain gender',
            'Unadopted dogs who recently came to the shelter',
            'All unadopted dogs',
            'Fully vaccinated and unadopted dogs']
    choice = choicebox(msg, title, choices)
    db.close()

msg ="What information do you want?"
title = "Dog Shelter"
choices = ['All information',
            'Dogs who are fully vaccinated',
            'Dogs of a specific breed',
            'The health of all dogs',
            'Dogs of a certain gender',
            'Unadopted dogs who recently came to the shelter',
            'All unadopted dogs',
            'Fully vaccinated and unadopted dogs']
choice = choicebox(msg, title, choices)
if choice == 'All information':
    print_query('all_data')
elif choice == 'Dogs who are fully vaccinated':
    print_query('all_vaccinated')
elif choice == 'Dogs of a specific breed':
    msg ="What dog breed?"
    title = "Dog Breeds"
    choices = ['Border Collie',
            'Boxer',
            'Bulldog',
            'Chihuahua',
            'Dachshund',
            'German Shepard',
            'Golden Retriever',
            'Great Dane',
            'Labrador',
            'Rottweiler',
            'Pitbull']
    choice = choicebox(msg, title, choices)
    print_parameter_query('dog_name, age, gender, arrival_date, date_adopted', 'breed = ? ORDER BY date_adopted', choice )

elif choice == "The health of all dogs":
    print_query('dog_health')
elif choice == 'Dogs of a certain gender':
     choices = ['Male',
            'Female']
     choice = choicebox('What gender?', 'Genders', choices)
     print_parameter_query('dog_name, age, breed, arrival_date, date_adopted', 'gender = ? ORDER BY date_adopted', choice )
elif choice == 'Unadopted dogs who recently came to the shelter':
    print_query('recent_dogs')
elif choice == 'All unadopted dogs':
    print_query('unadopted_dogs')
elif choice == 'Fully vaccinated and unadopted dogs':
    print_query('vaccinated_unadopted_dogs')