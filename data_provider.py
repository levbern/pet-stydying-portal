from flask import Flask
import json

app = Flask(__name__)

def get_user(id):
    user_path = "sources/users/user_%s.json" % id
    with open(user_path, 'r', encoding='utf-8') as json_file:
        user_data = json.load(json_file)
    return user_data

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")

