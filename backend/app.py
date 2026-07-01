from flask import Flask
from flask_cors import CORS

from routes.upload import upload_bp
from routes.github_routes import github_bp  
from routes.repository import repository_bp
app = Flask(__name__)

CORS(app)

app.register_blueprint(upload_bp)
app.register_blueprint(repository_bp)
app.register_blueprint(github_bp)


@app.route("/")
def home():
    return {"message": "AI Code reviewer Backend Running"}


if __name__ == "__main__":
    app.run(debug=True)