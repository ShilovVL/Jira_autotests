import requests
from requests.auth import HTTPBasicAuth
import json
import pytest

# my constants
admin_name = 'Василий Шилов'  # project owner
mylogin = "shilovv@sibnet.ru"  # your email as jira login
mypass = "Iv4dfcGlvODzhtHJYemH5681"  # your jira api token
tkey = 'TK02'  # key for temp testproject
tname = "TMP SCRUM test project for test issues"  # tmp name testproject


def find_board_id(tkey):
    url = "https://mytestsite1.atlassian.net/rest/agile/1.0/board"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    r = json.loads(response.text)

    for i in range(len(r["values"])):

        if r["values"][i]['location']['projectKey'] == tkey:
            return r["values"][i]['id']


def get_list_all_issues_in_project(tkey):
    url = "https://mytestsite1.atlassian.net/rest/api/3/search"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    query = {
        'jql': 'project = ' + str(tkey)
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    issues_id = []
    r = json.loads(response.text)
    assert response.status_code == 200
    # print('      Найдено', len(r['issues']), 'задач:', end=' ')
    for i in range(len(r['issues'])):
        # if str(r['issues'][i]['fields']['summary']) == 'REST EXAMPLE':
        #     print(i, r['issues'][i]['fields']['summary'])
        if r['issues'][i]['fields']['issuetype']['name'] != 'Эпик' and r['issues'][i]['fields']['issuetype'][
            'name'] != 'Epic':
            issues_id.append(r['issues'][i]['id'])
    return issues_id


def get_list_all_epic_issues_in_project(tkey):
    url = "https://mytestsite1.atlassian.net/rest/api/3/search"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    query = {
        'jql': 'project = ' + str(tkey)
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    issues_id = []
    r = json.loads(response.text)
    assert response.status_code == 200
    # print('      Найдено', len(r['issues']), 'задач:', end=' ')
    for i in range(len(r['issues'])):

        if r['issues'][i]['fields']['issuetype']['name'] == 'Эпик' or r['issues'][i]['fields']['issuetype'][
            'name'] == 'Epic':
            issues_id.append(r['issues'][i]['id'])
    return issues_id


def test_create_kanban_project():
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth(mylogin, mypass)

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
        "name": "TMP KANBAN test project",

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
    if r['key'] == tkey:
        print(' Проект ID', r['id'], ' по шаблону "KANBAN" создан', end='')

    # print(type(r), r['key'], '\n', r)
    assert r['key'] == tkey


def test_create_and_get_epic_issue_in_kanban_project():
    url = "https://mytestsite1.atlassian.net/rest/api/2/issue"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project":
                {
                    "key": tkey
                },
            "summary": "REST EPIC EXAMPLE",
            "description": "Creating an issue via REST API",
            "issuetype": {
                "name": "Epic"
            },
            "customfield_10011": 'Epic'
        }
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    if response.status_code != 201:
        print("Ошибка! Код -", response.status_code)

    # print(r[0]['statuses'][0]['name'])
    r = json.loads(response.text)
    print(' Задача(Epic) ID', r['id'], 'успешно создана! Код -', str(response.status_code) + '.', end='')
    # issues_id.append(r['id'])
    # Детали созданной задачи

    url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(r['id'])

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    if response.status_code != 200:
        print("Ошибка! Код -", response.status_code)

    print("  Задача ID " + str(r['id']) + " верифицирована! Код - ", response.status_code)
    assert response.status_code == 200


def test_create_and_get_task_issue_in_kanban_project_positive():
    url = "https://mytestsite1.atlassian.net/rest/api/2/issue"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project":
                {
                    "key": tkey
                },
            "summary": "REST EXAMPLE",
            "description": "New issue in KANBAN project via REST API ",
            "issuetype": {
                "name": "Task"
            }
        }
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    if response.status_code != 201:
        print("Ошибка! Код -", response.status_code)

    # print(r[0]['statuses'][0]['name'])
    r = json.loads(response.text)

    print('     Задача тип "Task" ID', r['id'], ' создана! Код -', str(response.status_code) + '.', end='')

    # Детали созданной задачи
    issue_id = r['id']

    url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(issue_id)

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    if response.status_code != 200:
        print("Ошибка! Код -", response.status_code)

    r = json.loads(response.text)

    assert response.status_code == 200
    assert r['fields']['summary'] == "REST EXAMPLE"
    assert r['fields']['description'] == 'New issue in KANBAN project via REST API '

    print("  Задача ID " + str(r['id']) + " проверена! Код - ", response.status_code, end='')


