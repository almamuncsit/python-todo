from app.routes.category import bp as category_bp
from app.routes.task import bp as task_bp

def init_app(app):
    app.register_blueprint(category_bp)
    app.register_blueprint(task_bp)