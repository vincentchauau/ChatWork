from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='113984963736-smpju8fu9bcfkapqo9msjb3ptelm53or.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    return 'Welcome! <a href="/login/google">Login with Google</a>'

@app.route('/login/google')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout/google')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/google/authorized')
def authorized():
    resp = google.authorized_response()
    if resp and resp.get('access_token'):
        session['google_token'] = (resp['access_token'], '')
        user_info = google.get('userinfo')
        return 'Logged in as: {}'.format(user_info.data['email'])
    
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)
