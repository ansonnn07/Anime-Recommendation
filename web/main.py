from website import create_app
from website.config import Config

app = create_app()

# Run this command to run the application in DEBUG mode
# docker run -p 5000:5000 -e DEBUG=1 <image-name>
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
