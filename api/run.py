from app import app
from instance.config import config

# import import pdb; pdb.set_trace()
if __name__ == "__main__":
	app.run(debug=True, host='127.0.0.1', port=5000)
