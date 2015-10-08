# docsql
django mysql google drive api oauth2

An oauth2 authorization using google api with permissions to drive files along with a file download

Create an account on Google Developers and download your JSON credentials from the dev console.


    Open the Credentials page.
    If you haven't done so already, create your project's OAuth 2.0 credentials by clicking Add credentials > OAuth 2.0 client ID, and providing the information needed to create the credentials.
    Look for the Client ID in the OAuth 2.0 client IDs section. You can click the client ID for details.



{"web":{"client_id":"YOUR-GOOGLE.apps.googleusercontent.com",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":"o8sbye58o374tyd93j8e","redirect_uris":["http://localhost:8000/oauth2callback"],
    "javascript_origins":["http://localhost","http://localhost:8000"]}}
