import argparse
import json
import os
import sys

# Add current directory to path so it can find the other file
sys.path.append(os.getcwd())
from goosepaper.goosepaper import Goosepaper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="DailyPaper.pdf")
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    gp = Goosepaper(config)
    print("Starting news fetch...")
    articles = gp.fetch_articles()
    
    if not articles:
        print("No articles found. Check your config.json URLs.")
        return

    print(f"Generating PDF: {args.output}")
    gp.create_pdf(articles, args.output)

    if args.upload:
        token = os.environ.get("REMARKABLE_AUTH_TOKEN")
        print("Attempting to upload to reMarkable...")
        gp.upload_to_remarkable(args.output, token)
        print("Success! Check your tablet.")

if __name__ == "__main__":
    main()
