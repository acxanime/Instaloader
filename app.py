# © Coded by @Dypixx

from flask import Flask, Response
import requests
app = Flask(__name__)
@app.route('/')
def show_github_html():
    response = requests.get('https://raw.githubusercontent.com/Dypixx/live/main/index.html')
    return Response(response.text, mimetype='text/html') if response.status_code == 200 else ("Bot is LIVE", 500)
if __name__ == "__main__":
    app.run()

"""
This code is created and owned by @Dypixx. Do not remove or modify the credit.

Removing the credit does not make you a developer; it only shows a lack of respect for real developers.
  
Respect the work. Keep the credit.

"""
