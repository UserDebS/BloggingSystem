def dictToList(data : dict[str, str | dict[str, bool]]) -> dict[str, str | list[str]]:
    data['tags'] = list(data['tags'].keys())
    return data

if __name__ == '__main__':
    data = {'title': 'hello', 'username': 'admin', 'tags': {'programming': True, 'web_development': True}, 'self_url': 'http://localhost:8080/?blogid=19'}
    print(dictToList(data=data))