def test_create_and_get_history_issue_in_kanban_project_positive():
    url = "https://mytestsite1.atlassian.net/rest/api/2/issue"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project":
                {
                    "key": tkey
                },
            "summary": "REST EXAMPLE",
            "description": "New history issue in SCRAM project via REST API ",
            "issuetype": {
                "name": "История"
            }
        }
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    if response.status_code != 201:
        print("Ошибка! Код -", response.status_code)

    # print(r[0]['statuses'][0]['name'])
    r = json.loads(response.text)

    print('     Задача тип "История" ID', r['id'], ' создана! Код -', str(response.status_code) + '.', end='')
    issue_id = r['id']

    # Детали созданной задачи

    url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(issue_id)

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    if response.status_code != 200:
        print("Ошибка! Код -", response.status_code)

    r = json.loads(response.text)

    assert response.status_code == 200
    assert r['fields']['summary'] == "REST EXAMPLE"
    assert r['fields']['description'] == 'New history issue in SCRAM project via REST API '
    print("  Задача ID " + str(r['id']) + " проверена! Код - ", response.status_code, end='')


def test_create_and_get_bug_issue_in_kanban_project_positive():
    url = "https://mytestsite1.atlassian.net/rest/api/2/issue"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project":
                {
                    "key": tkey
                },
            "summary": "REST EXAMPLE",
            "description": "New bug issue in SCRAM project via REST API ",
            "issuetype": {
                "name": "Баг"
            }
        }
    })

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    if response.status_code != 201:
        print("Ошибка! Код -", response.status_code)

    # print(r[0]['statuses'][0]['name'])
    r = json.loads(response.text)
    print('     Задача тип "Баг" ID', r['id'], ' создана! Код -', str(response.status_code) + '.', end='')
    issue_id = r['id']

    # Детали созданной задачи

    url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + issue_id

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    if response.status_code != 200:
        print("Ошибка! Код -", response.status_code)

    r = json.loads(response.text)

    assert response.status_code == 200
    assert r['fields']['summary'] == "REST EXAMPLE"
    assert r['fields']['description'] == 'New bug issue in SCRAM project via REST API '
    print("  Задача ID " + str(r['id']) + " проверена! Код - ", response.status_code, end='')


def test_assign_issue_to_testuser():
    issues_id = [*get_list_all_issues_in_project(tkey), *get_list_all_epic_issues_in_project(tkey)]

    for i_key in issues_id:
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + i_key + "/assignee"

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "accountId": "60e2a4094ee1be00711f1136"
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        # r = json.loads(response.text)
        if response.status_code == 204:
            print('      Назначение успешно. Код - ', response.status_code, end='')
        else:
            print('Неудача! Код - ', response.status_code, end='')

        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + i_key
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )

        r = json.loads(response.text)
        assert str(r['fields']['assignee']['displayName']) == 'Testuser'
        assert response.status_code == 200
        print(' Проверено, код -', str(response.status_code) + '.', ' У задачи ID', str(r['id']), 'теперь '
                                                                                                  'исполнитель  -',
              r['fields']['assignee']['displayName'], end='. ')


def test_assign_issues_random_user_negative():
    import secrets
    secret_token = secrets.token_hex(nbytes=12)

    issues_id = [*get_list_all_issues_in_project(tkey), *get_list_all_epic_issues_in_project(tkey)]

    for i_key in issues_id:
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + i_key + "/assignee"

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "accountId": str(secret_token)
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        # r = json.loads(response.text)
        if response.status_code == 204:
            print('   Назначение успешно. Код - ', response.status_code, end='')
        else:
            print(' Назначение не удалось. Код - ', response.status_code, '.', sep='', end='')

        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + i_key
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )

        r = json.loads(response.text)

        assert response.status_code == 200
        if r['fields']['assignee']['displayName'] == admin_name or r['fields']['assignee']['displayName'] == 'Testuser':
            print(' У задачи ID', str(r['id']), ' исполнитель не изменился -', r['fields']['assignee']['displayName'],
                  end='. ')


def test_edit_name_issue():
    def edit_issue(id_issue):

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(id_issue) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "update": {
                "summary": [{
                    "set": "Редактированное название задачи"
                }]
            }
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        if response.status_code == 204:
            print('   Задача переименована', end='. ')

        assert response.status_code == 204

    print(3 * ' ', end='')
    issues_id = [*get_list_all_issues_in_project(tkey), *get_list_all_epic_issues_in_project(tkey)]
    for i in issues_id:
        edit_issue(i)


