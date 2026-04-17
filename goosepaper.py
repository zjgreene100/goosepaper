import os
import requests
from goose3 import Goose
from weasyprint import HTML
from rmapy.api import rMapyAPI

class Goosepaper:
    def __init__(self, config):
        self.config = config

    def fetch_articles(self):
        articles = []
        g = Goose()
        for source in self.config.get("sources", []):
            try:
                print(f"Fetching {source['url']}...")
                response = requests.get(source["url"], timeout=15)
                article = g.extract(raw_html=response.text)
                if article.cleaned_text:
                    articles.append({"title": article.title, "content": article.cleaned_text})
            except Exception as e:
                print(f"Failed to fetch: {e}")
        return articles

    def create_pdf(self, articles, output_file):
        html_content = "<html><style>body{font-family:serif;padding:2em;} h1{border-bottom:2px solid black;}</style><body><h1>Daily News</h1>"
        for art in articles:
            html_content += f"<h2>{art['title']}</h2><p>{art['content']}</p><hr>"
        html_content += "</body></html>"
        HTML(string=html_content).write_pdf(output_file)

    def upload_to_remarkable(self, file_path, auth_token):
        rm = rMapyAPI()
        rm.renew_token(auth_token)
        with open(file_path, "rb") as f:
            rm.upload(f, remote_path="/")
