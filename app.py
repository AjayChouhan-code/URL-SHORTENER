from flask import Flask, request, jsonify, redirect, abort
from services.url_services import URLService

app = Flask(__name__)
url_service = URLService()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    POST /shorten
    Shortens a given original URL. If the same URL is provided again,
    it returns the same short URL as before.

    Request JSON:
    {
        "url": "https://example.com"
    }

    Response JSON (on success):
    {
        "data": {
            "short_url": "http://localhost:5000/abc123"
        },
        "status": 200,
        "message": "Short URL generated successfully",
        "error": false
    }

    Response JSON (on error):
    {
        "data": {},
        "status": 400/500,
        "message": "Error message",
        "error": true
    }
    """
    try:
        data = request.get_json()
        original_url = data.get('url')

        if not original_url:
            return jsonify({
                "data": {},
                "status": 400,
                "message": "URL is required",
                "error": True
            }), 400

        short_url = url_service.shorten(original_url)

        return jsonify({
            "data": {"short_url": request.host_url + short_url},
            "status": 200,
            "message": "Short URL generated successfully",
            "error": False
        }), 200

    except Exception as e:
        return jsonify({
            "data": {},
            "status": 500,
            "message": f"Error occurred: {str(e)}",
            "error": True
        }), 500

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    """
    GET /<short_url>
    Redirects the user to the original URL based on the provided short URL.

    URL Parameter:
        short_url (str): The shortened URL key.

    Redirects:
        - To the original URL if found.
        - Returns 404 if the short URL is not found.
    """
    original_url = url_service.get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return abort(404)

@app.route('/metrics', methods=['GET'])
def metrics():
    """
    GET /metrics
    Returns the top 3 domain names that have been shortened the most.

    Response JSON:
    {
        "youtube.com": 4,
        "udemy.com": 3,
        "wikipedia.org": 2
    }
    """
    top_domains = url_service.get_top_domains()
    return jsonify({domain: count for domain, count in top_domains})

if __name__ == '__main__':
    """
    Entry point of the Flask application.
    Starts the development server with debug mode enabled.
    """
    app.run(debug=True)