def test_api_login():
    import requests
    from requests.auth import HTTPBasicAuth

    url = "https://mytestsite1.atlassian.net/rest/api/3/project"

    auth = HTTPBasicAuth("", "***API token****")
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    if str(response) == '<Response [200]>':
        print(' Авторизация удачно - код: ', str(response.status_code), end='')
    assert str(response) == '<Response [200]>'


def test_login_web_selenium_positive():
    from selenium import webdriver
    import time

    link = "https://id.atlassian.com/login"

    try:
        browser = webdriver.Chrome()
        browser.get(link)

        browser.find_element_by_id('username').send_keys('my@email.com')
        browser.find_element_by_id('login-submit').click()
        time.sleep(1)
        browser.find_element_by_id('password').send_keys('jirabynfyn')
        browser.implicitly_wait(10)
        browser.find_element_by_id('login-submit').click()
        time.sleep(6)

        assert "Atlassian | Start page" in browser.title
        print(' Авторизация удачно - открыта страница: ', browser.title, end='')
    finally:

        time.sleep(3)
        browser.quit()


def test_api_anonymous_login_negative():
    import requests
    from requests.auth import HTTPBasicAuth

    url = "https://mytestsite1.atlassian.net/rest/api/3/project"

    auth = HTTPBasicAuth("anonymous", "")
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    if str(response) == '<Response [401]>':
        print(' Авторизация НЕудачно - код: ', str(response.status_code), end='')


    assert str(response) == '<Response [401]>'


def test_api_random_token_login_negative():
    import secrets
    import requests
    from requests.auth import HTTPBasicAuth
    secret_token = secrets.token_hex(nbytes=12)
    url = "https://mytestsite1.atlassian.net/rest/api/3/project"

    auth = HTTPBasicAuth("", secret_token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    if str(response) == '<Response [401]>':
        print(' Авторизация НЕудачно - код: ', str(response.status_code), " Токен:", secret_token,  end='')
    assert str(response) == '<Response [401]>'


def test_api_SQL_injection_login_negative():
    import requests
    from requests.auth import HTTPBasicAuth

    url = "https://mytestsite1.atlassian.net/rest/api/3/project"
    sql_inj = [
        "' OR 1=1--",
        '" OR 1=1--',
        ' OR 1=1--',
        "' OR 'a'='a",
        '" OR "a"="a',
        "') OR ('a'='a",
        " OR '1'='1'"]
    for s in sql_inj:
        auth = HTTPBasicAuth("Anonymous"+s, "")
        headers = {
        "Accept": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )

        if str(response) != '<Response [401]>':
            print(' Авторизация удачно - код: ', str(response.status_code), end='')
            break
    print(' Авторизация НЕудачно - код: ', str(response.status_code), end='')

    assert str(response) == '<Response [401]>'

