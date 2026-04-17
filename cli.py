import argparse
import json
import os
from .goosepaper import Goosepaper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="DailyPaper.pdf")
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    gp = Goosepaper(config)
    print("Fetching articles...")
    articles = gp.fetch_articles()
    
    print(f"Generating PDF: {args.output}")
    gp.create_pdf(articles, args.output)

    if args.upload:
        token = os.environ.get("REMARKABLE_AUTH_TOKEN")
        if not token:
            print("Error: REMARKABLE_AUTH_TOKEN not found in environment.")
            return
        print("Uploading to reMarkable...")
        gp.upload_to_remarkable(args.output, token)
        print("Done!")

if __name__ == "__main__":
    main()
