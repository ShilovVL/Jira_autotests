import requests
from requests.auth import HTTPBasicAuth
import json
import pytest

# my constants
admin_name = 'Василий Шилов'  # project owner
mylogin = "shilovv@sibnet.ru"  # your email as jira login
mypass = "*******"  # your jira api token
tkey = 'TB01'  # key for tmp project
tname = "TMP test business project for test issues"  # tmp name testproject


def get_list_issues_in_project(tkey):
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
    for i in range(len(r['issues'])):
        if r['issues'][i]['fields']['issuetype']['name'] != 'Эпик' and r['issues'][i]['fields']['issuetype'][
            'name'] != 'Epic':
            issues_id.append(r['issues'][i]['id'])
    return issues_id


def get_list_all_subtasks():
    url = "https://mytestsite1.atlassian.net/rest/api/3/search"

    auth = HTTPBasicAuth(mylogin, mypass)
    headers = {
        "Accept": "application/json"
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

    subtasks_id = []
    r = json.loads(response.text)

    for i in range(len(r['issues'])):
        subtasks_id.append(r['issues'][i]['id'])
    return subtasks_id


def test_create_business_project():
    url = "https://mytestsite1.atlassian.net/rest/api/2/project"

    auth = HTTPBasicAuth(mylogin, mypass)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "notificationScheme": 10000,
        "description": "Temporaly_Test_issues_in_business_project",
        "leadAccountId": "5f774fa64d09f70076f97f65",
        "url": "http://mytestsite1.atlassian.net",
        "avatarId": 10407,
        "issueSecurityScheme": 10000,
        "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",
        "name": tname,

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
    # error = 0
    if 'key' in r:
        if r['key'] == tkey:
            print('   Проект ', '"' + json.loads(payload)['name'] + '"', ' ID', r['id'], ' создан', end='')
    assert json.loads(payload)['name'] == tname
    assert 'errors' not in r
    assert r['key'] == tkey


def test_create_and_get_task_issue_in_business_project_positive():
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
            "description": "New issue in business project via REST API ",
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

    r = json.loads(response.text)
    print('     Задача тип "Task" ID', r['id'], ' создана! Код -', str(response.status_code) + '.', end='')
    global issue_id
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
    assert r['fields']['description'] == 'New issue in business project via REST API '
    print("  Задача ID " + str(r['id']) + " проверена! Код - ", response.status_code, end='')


def test_create_and_get_3aga4a_issue_in_business_project_positive():
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
            "description": "New issue in business project via REST API ",
            "issuetype": {
                "name": "Задача"
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

    r = json.loads(response.text)
    print('      Задача тип "Задача" ID', r['id'], ' создана! Код -', str(response.status_code) + '.', end='')
    issue_id = r['id']

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
    assert r['fields']['description'] == 'New issue in business project via REST API '
    print("  Задача ID " + str(r['id']) + " проверена! Код - ", response.status_code, end='')


def test_get_list_all_issues_in_project():
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
    global issues_id
    issues_id = []
    r = json.loads(response.text)
    assert response.status_code == 200
    print('      Найдено', len(r['issues']), 'задач:', end=' ')
    for i in range(len(r['issues'])):
        # if str(r['issues'][i]['fields']['summary']) == 'REST EXAMPLE':
        #     print(i, r['issues'][i]['fields']['summary'])
        issues_id.append(r['issues'][i]['id'])
    print("их ID ", issues_id, end=' ')


def test_create_subtasks_for_all_tasks():
    url = "https://mytestsite1.atlassian.net/rest/api/2/issue"

    auth = HTTPBasicAuth(mylogin, mypass)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    issues_id = get_list_issues_in_project(tkey)
    for issue_id in issues_id:
        payload = json.dumps({'fields': {
            'project': {'key': tkey},
            'summary': 'New subtask name',
            'description': 'Какая то новая подзадача',
            'issuetype': {'name': 'Sub-task'},
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
        "Accept": "application/json"
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
    global subtasks_id
    subtasks_id = []
    r = json.loads(response.text)

    print(' Найдено', len(r['issues']), 'подзадачи:', end=' ')
    for i in range(len(r['issues'])):
        subtasks_id.append(r['issues'][i]['id'])
    print("их ID ", subtasks_id, end='')


def test_change_subtasks_status():
    all_transitions = ['11', '111', '121', '11', '21', '131', '141', '21', '31', '41']
    print(3 * ' ', end='')
    subtasks_id = get_list_all_subtasks()
    for iss_id in subtasks_id:

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

        assert not r['transitions']
        assert response.status_code == 200
        if not r['transitions'] and response.status_code == 200:
            print(' Подзадача ', iss_id, ' прошла все возможные этапы и завершена.', end=' ')


def test_set_incorrect_subtasks_status_negative():
    all_transitions = ['11', '41', '11']
    print(3 * ' ', end='')
    subtasks_id = get_list_all_subtasks()
    for iss_id in subtasks_id:

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

            assert response.status_code != 204
            rcode = response.status_code

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

        print('Код -', rcode, end='.')

        if response.status_code == 200:
            print(' Статус подзадачи ', iss_id, ' не изменился.', end=' ')


def test_assign_issue_to_testuser():
    issues_id = get_list_issues_in_project(tkey)
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


def test_assign_issue_to_random_user_negative():
    issues_id = get_list_issues_in_project(tkey)
    import secrets
    secret_token = secrets.token_hex(nbytes=12)
    for i_key in issues_id:
        url = "https://mytestsite1.atlassian.net/rest/api/2/issue/" + i_key + "/assignee"

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "accountId": secret_token
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
        # else:
        #     print('Неудача! Код - ', response.status_code, end='')

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
        assert str(r['fields']['assignee']['displayName']) == 'Testuser' or r['fields']['assignee'][
            'displayName'] == admin_name
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
                    "set": "Редактированное поле Summary"
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
            print(' Задача', id_issue, 'переименована', end='. ')

        assert response.status_code == 204

    print(3 * ' ', end='')
    issues_id = get_list_issues_in_project(tkey)
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
            print(' Задача', id_issue, 'переименована', end='. ')
        else:
            print(' Задача', id_issue, ' не переименована', end='. ')

        assert response.status_code != 204

    print(3 * ' ', end='')
    issues_id = get_list_issues_in_project(tkey)
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
            print(' Задача', id_issue, 'переименована', end='. ')
        else:
            print(' Задача', id_issue, ' не переименована', end='. ')

        assert response.status_code != 204

    print(3 * ' ', end='')
    issues_id = get_list_issues_in_project(tkey)
    for i in issues_id:
        edit_issue(i)


def test_edit_due_date_issue():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(id_issue) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                "duedate": '2021-12-31'
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

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )
        r = json.loads(response.text)
        print('  Установлек срок задачи - ', r['fields']['duedate'], '. ', sep='', end='')
        assert r['fields']['duedate'] == '2021-12-31'

    issues_id = get_list_issues_in_project(tkey)
    for i in issues_id:
        edit_issue(i)


def test_edit_due_date_issue_set_incorrect_date_negative():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(id_issue) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                "duedate": '2021-15-32'
            }
        })

        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )

        assert response.status_code != 204

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )
        r = json.loads(response.text)
        print('  Cрок задачи ', id_issue, ' не изменился - ', r['fields']['duedate'], '. ', sep='', end='')
        assert r['fields']['duedate'] == '2021-12-31'

    issues_id = get_list_issues_in_project(tkey)
    for i in issues_id:
        edit_issue(i)


