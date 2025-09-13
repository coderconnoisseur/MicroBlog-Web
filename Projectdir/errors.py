from Projectdir import app,db
from flask import render_template, jsonify, request

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors"""
    if request.is_json:
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': str(e.description),
            'retry_after': e.retry_after
        }), 429
    else:
        return render_template('429.html', 
                             error=e.description,
                             retry_after=e.retry_after), 429