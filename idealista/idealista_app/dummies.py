user = {
    'name': 'Usuario',
    'email': 'usuario@mail.com',
    'password': '1234abcd'
}

users = [user]


def add_user(name, email, password):
    users.append({
        'name': name,
        'email': email,
        'password': password,
    })


def user_exists(email):
    return any(x['email'] == email for x in users)
