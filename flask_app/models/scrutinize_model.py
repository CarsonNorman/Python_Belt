from flask_app.config.mysqlconnection import connectToMySQL


db='beltdb'
class Scrutiny:
    def __init__(self, data):
        self.user_id = data['users_id']
        self.sightings_id = data['sightings_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @staticmethod
    def validateLike(data):
        query="""
        SELECT * FROM scrutinize
        WHERE users_id = %(user)s AND sightings_id = %(item)s
        """
        results = connectToMySQL(db).query_db(query, data)
        if results:
            return False
        else:
            return True
    @staticmethod
    def dislike(data):
        query="""
        DELETE FROM scrutinize 
        WHERE users_id = %(users_id)s AND sightings_id = %(items_id)s
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def like(cls, data):
        query="""
        INSERT INTO scrutinize(users_id, sightings_id)
        VALUE(%(user)s, %(item)s)
        """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def get_likes(cls,data):
        query = """
        SELECT *
        FROM scrutinize
        WHERE scrutinize.sightings_id=%(id)s
        """
        return connectToMySQL(db).query_db(query, data)
    @classmethod
    def getSkeptics(cls, data):
        query="""
        SELECT users.first_name, users.last_name, users.id FROM
        scrutinize LEFT JOIN users ON users.id = scrutinize.users_id
        JOIN sightings ON sightings.id = scrutinize.sightings_id
        WHERE sightings_id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query, data)
        return results