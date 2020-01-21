from config import app
from controller_functions import index, login, new_user, create_user, ongoing, render_lists, find, unfind, new_plate, home, trip_detail, start_trip, trip_time, end_trip, logout

app.add_url_rule('/', view_func=index)
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/new_user', view_func=new_user)
app.add_url_rule('/create_user', view_func=create_user, methods=['POST'])
app.add_url_rule('/ongoing', view_func=ongoing)
app.add_url_rule('/render_lists', view_func=render_lists)
app.add_url_rule('/find/<id>', view_func=find)
app.add_url_rule('/unfind/<id>', view_func=unfind)
app.add_url_rule('/new_plate', view_func=new_plate, methods=['POST'])
app.add_url_rule('/home', view_func=home)
app.add_url_rule('/trip_detail/<id>', view_func=trip_detail)
app.add_url_rule('/start_trip', view_func=start_trip, methods=['POST'])
app.add_url_rule('/trip_time', view_func=trip_time)
app.add_url_rule('/end_trip/<id>', view_func=end_trip)
app.add_url_rule('/logout', view_func=logout)