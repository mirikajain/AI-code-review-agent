from flask import Flask
from flask_cors import CORS

from routes.upload import upload_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(upload_bp)


@app.route("/")
def home():
    return {"message": "AI Code reviewer Backend Running"}


if __name__ == "__main__":
    app.run(debug=True)