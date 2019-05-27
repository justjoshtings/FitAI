# FitAI

## About
The goal of this project is to use data and advanced analytics to generate value and insights in fitness, health, and wellness. The majority of the data source will be data collected from a Fitbit device. 

This project will touch on many different areas including working with OAuth 2.0, REST APIs, data modeling, database management, ETLs, statistical analysis, and machine learning.

This repository will also include a custom built and fairly comprehensive method of working with Fitbit's API.

## 1. Fitbit API
1. Register an app with [Fitbit](https://dev.fitbit.com/apps/new).

2. Will need **ClientID**, **ClientSecret**, and the entered **Callback URI**.

3. Fitbit's API uses OAuth 2.0 for user-client app authentication. General steps for OAuth 2.0:
```
1. User interacts with client application interface.
2. Client app redirects the user to the Fitbit authorization page. 
3. If approved, Fitbit redirects the user to the app's callback URL with a temporary authorization code.
4. User delivers the temporary authorization code to the client.
5. The client app exchanges the temporary code for an access token and a refresh token to gain access to the user's data.
6. The client app can use the refresh token to refresh the access token after token expiration.
```
Fitbit also has a fairly detailed [API documentation](https://dev.fitbit.com/build/reference/web-api/basics/)
and a list of [REST API Endpoints](https://dev.fitbit.com/build/reference/web-api/explore/)

## Other Useful Resources and Documentation
Michael Gully-Santiago, PhD [How to download all of your raw fitbit data](https://towardsdatascience.com/how-to-download-all-of-your-raw-fitbit-data-d5bcf139d7ed)

[Requests](https://2.python-requests.org/en/master/user/quickstart/)

[Requests-OAuthLib OAuth 2.0](https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html)




