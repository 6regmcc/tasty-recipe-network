import os


def test_load_env_vars_pytest_env():
    assert os.environ["ENVIRONMENT"] == "TEST"
    assert (
        os.environ["SECRET_KEY"]
        == "9f6d389daa1829e2a8757d92f7fb6068317b7c2a9a6927357cd314adc2e96a72"
    )
    assert (
        os.environ["DATABASE_URL"]
        == "postgresql+psycopg://postgres:postgres@localhost:5456/postgres"
    )
