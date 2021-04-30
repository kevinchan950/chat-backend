from app import app, csrf

from chat_api.sessions.views import sessions_api_blueprint
from chat_api.users.views import users_api_blueprint

app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

csrf.exempt(sessions_api_blueprint)
csrf.exempt(users_api_blueprint)