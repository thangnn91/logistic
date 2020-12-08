from flask_login import UserMixin
class User(UserMixin):

    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.urole = role
    
    
    def get_name(self):
        return self.username
    
    def get_urole(self):
        return self.urole
        
    def __repr__(self):
        return self.id

    def get_id(self):
        return self.id
    
       