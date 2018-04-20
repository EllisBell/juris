import requests
import time

headers = {'User-Agent': 'Mozilla/5.0'}


def check_page_not_found(url):
    req = requests.head(url, headers=headers)
    # Only want to delete if page doesn't exist - 404 error
    return req.status_code == 404


def get_page_content(url):
    r = requests.get(url, headers=headers)
    return r.content


# try for number of attempts, catching request exceptions
# if pass max attempts, raise the exception
def try_get_page_content(url, max_attempts, wait_time):
    attempts = 0
    while True:
        try:
            time.sleep(wait_time)
            attempts += 1
            content = get_page_content(url)
            return content
        except requests.exceptions.RequestException as e:
            # todo log exception
            print("exception requesting " + url + ": " + str(e))
            if attempts == max_attempts:
                raise
