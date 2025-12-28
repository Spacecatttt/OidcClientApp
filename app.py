import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, request, session, url_for

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = os.urandom(12)
oauth = OAuth(app)


app_config = {
    "CLIENT_ID": "client-carolyne-0x1da00e02",
    "CLIENT_SECRET": "9h8dptu7kjjb6h8et393gdyvscvsd83y",
    "ISSUER_URL": "https://localhost:9331",
    "SCOPES": "openid profile email",
}
# Redirect url =https://127.0.0.1:5000/auth


def register_oidc_client():
    """
    Clears old OIDC client and registers a new one with the current config.
    """
    # Remove previous 'oidc' client if it exists to allow reconfiguration
    if "oidc" in oauth._clients:
        oauth._clients.pop("oidc")

    oauth.register(
        name="oidc",
        client_id=app_config["CLIENT_ID"],
        client_secret=app_config["CLIENT_SECRET"],
        server_metadata_url=f"{app_config['ISSUER_URL']}/.well-known/openid-configuration",
        client_kwargs={"scope": app_config["SCOPES"], "verify": False},
    )


# --- Routes ---
@app.route("/")
def index():
    user_info = session.get("user_info")
    return render_template(
        "index.html",
        user=user_info,
        debug=app.debug,
        config=app_config,
    )


@app.route("/update_config", methods=["POST"])
def update_config():
    """
    Updates the global configuration from the form submission.
    """
    if not app.debug:
        return "Configuration changes are only allowed in Debug mode.", 403

    app_config["CLIENT_ID"] = request.form.get("client_id")
    app_config["CLIENT_SECRET"] = request.form.get("client_secret")
    app_config["ISSUER_URL"] = request.form.get("issuer_url")
    app_config["SCOPES"] = request.form.get("scopes")

    # Clear session to avoid using old tokens with new config
    session.clear()
    return redirect(url_for("index"))


@app.route("/login")
def login():
    # 1. Register the client dynamically with the latest config
    register_oidc_client()

    # 2. Start the flow
    redirect_uri = url_for("auth", _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri, code_challenge_method="S256")


@app.route("/auth")
def auth():
    """
    Callback route. Handles successful logins AND errors from IdentityServer.
    """
    error = request.args.get("error")
    if error:
        error_description = request.args.get("error_description")
        return render_template(
            "client_error.html", error=error, description=error_description
        )

    try:
        # Ensure the client is registered (in case server restarted during redirect)
        register_oidc_client()
        token = oauth.oidc.authorize_access_token()
        user_info = oauth.oidc.userinfo()
        session["user_info"] = user_info

        return redirect(url_for("index"))

    except Exception as e:
        # 3. Виловлюємо помилки бібліотеки Authlib (наприклад, MismatchingStateError)
        return render_template(
            "client_error.html", error="Internal Client Error", description=str(e)
        )


@app.route("/logout")
def logout():
    session.clear()
    logout_url = f"{app_config['ISSUER_URL']}/account/logout"
    return render_template("logout.html", logout_url=logout_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context="adhoc", debug=True)
