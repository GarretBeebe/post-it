import os
import sys
import argparse
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
from atproto import Client as BlueskyClient

def post_to_facebook(text, image_path, audience='public'):
    token = os.getenv("FB_ACCESS_TOKEN")
    page_id = os.getenv("FB_PAGE_ID")
    url = f"https://graph.facebook.com/{page_id}/photos"

    with open(image_path, 'rb') as img:
        privacy = {'value': 'ALL_FRIENDS' if audience == 'friends' else 'EVERYONE'}
        r = requests.post(url, 
        files={'source': img}, 
        data={'access_token': token, 'caption': text, 'privacy': str(privacy)})
        
    print("Facebook:", r.status_code, r.text)

def post_to_x(text, image_path):
    auth = OAuth1(
        os.getenv("X_API_KEY"), 
        os.getenv("X_API_SECRET"),
        os.getenv("X_ACCESS_TOKEN"), 
        os.getenv("X_ACCESS_TOKEN_SECRET"))
    
    upload = requests.post(
        "https://upload.twitter.com/1.1/media/upload.json",
        files={'media': open(image_path, 'rb')}, auth=auth)
    
    media_id = upload.json()['media_id_string']

    post = requests.post(
        "https://api.twitter.com/1.1/statuses/update.json",
        data={'status': text, 'media_ids': media_id}, 
        auth=auth)
    
    print("X:", post.status_code, post.text)

def post_to_bluesky(text, image_path):
    client = BlueskyClient()
    client.login(os.getenv("BSKY_HANDLE"), os.getenv("BSKY_APP_PASSWORD"))
    client.send_post(text=text, embed_image_path=image_path)
    print("BlueSky: Post successful")

def post_to_substack(text):
    print("Substack (simulated):", text[:60] + "...")

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Post to social media from the CLI.")
    parser.add_argument("text", help="Text of the post")
    parser.add_argument("-i", "--image", help="Image file path (required for most services)")
    parser.add_argument("--facebook", action="store_true")
    parser.add_argument("--x", action="store_true")
    parser.add_argument("--bluesky", action="store_true")
    parser.add_argument("--substack", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument('--fb-audience', choices=['public', 'friends'], default='public', help='Facebook audience setting')

    args = parser.parse_args()

    if not args.image and not args.substack:
        print("Image required for selected platforms.")
        sys.exit(1)

    if args.all or args.facebook:
        post_to_facebook(args.text, args.image, args.fb_audience)
    if args.all or args.x:
        post_to_x(args.text, args.image)
    if args.all or args.bluesky:
        post_to_bluesky(args.text, args.image)
    if args.all or args.substack:
        post_to_substack(args.text)
