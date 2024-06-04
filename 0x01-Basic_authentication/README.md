This project implements a basic authentication system for a simple API. You'll learn about authentication mechanisms, Base64 encoding, and user credentials.

Learning Objectives

Explain general authentication concepts.
Understand Base64 encoding and decoding.
Implement Basic Authentication.
Requirements

Python 3.7
Ubuntu 18.04 LTS
Text editor or IDE
Git version control
Tasks

Download and Start the Project

Download the project archive from the provided link.
Unzip the archive and navigate to the project directory.
Install required dependencies using pip3 install -r requirements.txt.
Start the API server using python3 -m api.v1.app.
Error Handlers

Implement error handlers for unauthorized requests (401) and forbidden requests (403).
The error handlers should return a JSON response with the appropriate error message and status code.
Authentication Class

Create a class named Auth in the api/v1/auth directory.
Define methods for checking if a request requires authentication, retrieving the authorization header, and retrieving the current user.
Authentication Logic

Update the Auth class methods to handle authentication logic.
Define which routes don't require authentication (e.g., status endpoint).
Validate all requests to ensure they include the necessary headers.
Basic Authentication

Create a subclass named BasicAuth that inherits from Auth.
Implement methods for extracting, decoding, and validating Base64 encoded authorization headers.
Use these methods to extract user credentials (email and password) from the authorization header.
User Object and Credentials

Implement methods in BasicAuth to retrieve the user object based on email and password from your user database (file).
Ensure proper handling of cases where the user is not found or the password is incorrect.
Complete Basic Authentication

Update the API application (api/v1/app.py) to use the BasicAuth class for authentication.
Use environment variables to switch between authentication types (e.g., AUTH_TYPE=basic_auth).
Testing

Use curl or another tool to send requests to your API and verify the authentication behavior. Test different scenarios, including:

Unauthenticated requests
Incorrect authorization headers
Invalid credentials
