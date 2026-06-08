from flask import Flask
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")

from backend.routes.auth_routes import auth_bp
from backend.routes.tender_routes import tender_bp
from backend.routes.compare_routes import compare_bp

app.register_blueprint(auth_bp)
app.register_blueprint(tender_bp)
app.register_blueprint(compare_bp)

if __name__ == "__main__":
    app.run(debug=True)