# Paranuara Challenge
Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

## New Features
Your API must provides these end points:
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Requirements
This system requires the following to be installed:
- Python 3
- MongoDB

## Setup 
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install all dependencies into the virtual environment: `pip install -r requirements.txt`

## Run unit tests
- To run all the unit tests: `python test_app.py`

## Run 
- To start the program: `python app.py`

## APIs:
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees:
`/companies/<company_index>/employees`
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
`/people/filtered_common_friends?first_id=<first_person_index>&second_id=<second_person_index>`
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}
`/people/<person_index>/favouriteFood`

## Assumptions and Limitations
- This system assumes that the list of vegetables and fruits are only limited to those provided by the sample resources file. Any new type won't be recognized because there is no way to tell if one is vegetable or fruit based on the name alone.
- Current settings is mostly for development environment.
- For the 3rd API, it is not clear what username is so name is used for username.