def test_set_empty_name_issue_negative():
    def edit_issue(id_issue):

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(id_issue) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "update": {
                "summary": [{
                    "set": None
                }]
            }
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        if response.status_code == 204:
            print('   Задача переименована', end='. ')
        else:
            print('   Задача не переименована, код -', response.status_code, end='. ')

        assert response.status_code != 204

    print(2 * ' ', end='')
    issues_id = [*get_list_all_issues_in_project(tkey), *get_list_all_epic_issues_in_project(tkey)]
    for i in issues_id:
        edit_issue(i)


def test_set_space_name_issue_negative():
    def edit_issue(id_issue):

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(id_issue) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "update": {
                "summary": [{
                    "set": '   '
                }]
            }
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        if response.status_code == 204:
            print('   Задача переименована', end='. ')
        else:
            print('   Задача не переименована, код -', response.status_code, end='. ')

        assert response.status_code != 204

    print(2 * ' ', end='')
    issues_id = [*get_list_all_issues_in_project(tkey), *get_list_all_epic_issues_in_project(tkey)]
    for i in issues_id:
        edit_issue(i)


def test_set_3day_timeSpent_epic_issue():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(id_issue) + '/worklog/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "timeSpentSeconds": 86400,

            "comment": "I did some work here.",
            "started": "2021-09-23T02:13:20.853+0000"
        })

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        assert response.status_code == 201

        r = json.loads(response.text)
        assert r['timeSpent'] == '3d'
        print(' Для эпика ', id_issue, ' установлен интервал - ', r['timeSpent'], '. ', sep='', end='')

    issues_id = get_list_all_epic_issues_in_project(tkey)

    for i in issues_id:
        edit_issue(i)


def test_set_big_incorrect_timeSpent_epic_issue_negative():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(id_issue) + '/worklog/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "timeSpentSeconds": 5999999999999999999,

            "comment": "I did some work here.",
            "started": "2021-09-23T02:13:20.853+0000"
        })

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )

        r = json.loads(response.text)

        assert 'errors' in r
        if 'errors' not in r:
            print(' Удачно установлен некорректный интервал')
        else:
            print(' Для задачи ', id_issue, ' установки срока не изменились.', end='')

    issues_id = get_list_all_epic_issues_in_project(tkey)

    for i in issues_id:
        edit_issue(i)


def test_set_1day_timeSpent_for_issues():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(id_issue) + '/worklog/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "timeSpentSeconds": 28800,

            "comment": "I did some work here.",
            "started": "2021-09-23T02:13:20.853+0000"
        })

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        assert response.status_code == 201

        r = json.loads(response.text)
        assert r['timeSpent'] == '1d'
        print(' Для задачи ', id_issue, ' установлен срок - ', r['timeSpent'], '. Код  ', response.status_code, sep='',
              end='. ')

    issues_id = get_list_all_issues_in_project(tkey)

    for i in issues_id:
        edit_issue(i)


def test_set_incorrect_timeSpent_for_issues_negative():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + str(id_issue) + '/worklog/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "timeSpentSeconds": 5999999999999999999,

            "comment": "I did some work here.",
            "started": "2021-09-23T02:13:20.853+0000"
        })

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )

        r = json.loads(response.text)
        assert 'errors' in r
        if 'errors' not in r:
            print(' Удачно установлен некорректный интервал')
        else:
            print(' Для задачи ', id_issue, ' установки срока не изменились.', end='')

    issues_id = get_list_all_issues_in_project(tkey)

    for i in issues_id:
        edit_issue(i)


def test_create_subtasks_for_all_tasks():
    url = "https://mytestsite1.atlassian.net/rest/api/2/issue"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    issues_id = get_list_all_issues_in_project(tkey)
    for issue_id in issues_id:
        payload = json.dumps({'fields': {
            'project': {'key': tkey},
            'summary': 'New subtask name',
            'description': 'Какая то новая подзадача',
            'issuetype': {'name': 'Подзадача'},
            'parent': {'id': issue_id},
            'assignee': {'name': 'Testuser'}
        }})

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )

        if response.status_code != 201:
            print("Ошибка! Код -", response.status_code, response.text)
        else:
            print(' Подзадача к задаче id ', issue_id, 'создана.', end='')
        assert response.status_code == 201


