import os
from google_auth_oauthlib.flow import Flow

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]

def get_google_flow():
    # FORCE PROJECT ROOT (MOST RELIABLE METHOD)
    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    )

    credentials_path = os.path.join(
        base_dir,
        "credentials",
        "google_credentials.json"
    )

    print("DEBUG PATH:", credentials_path)  # IMPORTANT DEBUG LINE

    return Flow.from_client_secrets_file(
        credentials_path,
        scopes=GOOGLE_SCOPES,
        redirect_uri="http://127.0.0.1:8000/api/gmail/oauth/callback/"
    )