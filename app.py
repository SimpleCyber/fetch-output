from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        # Fetch the URL content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the title of the webpage
        title = soup.title.string if soup.title else "No Title Found"
        
        # Get all the links on the page
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # Get all images on the page
        images = [img['src'] for img in soup.find_all('img', src=True)]

        # Extract the text content
        text = soup.get_text()

        # Return structured data
        return jsonify({
            "title": title,
            "content": text[:1000] + "..." if len(text) > 1000 else text,
            "links": links,
            "images": images,
            "raw_html": response.text  # This is the full HTML content
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch the URL: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
