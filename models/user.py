from enum import unique
import peewee as pw
from models.base_model import BaseModel
import re

class User(BaseModel):
    username = pw.CharField(index=True, unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    hashed_password = pw.CharField(null=False)
    password = None
    profile_picture = pw.CharField(default='https://i.stack.imgur.com/l60Hf.png')

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username:
            self.errors.append('Username has been registered!')
        
        if duplicate_email:
            self.errors.append('Email has been registered!')

        if len(self.username.strip())==0:
            self.errors.append('Username cannot be blank!')

        if len(self.username.strip())>0 and len(self.username.strip())<8:
            self.errors.append('Username must have at least 8 characters!')
        
        if len(self.email.strip())==0:
            self.errors.append('Email cannot be blank!')

        if re.match("\w+@\w+.\w+", self.email):
            pass
        else:
            self.errors.append("Email format is not correct!")

        if self.password == None:
            pass
        else:
            if len(self.password.strip())==0:
                self.errors.append('Password cannot be blank!')

            elif len(self.password.strip())<8:
                self.errors.append('Password need at least 8 characters!')
            
            elif any(letter.isupper() for letter in self.password) and any(letter.islower() for letter in self.password) and any(re.search("\W{1,}", letter) for letter in self.password):
                pass

            else:
                self.errors.append('Password must consists of at least one uppercase, one lowercase and one special character')