from app import app
from os import environ



port = 5000

if "PORT" in environ:
  port = int(environ["PORT"])

app.debug = True
app.run(host='0.0.0.0', port=port)
