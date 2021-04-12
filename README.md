# sunboard

Foster collective intelligence, avoid groupthink.

A tool for collaborative brainstorming.

# Install

```
python3 -m venv sunboard-env
cd sunboard-env
. bin/activate
pip install -U pip
pip install -e git+ssh://git@github.com/guettli/sunboard.git#egg=sunboard
```

Create `.env`

```
cp .env.example .env
```


We use PostgreSQL. First create a database superuser with the same name as your login name (of your PC)

Check [Django Database Setup](https://docs.djangoproject.com/en/3.2/intro/tutorial02/#database-setup)
```
createdb sunboard
```
If you use PyCharm than open "sunboard-env-src/sunboard" and set the Python Interpreter to "sunboard-env/bin/python".

Run database migrations
```
manage.py migrate
```

Start local web-server
```
manage.py runserver
```