def test_clear_due_date_issue():
    def edit_issue(id_issue):
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(id_issue) + '/'

        auth = HTTPBasicAuth(mylogin, mypass)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = json.dumps({
            "fields": {
                "duedate": None
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

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )
        r = json.loads(response.text)
        print('  Cрок задачи ', id_issue, ' очищен, теперь значение - ', r['fields']['duedate'], '. ', sep='', end='')
        assert r['fields']['duedate'] == None

    issues_id = get_list_issues_in_project(tkey)
    for i in issues_id:
        edit_issue(i)


def test_add_comment_in_all_issues_and_subtasks():
    alltasks_id = get_list_issues_in_project(tkey)

    for issue_id in alltasks_id:

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
        print(' Коммент к задаче ', issue_id, 'добавлен! Код -', response.status_code, end='')
        if response.status_code != 201:
            print("Ошибка! Код -", response.status_code, response.text)


def test_check_all_comment():
    alltasks_id = get_list_issues_in_project(tkey)
    for issue_id in alltasks_id:
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id) + '/comment'

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
        rez = json.loads(response.text)  # 'dict'

        y = 0
        for i in rez['comments']:
            txt_comnt1 = rez['comments'][y]['body']['content'][0]['content'][0]['text']
            assert txt_comnt1 == "Новый добавленный тестовый комментарий - Сьешь немного этих прекрасных бельгийских вафель!"
            y += 1
            if txt_comnt1 == "Новый добавленный тестовый комментарий - Сьешь немного этих прекрасных бельгийских вафель!":
                print(' Нов. коммент Ок. Код -', response.status_code, end='. ')


def test_change_issue_status_move_by_columns():
    all_transitions = ['11', '111', '121', '11', '21', '131', '141', '21', '31', '41']
    print(3 * ' ', end='')
    all_issues = get_list_issues_in_project(tkey)
    all_subtasks = get_list_all_subtasks()
    issues_id = []
    for i in all_issues:
        if i not in all_subtasks:
            issues_id.append(i)

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

            # print('Код -', response.status_code)

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

            r = json.loads(response.text)

        assert not r['transitions']
        assert response.status_code == 200

        if not r['transitions'] and response.status_code == 200:
            print(' Задача ', iss_id, ' прошла через все этапы проекта и завершена.', end=' ')


def test_incorrect_change_issue_status_negative():
    all_transitions = ['11', '41', '11']  # impossible transitions for issues in business project
    print(3 * ' ', end='')
    all_issues = get_list_issues_in_project(tkey)
    all_subtasks = get_list_all_subtasks()
    issues_id = []
    for i in all_issues:
        if i not in all_subtasks:
            issues_id.append(i)

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
                rcode = response.status_code

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

            r = json.loads(response.text)

        print("Код -", rcode, end='.')

        if r['transitions'] == [] and response.status_code == 200:
            print(' Статус задачи ', iss_id, ' не изменился.',  end=' ')


def test_delete_all_subtask():
    subtasks_id = get_list_all_subtasks()
    for issue_id in subtasks_id:
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id)

        auth = HTTPBasicAuth(mylogin, mypass)

        response = requests.request(
            "DELETE",
            url,
            auth=auth
        )
        assert response.status_code == 204, f"Неверный код ответа, получен {response.status_code}"
        if response.status_code == 204:
            print(f" Подзадача id {issue_id} удалена. Код -", response.status_code, end='.')


def test_delete_all_issues():
    issues_id = get_list_issues_in_project(tkey)
    for issue_id in issues_id:
        url = "https://mytestsite1.atlassian.net/rest/api/3/issue/" + str(issue_id)

        auth = HTTPBasicAuth(mylogin, mypass)

        response = requests.request(
            "DELETE",
            url,
            auth=auth
        )
        assert response.status_code == 204, f"Неверный код ответа, получен {response.status_code}"
        if response.status_code == 204:
            print(f" Задача id {issue_id} удалена. Код -", response.status_code, end='.')


# *****************************************************
#  Удаляем тестируемый проект - заканчиваем тест свиту
def test_delete_test_business_project():
    url = "https://mytestsite1.atlassian.net/rest/api/2/project/" + str(tkey)

    auth = HTTPBasicAuth(mylogin, mypass)

    response = requests.request(
        "DELETE",
        url,
        auth=auth
    )

    if response.status_code != 204:
        r = json.loads(response.text)
        print(r['errorMessages'][0])
    else:
        print(" Проект успешно удален", end='')
    # print(response.status_code)
    assert response.status_code == 204
