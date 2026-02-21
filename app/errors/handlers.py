from flask import render_template
from . import errors_bp

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('error/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error/500.html'), 500
