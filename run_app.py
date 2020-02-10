import os
from colorjeopardy import app, server

server = server
app = app

if __name__ == "__main__":
    app.server.secret_key = os.urandom(24)
    app.run_server(debug=True)
