About
_____

This project allows you to control external objects (a tree). In the basic package, there are two types of objects: the server and site. Of these, one can construct a reflection of its infrastructure sites and servers. On these objects you can execute commands. Now is the management of the demons.


Installation
------------

**Download**

    git clone git@github.com:NElias/Meotec.git
    cd Meotec

**Install requirements**

    pip install -r requirements.txt

**Configure DB in settings/local.py, example:**

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'meotec',
            'USER': 'root',
        }
    }

Sqlite3 does not work

**Migrate and run**

    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver


Usage
-----

Now you can add the first manager.
At the root of the project is the Base Manager, use it.
Go into Settings and specify the absolute path to it.
On the left you can build a tree of objects.
After that, go to Dashboard and manage objects.
