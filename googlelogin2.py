import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)
app.secret_key = "supersekrit"
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
blueprint = make_google_blueprint(
    client_id="103178889954-jn7h5oipfmv7qmol1br5ju95lctqrolg.apps.googleusercontent.com",
    client_secret="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",
    scope=['email', 'profile'],
)
app.register_blueprint(blueprint, url_prefix="/login")
@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    else:
        resp = google.get("/oauth2/v3/userinfo")
        if resp.ok:
            user_info = resp.json()
            name = user_info['name']
            email = user_info['email']
            return f"You are {name} {email} on Google"
        else:
            return "Failed to fetch user info"

if __name__ == "__main__":
    app.run(ssl_context=('localhost.pem', 'localhost-key.pem'), debug=True)
