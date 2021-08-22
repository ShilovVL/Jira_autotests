def test_create_business_project():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T101'
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_business_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",
        "name": "TMP business test project1",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "business",
        "key": tkey
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)
    error = 0
    if 'key' in r:
        if r['key'] == tkey:
            print(' Проект ', '"' + json.loads(payload)['name'] + '"', ' ID', r['id'], ' создан', end='')
    assert json.loads(payload)['name'] == "TMP business test project1"
    assert 'errors' not in r
    assert r['key'] == tkey


def test_create_business_project_duplicate_name_negative():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T103'
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_business_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",
        "name": "TMP business test project1",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "business",
        "key": tkey
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)

    if 'key' in r:
        if r['key'] == tkey:
            print(' Проект ', '"' + json.loads(payload)['name'] + '"', ' ID', r['id'], ' создан', end='')

    # print(r['errors']['projectName'])
    print(' ', r['errors']['projectName'], end='')

    assert 'errors' in r


def test_create_business_project_long_key_negative():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T12345678910'  # более 10 символов нельзя
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_business_project long key",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",
        "name": "TMP business test project long key",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "business",
        "key": tkey
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)

    if 'key' in r:
        if r['key'] == tkey:
            print(' Проект ', '"' + json.loads(payload)['name'] + '"', ' ID', r['id'], ' создан', end='')
    print(' ', r['errors']['projectKey'], end='')
    # print(r['errors']['projectName'])
    # print(' ', r['errors']['projectName'], end='')

    assert 'errors' in r


def test_create_scrum_project_positive():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T201'
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",
        "name": "TMP SCRUM test project1",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "software",
        "key": tkey
    })
    # "projectTypeKey":  software,  business
    # "permissionScheme": 10000, #     "categoryId": 10000
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)
    if r['key'] == tkey:
        print(' Проект ID', r['id'], '"' + json.loads(payload)['name'] + '"', ' по шаблону "SCRUM" создан', end='')

    # print(type(r), r['key'], '\n', r)
    assert json.loads(payload)['name'] == "TMP SCRUM test project1"
    assert 'errors' not in r
    assert r['key'] == tkey


def test_create_scrum_project_duplicate_key_negative():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T201'
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",
        "name": "TMP SCRUM test project2",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "software",
        "key": tkey
    })
    # "projectTypeKey":  software,  business
    # "permissionScheme": 10000, #     "categoryId": 10000
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)

    if 'key' in r and r['key'] == tkey:
        print(' Проект ID', r['id'], '"' + json.loads(payload)['name'] + '"', ' по шаблону "SCRUM" создан', end='')
    else:
        print('', r['errors']['projectKey'], end='')
    assert response.status_code == 400, f"Неверный код ответа, получен {response.status_code}"
    assert 'errors' in r


def test_create_scrum_project_empty_key_negative():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = ''
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum",
        "name": "TMP SCRUM test project2",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "software",
        "key": tkey
    })
    # "projectTypeKey":  software,  business
    # "permissionScheme": 10000, #     "categoryId": 10000
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)

    if 'key' in r and r['key'] == tkey:
        print(' Проект ID', r['id'], '"' + json.loads(payload)['name'] + '"', ' по шаблону "SCRUM" создан', end='')
    else:
        print('', r['errors']['projectKey'], end='')
    assert response.status_code == 400, f"Неверный код ответа, получен {response.status_code}"
    assert 'errors' in r


def test_create_kanban_project_positive():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T301'
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic",
        "name": "TMP KANBAN test project1",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "software",
        "key": tkey
    })
    # "projectTypeKey":  software, service_desk, business
    # "permissionScheme": 10000, #     "categoryId": 10000
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)
    if 'key' in r and r['key'] == tkey:
        print(' Проект ID', r['id'], '"' + json.loads(payload)['name'] + '"', ' по шаблону "KANBAN" создан', end='')

    # print(type(r), r['key'], '\n', r)
    assert 'errors' not in r
    assert json.loads(payload)['name'] == "TMP KANBAN test project1"
    assert r['key'] == tkey


def test_create_kanban_project_duplicate_key_and_name_negative():
    import requests
    from requests.auth import HTTPBasicAuth
    import json
    tkey = 'T301'
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic",
        "name": "TMP KANBAN test project1",

        "assigneeType": "PROJECT_LEAD",
        "projectTypeKey": "software",
        "key": tkey
    })
    # "projectTypeKey":  software, service_desk, business
    # "permissionScheme": 10000, #     "categoryId": 10000
    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)
    if 'key' in r and r['key'] == tkey:
        print(' Проект ID', r['id'], '"' + json.loads(payload)['name'] + '"', ' по шаблону "KANBAN" создан', end='')
    else:
        print('', r['errors']['projectKey'], r['errors']['projectName'], end='')

    assert 'errors' in r


#  Удаляем тестируемый проект - заканчиваем тест свиту
def test_delete_test_projects():
    import requests
    from requests.auth import HTTPBasicAuth
    import json

    projects_key = ['T101', 'T201', 'T301']
    for tkey in projects_key:
        url = "https://mytestsite1.atlassian.net/rest/api/2/project/" + str(tkey)

        auth = HTTPBasicAuth("shilovv@sibnet.ru", "*******")

        response = requests.request(
            "DELETE",
            url,
            auth=auth
        )

        # print(r['errorMessages'][0])
        if response.status_code != 204:
            r = json.loads(response.text)
            print(r['errorMessages'][0])
        else:
            print(" Проект", tkey, "успешно удален", end='.')
        # print(response.status_code)
        assert response.status_code == 204
