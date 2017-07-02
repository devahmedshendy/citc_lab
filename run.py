from app import app

import os

if os.environ["PORT"]:
  port = int(os.environ["PORT"])

else:
  port = 5000

app.debug = True
app.run(host='0.0.0.0', port=port)