def test_get_list_all_subtasks():
    url = "https://mytestsite1.atlassian.net/rest/api/3/search"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    q2 = ' AND \"issuetype\" = \"Sub-task\"'  # 'Task' or 'Sub-task'
    query = {
        'jql': ('project = ' + str(tkey) + ' ' + str(q2))
    }
    # print(query)
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    assert response.status_code == 200
    global subtasks_id
    subtasks_id = []
    r = json.loads(response.text)
    # print(r)
    print(' Найдено', len(r['issues']), 'подзадачи:', end=' ')
    for i in range(len(r['issues'])):
        subtasks_id.append(r['issues'][i]['id'])
    print("их ID ", subtasks_id, end='')
    return subtasks_id


def test_change_issues_and_subtask_status():
    all_transitions = ['21', '31', '21', '11', '31', '11', '41', '31', '41', '21', '41']
    print(3 * ' ', end='')
    issues_id = get_list_all_epic_issues_in_project(tkey)
    print("Найдено ", len(issues_id), "задач", end='. ')
    for iss_id in issues_id:

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(iss_id) + "/transitions"

        auth = HTTPBasicAuth(mylogin, mypass)

        for tr in all_transitions:

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = json.dumps({
                "transition": {
                    "id": tr
                }
            })

            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth
            )

            if response.status_code != 204:
                print("Ошибка! Код -", response.status_code, response.text)

            # GET
            headers = {
                "Accept": "application/json"
            }

            response = requests.request(
                "GET",
                url,
                headers=headers,
                auth=auth
            )

            # r = json.loads(response.text)

        assert response.status_code == 200

        if response.status_code == 200:
            print(' Задача ', iss_id, ' прошла через все этапы проекта.', end=' ')


def test_move_issues_to_epic():
    def get_list_key_all_epic_issues_in_project(tkey):

        url = "https://mytestsite1.atlassian.net/rest/api/3/search"

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json"
        }

        query = {
            'jql': 'project = ' + str(tkey)
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query,
            auth=auth
        )
        issues_keys = []
        issues_id = []
        r = json.loads(response.text)
        assert response.status_code == 200
        # print('      Найдено', len(r['issues']), 'задач:', end=' ')
        for i in range(len(r['issues'])):

            if r['issues'][i]['fields']['issuetype']['name'] in ['Эпик', 'Epic']:
                issues_id.append(r['issues'][i]['id'])
                issues_keys = []
                issues_keys.append(r['issues'][i]['key'])

        return issues_keys

    def get_list_issues_in_project(tkey):
        url = "https://mytestsite1.atlassian.net/rest/api/3/search"

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        query = {
            'jql': 'project = ' + str(tkey)
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query,
            auth=auth
        )

        issues_id = []
        r = json.loads(response.text)
        assert response.status_code == 200

        for i in range(len(r['issues'])):

            if r['issues'][i]['fields']['issuetype']['name'] not in ['Эпик', 'Epic', 'Подзадача', 'Sub-task']:
                issues_id.append(r['issues'][i]['id'])
        return issues_id

    issues_id = get_list_issues_in_project(tkey)

    for issue_id in issues_id:
        epic_key = get_list_key_all_epic_issues_in_project(tkey)

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                # "parent": {"id": str(epic_id[0])},
                "customfield_10014": str(epic_key[0])
                # "customfield_10014": None
            }
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        assert response.status_code == 204
        if response.status_code == 204:
            print(" Код ", str(response.status_code) + '. ', 'Задача ', issue_id, 'теперь в эпике ', str(epic_key[0]),
                  end='. ')


def test_return_issues_from_epic():
    def get_list_key_all_epic_issues_in_project(tkey):

        url = "https://mytestsite1.atlassian.net/rest/api/3/search"

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json"
        }

        query = {
            'jql': 'project = ' + str(tkey)
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query,
            auth=auth
        )
        issues_keys = []
        issues_id = []
        r = json.loads(response.text)
        assert response.status_code == 200
        # print('      Найдено', len(r['issues']), 'задач:', end=' ')
        for i in range(len(r['issues'])):

            if r['issues'][i]['fields']['issuetype']['name'] in ['Эпик', 'Epic']:
                issues_id.append(r['issues'][i]['id'])
                issues_keys = []
                issues_keys.append(r['issues'][i]['key'])

        return issues_keys

    def get_list_issues_in_project(tkey):
        url = "https://mytestsite1.atlassian.net/rest/api/3/search"

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        query = {
            'jql': 'project = ' + str(tkey)
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query,
            auth=auth
        )

        issues_id = []
        r = json.loads(response.text)
        assert response.status_code == 200

        for i in range(len(r['issues'])):

            if r['issues'][i]['fields']['issuetype']['name'] not in ['Эпик', 'Epic', 'Подзадача', 'Sub-task']:
                issues_id.append(r['issues'][i]['id'])
        return issues_id

    issues_id = get_list_issues_in_project(tkey)

    for issue_id in issues_id:
        epic_key = get_list_key_all_epic_issues_in_project(tkey)

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                # "parent": {"id": str(epic_id[0])},
                "customfield_10014": None
            }
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        assert response.status_code == 204
        if response.status_code == 204:
            print(" Код ", str(response.status_code) + '. ', 'Задача ', issue_id, 'выведена из эпика ',
                  str(epic_key[0]), end='. ')


