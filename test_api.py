import requests

url = "http://127.0.0.1:8000/analyze"
with open('test_docs/template.docx', 'rb') as template_file, \
     open('test_docs/target.docx', 'rb') as target_file:
    files = {
        'template_file': template_file,
        'target_file': target_file
    }
    response = requests.post(url, files=files, timeout=10)

print(f"Status Code: {response.status_code}")
try:
    print(response.json())
except Exception:
    print(response.text)
