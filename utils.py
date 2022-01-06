import requests
from gql import Client
from gql.transport.requests import RequestsHTTPTransport


def get_jwt(domain, client_id, client_secret):
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.post(f"{domain}/oauth/token/", headers=headers, data=data)
    return response.json()


def get_client(domain, client_id, client_secret):
    jwt = get_jwt(domain, client_id, client_secret)
    transport = RequestsHTTPTransport(
        url=f"{domain}/graphql",
        headers={"Authorization": f'Bearer {jwt["access_token"]}'},
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client
