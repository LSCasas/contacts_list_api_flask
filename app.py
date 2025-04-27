import os
from contacts_list import create_app

app = create_app()

@app.route('/')
def status():
    return "API is up and running"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port)
