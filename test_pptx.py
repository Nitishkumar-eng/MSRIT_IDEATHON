import pptx
import requests

prs = pptx.Presentation()
url = "http://127.0.0.1:8000/analyze"
with open('test_docs/template.pptx', 'rb') as template_file, \
     open('test_docs/target.pptx', 'rb') as target_file:
    files = {
        'template_file': template_file,
        'target_file': target_file
    }
    res = requests.post(url, files=files, timeout=10)
print(res.status_code)
print(res.text)
