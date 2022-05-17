from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Tree:
    db_name = 'treetrees'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.species = db_data['species']
        self.location = db_data['location']
        self.reason = db_data['reason']
        self.date_planted = db_data['date_planted']
        self.users_id = db_data['users_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO tree (species, location, reason, date_planted, users_id) VALUES (%(species)s,%(location)s,%(reason)s,%(date_planted)s,%(users_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tree;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_trees = []
        for row in results:
            print(row['species'])
            all_trees.append( cls(row) )
        return all_trees

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM tree WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_trees_by_id(cls,data):
        query = "SELECT * FROM tree where users_id = %(id)s;"
        results = connectToMySQL('treetrees').query_db(query,data)
        all_trees = []
        for row in results:
            all_trees.append( cls(row) )
        return all_trees

    @classmethod
    def get_one_with_trees(cls,data):
        query = "SELECT * FROM users LEFT JOIN tree on users.id = tree.users_id WHERE users.id=%(id)s;"
        results = connectToMySQL('treetrees').query_db(query,data)
        print(results)
        trees = cls(results[0])
        for row in results:
            n = {
                'id': row['tree.id'],
                'species': row['species'],
                'location': row['location'],
                'reason': row['reason'],
                'created_at': row['tree.created_at'],
                'updated_at': row['tree.updated_at'],
            }
            tree.tree.append( Tree(n) )
        return trees

    @classmethod
    def update(cls, data):
        query = "UPDATE tree SET species=%(species)s, location=%(location)s, reason=%(reason)s, date_planted=%(date_planted)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM tree WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_tree(tree):
        is_valid = True
        if len(tree["species"]) < 5:
            is_valid = False
            flash("Species must be at least 5 characters")
        if len(tree["location"]) < 2:
            is_valid = False
            flash("Location must be at least 2 characters")
        if len(tree["reason"]) > 50:
            is_valid = False
            flash("Reason can be a max of 50 characters")
        if tree["date_planted"] == "":
            is_valid = False
            flash("Please enter a date")
        return is_valid