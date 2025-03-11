from app.routes.category import bp as category_bp

def init_app(app):
    app.register_blueprint(category_bp)