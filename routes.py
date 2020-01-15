from config import app
from controller_functions import index, login, new_user, create_user, home

app.add_url_rule('/', view_func=index)
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/new_user', view_func=new_user)
app.add_url_rule('/create_user', view_func=create_user, methods=['POST'])
app.add_url_rule('/home', view_func=home)