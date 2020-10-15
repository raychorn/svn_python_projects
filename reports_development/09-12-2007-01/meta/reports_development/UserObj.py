class UserObj(object):
    def __init__(self, id, session_id, name, email, hashed_password, username, remember_token_expires_at, remember_token, salt):
        self.id = id
        self.session_id = session_id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.username = username
        self.remember_token_expires_at = remember_token_expires_at
        self.remember_token = remember_token
        self.salt = salt
        
    def __repr__(self):
        return "<User(%r,%r,%r,%r,%r,%r,%r,%r,%r)>" % (self.id, self.session_id, self.name, self.email, self.hashed_password, self.username, self.remember_token_expires_at, self.remember_token, self.salt)
