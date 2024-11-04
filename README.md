

App deployed at https://tasty-recipe-network.fly.dev/docs

How to run
Requires Docker

Download repo

Create .env file in root with the following values

    ENVIRONMENT=DEV
    SECRET_KEY = < openssl rand -hex 32

Run commands

    docker compose build
    docker compose up

app available at http://localhost:8080/docs
