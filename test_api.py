import requests
import json

BASE_URL = 'http://localhost:5000'

def test_home():
    response = requests.get(f'{BASE_URL}/')
    print("Testing Home Route:")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    print("\n")

def test_create_post():
    url = f'{BASE_URL}/api/posts'
    data = {
        'title': 'Test Post with Image',
        'content': 'This is a test post content including an image URL.',
        'image': 'https://example.com/test-image.jpg'  # Include an image URL here
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    print("Testing Create Post:")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    print("\n")

def test_get_posts():
    url = f'{BASE_URL}/api/posts'
    response = requests.get(url)
    print("Testing Get Posts:")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    print("\n")

if __name__ == '__main__':
    print("Starting API Tests...\n")
    test_home()
    test_create_post()
    test_get_posts()
