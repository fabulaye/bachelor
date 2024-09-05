import wrds

def start_connection():
    connection=wrds.Connection(wrds_username="lukasmeyer")
    return connection


def close_connection(connection):
    connection.close()

