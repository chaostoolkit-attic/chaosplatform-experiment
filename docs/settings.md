# Server settings

The service is configured via environment variables which must be present in
the shell where you are running it from, or from a simple [.env][dotenv] file.

[dotenv]: https://pypi.org/project/python-dotenv/

You will find an example of such file in the repository.

## Configuration Keys

| Key                       | Default           | Required | Description                                        | 
|---------------------------|-------------------|----------|----------------------------------------------------|
| SERVER_LISTEN_ADDR        | "0.0.0.0"       | Yes      | The IP of the interface to bind the HTTP server to |
| SERVER_LISTEN_PORT        | 11080              | Yes      | The port to bind the HTTP server to                |
| HTTP_PROXY_BASE           |                   | No       | The base URL of the domain this service is attached|
| SECRET_KEY                |                   | Yes      | The key used to sign session cookies               |
| GRPC_LISTEN_ADDR          | "0.0.0.0:50051" | Yes      | The address to bind the GRPC server to             |
| DATABASE_URI              | "sqlite://"       | Yes      | The database connection URI for the store          |
| ACCOUNT_SERVICE_GRPC_ADDR | "0.0.0.0:50052" | Yes      | The address of the account gRPC service            |
| JWT_SECRET_KEY            |                   | Yes      | The key used to encode JWT tokens                  |
| JWT_ACCESS_TOKEN_EXPIRES  | 518400            | Yes      | The JWT expiricy timeout in seconds                |
| AUTH_GITHUB_CLIENT_ID     |                   | Yes      | The GitHub OAuth2 client id                        |
| AUTH_GITHUB_CLIENT_SECRET |                   | Yes      | The GitHub OAuth2 client secret                    |

A few remarks:

* Use strong keys for `SECRET_KEY` and `JWT_SECRET_KEY` but be-aware that
changing them means existing signed values will not work anymore. Be very
careful not to change them lightly.

* `AUTH_GITHUB_CLIENT_ID` and `AUTH_GITHUB_CLIENT_SECRET` are sensitive data
so you may need to consider ensuring the file is only readable by the process.