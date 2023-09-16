from app import app
from app import database


if __name__ == "__main__":
    app.run(port=5000, debug=True)