def test_change_epic_status():
    all_transitions = ['21', '31', '21', '11', '31', '11', '41', '31', '41', '21', '41']
    print(3 * ' ', end='')
    issues_id = get_list_all_epic_issues_in_project(tkey)
    print("Найдено ", len(issues_id), "эпиков", end='. ')
    for iss_id in issues_id:

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(iss_id) + "/transitions"

        auth = HTTPBasicAuth(mylogin, mypass)

        for tr in all_transitions:

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = json.dumps({
                "transition": {
                    "id": tr
                }
            })

            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth
            )

            if response.status_code != 204:
                print("Ошибка! Код -", response.status_code, response.text)

            # GET
            headers = {
                "Accept": "application/json"
            }

            response = requests.request(
                "GET",
                url,
                headers=headers,
                auth=auth
            )

            # r = json.loads(response.text)

        assert response.status_code == 200

        if response.status_code == 200:
            print(' Эпик задача ', iss_id, ' прошла через все этапы проекта.', end=' ')


def test_add_comment_in_all_issues_and_subtasks():
    issues_id = get_list_all_issues_in_project(tkey)

    for issue_id in issues_id:

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id) + '/comment'

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({

            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": "Новый добавленный тестовый комментарий - Сьешь немного этих прекрасных бельгийских вафель!",
                                "type": "text"
                            }
                        ]
                    }
                ]
            }
        })

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        assert response.status_code == 201
        print(' Коммент к задаче ', issue_id, 'добавлен! Код -', response.status_code, '. ', end='')
        if response.status_code != 201:
            print("Ошибка! Код -", response.status_code, response.text)


def test_add_empty_comment_in_all_issues_and_subtasks_negative():
    issues_id = get_list_all_issues_in_project(tkey)

    for issue_id in issues_id:

        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id) + '/comment'

        auth = HTTPBasicAuth(mylogin, mypass)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({

            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": None,
                                "type": "text"
                            }
                        ]
                    }
                ]
            }
        })

        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )
        assert response.status_code == 400
        print(' Пустой коммент к задаче ', issue_id, ' не добавлен! Код - ', response.status_code, sep='', end='. ')


def test_clear_comment_in_all_issues_and_subtasks():
    issues_id = get_list_all_issues_in_project(tkey)

    def get_all_comments_id():
        comments_id = []
        for i in range(len(issues_id)):
            url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issues_id[i]) + '/comment'
            auth = HTTPBasicAuth(mylogin, mypass)
            headers = {
                "Accept": "application/json"
            }

            response = requests.request(
                "GET",
                url,
                headers=headers,
                auth=auth
            )

            r = json.loads(response.text)

            comments_id.append(r['comments'][0]['id'])
        return comments_id

    comments_id = get_all_comments_id()

    for i in range(len(issues_id)):
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issues_id[i]) + '/comment/' + str(
            comments_id[i])
        auth = HTTPBasicAuth(mylogin, mypass)

        response = requests.request(
            "DELETE",
            url,
            auth=auth
        )

        assert response.status_code == 204
        if response.status_code == 204:
            print(' В задаче ', issues_id[i], 'Удален коммент ', comments_id[i], end='. ')
        print('Код ', response.status_code, end='. ')


def test_delete_all_epics_issues_subtasks_clear_project():
    issues_id = [*get_list_all_issues_in_project(tkey), *get_list_all_epic_issues_in_project(tkey)]
    for issue_id in issues_id:
        url = "https://mytestsite1.atlassian.net//rest/api/3/issue/" + str(issue_id) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)

        response = requests.request(
            "DELETE",
            url,
            auth=auth
        )
        assert response.status_code == 204
        if response.status_code == 204:
            print(' Задача ', str(issue_id), 'удалена. Код ', response.status_code, end='')


# delete project - finish test suite


def test_delete_test_project():
    url = "https://mytestsite1.atlassian.net/rest/api/2/project/" + str(tkey)

    auth = HTTPBasicAuth(mylogin, mypass)

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
        print(" Проект", tkey, "успешно удален. Код", response.status_code, end='.')
        # print(response.status_code)
    assert response.status_code == 204
