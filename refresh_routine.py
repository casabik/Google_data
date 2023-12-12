from google_auth_oauthlib.flow import InstalledAppFlow

client_id = '138454643883-eps8db9mo17c9l6bam5ah6c3juq0rred.apps.googleusercontent.com'
client_secret = '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'
scopes = ['https://www.googleapis.com/auth/adwords']

flow = InstalledAppFlow.from_client_secrets_file('client_secret My Project 43000.json',
                                                 scopes=scopes,
                                                 redirect_uri="http://localhost")

credentials = flow.run_local_server()

print(f"Refresh token: {credentials.refresh_token}")
