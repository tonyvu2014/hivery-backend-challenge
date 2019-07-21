from flask import Flask, request, jsonify
from pymongo import MongoClient
import json

FRUIT_LIST = ['banana', 'apple', 'orange', 'strawberry']
VEGETABLE_LIST = ['cucumber', 'beetroot', 'carrot', 'celery']

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

def get_db():
    client = MongoClient(app.config['DB_HOST'], app.config['DB_PORT'])
    db = client[app.config['DB_NAME']]
    return client, db

@app.before_first_request
def init_db():
    client, db = get_db()

    resource_path = app.config['RESOURCES_PATH']

    companies_collection = db['companies']
    companies = companies_collection.find({})
    if companies.count() == 0:
        with open(f'{resource_path}/companies.json') as f:
            companies_data = json.load(f)
        companies_collection.insert_many(companies_data)  

    people_collection = db['people']
    if people_collection.count() == 0:
        with open(f'{resource_path}/people.json') as f:
            people_data = json.load(f)
            for p in people_data:
                favouriteFood = p['favouriteFood']
                p['favouriteVegetables'] = list(filter(lambda x: x in VEGETABLE_LIST, favouriteFood))
                p['favouriteFruits'] = list(filter(lambda x: x in FRUIT_LIST, favouriteFood))
                del p['favouriteFood']
                people_collection.insert_one(p)

    client.close()


@app.route('/')
def hello():
    return "Welcome to Paranuara!"

@app.route('/companies/<int:company_id>/employees', methods= ['GET'])
def get_company_employees(company_id):
    result = []

    try:
        client, db = get_db()

        companies_collection = db['companies']

        company = companies_collection.find_one({'index': company_id})
        if not company:
            return 'Company not found', 404

        people_collection = db['people']

        employees = people_collection.find({'company_id': company_id})
        
        for e in employees:
            result.append(e)

        client.close()
    except Exception as e:
        print('Unexpected error:', str(e))
        return 'Internal Server Error', 500

    return jsonify({'employees': result}), 200


@app.route('/people/filtered_common_friends', methods= ['GET'])
def get_filtered_common_friends():
    try:
        first_id = int(request.args.get('first_id'))
        second_id = int(request.args.get('second_id'))
    except ValueError:
        return 'Invalid person id', 400

    result = []
    try:
        client, db = get_db()

        people_collection = db['people']

        persons = people_collection.find({'$or': [
            {'index': first_id },
            {'index': second_id }
        ]})

        if persons.count() < 2:
            return 'Person not found', 404

        if persons.count() > 2:
            return 'Corrupted data', 500      

        common_friends = set()    

        first_person = {}
        second_person = {}
        for p in persons:
            if p['index'] == first_id: 
                first_person = {
                    'name': p['name'],
                    'age': p['age'],
                    'address': p['address'],
                    'phone': p['phone']
                }
            else:
                second_person = {
                    'name': p['name'],
                    'age': p['age'],
                    'address': p['address'],
                    'phone': p['phone']
                }

            friends = p['friends']
            for f in friends:
                common_friends.add(f['index'])

        filtered_common_friends = people_collection.find({'$and': [
            {'index': {'$in': list(common_friends)}},
            {'eyeColor': 'brown'},
            {'has_died': False}
        ]})  

        for f in filtered_common_friends:
            result.append(f)      

        client.close()
    except Exception as e:
        print('Unexpected error:', str(e))
        return 'Internal Server Error', 500

    return jsonify({'first_person': first_person, 'second_person': second_person,'filtered_common_friends': result})

@app.route('/people/<int:person_id>/favouriteFood', methods= ['GET'])
def get_favourite_food(person_id):

    result = {}
    try:
        client, db = get_db()

        people_collection = db['people']

        person = people_collection.find_one({'index': person_id})

        if not person:
            return 'Person not found', 404
            
        client.close()
    except Exception as e:
        print('Unexpected error:', str(e))
        return 'Internal Server Error', 500

    return jsonify({
        'username': person['name'],
        'age': person['age'],
        'fruits': person['favouriteFruits'],
        'vegetables': person['favouriteVegetables']
    })

if __name__ == '__main__':
    app.run()