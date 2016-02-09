from flask import Flask

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"