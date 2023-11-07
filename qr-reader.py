import cv2
import requests
import validators
import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def detectQR():
    # Sets the default
    camera_id = 0
    delay = 1
    window_name = 'OpenCV QR Code'

    # Creates a QRCodeDetector + VideoCapture object
    qcd = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(camera_id)


    # Basically just an infinite loop
    goodLink = True
    url = ''

    while goodLink:
        ret, frame = cap.read()

        if ret:
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            if ret_qr:
                for s, p in zip(decoded_info, points):
                    if s:
                        print("Found QR Code: " + s)
                        url = s
                        color = (0, 255, 0)
                        cv2.destroyWindow(window_name)
                        return url

                    else:
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
            cv2.imshow(window_name, frame)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    # Now destroys the
    cv2.destroyWindow(window_name)

# Function that given an QR string, calls all of the other detections to see if they want to be detected or not
def analyseQR(url):
    print("Analysing...")

    # Checking that it's in a valid format
    if validators.url(url):
        print("This url is in the correct format")
    else: 
        print("This url is not in a valid format")
    
    if scan_xss(url):
        print("This url is vulnerable to XXS")
    else:
        print("This url is not vulnerable to XXS")
    
    
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    # get the form action (target url)
    action = form.attrs.get("action", "").lower()
    # get the form method (POST, GET, etc.)
    method = form.attrs.get("method", "get").lower()
    # get all the input details such as type and name
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    # construct the full URL (if the url provided in action is relative)
    target_url = urljoin(url, form_details["action"])
    # get the inputs
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # replace all text and search values with `value`
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            # if input name and value are not None, 
            # then add them to the data of form submission
            data[input_name] = input_value

    print(f"[+] Submitting malicious payload to {target_url}")
    print(f"[+] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # GET request
        return requests.get(target_url, params=data)
    
def scan_xss(url):
    # get all the forms from the URL
    forms = get_all_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<Script>alert('hi')</scripT>"
    # returning value
    is_vulnerable = False
    # iterate over all forms
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
            # won't break because we want to print available vulnerable forms
    return is_vulnerable


# The script that actually runs currently
url = detectQR()
user_input = input("Continue with analysis? (Y/N): ")
while (user_input != "Y"):
    url = detectQR()
analyseQR(url)
