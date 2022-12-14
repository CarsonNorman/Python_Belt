from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect, url_for, session
from flask_app.models.scrutinize_model import Scrutiny

db='beltdb'
class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.date = data['date']
        self.num = data['num']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['users_id']
        self.scrutinyData = data['scrutinyData']
        self.name=''
    
    @classmethod
    def create(cls, data):
        data={
            **data,
            'user_id': session['id']
        }
        query = """
        INSERT INTO sightings(location, date, num, description, users_id)
        VALUES(%(location)s,%(date)s, %(num)s, %(description)s, %(user_id)s)
        """
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validateCreate(data):
        if data['location'] == '':
            flash('Location Field cannot be empty', 'Sightings')
            return False
        if data['description'] == '':
            flash('Description Cannot be empty', 'Sightings')
            return False
        if not data['date']:
            flash('Please Enter a valid date', 'Sightings')
            return False
        if not data['num'] or int(data['num']) < 1:
            flash('Please enter number of Sasquatches', 'Sightings')
            return False
        return data
    
    @classmethod
    def getAllItems(cls):
        query = """
            SELECT sightings.*, users.first_name, users.last_name
            FROM sightings JOIN users ON sightings.users_id = users.id
        """
        results = connectToMySQL(db).query_db(query)
        if results:
        
            items = []
            for item in results:
                data={
                    **item,
                    'scrutinyData':Scrutiny.get_likes({'id':item['id']}),
                }
                sighting = cls(data)
                sighting.name = f"{item['first_name']} {item['last_name']}"
                items.append(sighting)
            return items
        else:
            return []
    @classmethod
    def getOneItems(cls, data):
        query = """
            SELECT sightings.*, users.first_name, users.last_name
            FROM sightings JOIN users ON sightings.users_id = users.id
            WHERE sightings.id = %(id)s
        """
        results = connectToMySQL(db).query_db(query, data)
        for item in results:
            data={
                 **item,
                'scrutinyData':Scrutiny.get_likes({'id':item['id']}),
            }
            sighting = cls(data)
            sighting.name = f"{item['first_name']} {item['last_name']}"
            return sighting
    @classmethod
    def edit(cls, data):
        query="""
            UPDATE sightings
            SET location=%(location)s, description=%(description)s, date=%(date)s, num=%(num)s, updated_at=now()
            WHERE id=%(id)s;
        """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def delete(cls, data):
        query= """DELETE FROM scrutinize
        WHERE sightings_id = %(id)s"""
        connectToMySQL(db).query_db(query, data)
        query="""
            DELETE FROM sightings
            WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query, data)
    