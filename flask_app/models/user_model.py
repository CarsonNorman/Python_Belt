from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.scrutinize_model import Scrutiny
from flask_app.models.sightings_model import Sighting
db = 'beltdb'
class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sightings = []

    @classmethod
    def get_one(cls, data):
        print('data', data)
        query="""
        SELECT * FROM users 
        WHERE id=%(id)s
        """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return results[0]
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users (email, first_name, last_name, password)
        VALUES(%(email)s,%(first_name)s, %(last_name)s, %(pass)s)
        """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def getUserInfo(cls, data):
        query = """
        SELECT *, sightings.* FROM users
        LEFT JOIN sightings ON sightings.users_id = users.id
        LEFT JOIN scrutinize ON scrutinize.sightings_id = sightings.id
        WHERE users.id = %(id)s
        """    
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if results:
            user = cls(results[0])
            for result in results:
                sightingData = {
                    'id':result['sightings.id'],
                    'location': result['location'],
                    'created_at': result['sightings.created_at'],
                    'date': result['date'],
                    'num': result['num'],
                    'description': result['description'],
                    'updated_at': result['sightings.updated_at'],
                    'users_id': result['users_id'],
                    'scrutinyData':Scrutiny.get_likes({'id': result['sightings.id']})
                }
                user.sightings.append(Sighting(sightingData))
            return user
    