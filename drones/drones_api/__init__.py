from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # existing code omitted
    from . import view
    app.register_blueprint(view.bp)

    return app