# This file is used by gunicorn to run our server

from live_run import server

if __name__ == "__main__":
    server.run()
