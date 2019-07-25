
import requests, urlparse
from BeautifulSoup import BeautifulSoup


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "website/ip"
response = request(target_url)

parsed_html = BeautifulSoup(response.content)
forms_list = parsed_html.findAll("form")
for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    print(" Action: " + action)
    print(" Post URL: " + post_url)
    method = form.get("method")
    print(" Method: " + method)
    inputs_list = form.findAll("input")

    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        print(" Input Name: " + input_name)
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result.content)
