<b>Abstract URL</b>


![Screenshot from 2023-12-29 23-17-16.png](Screenshot%20from%202023-12-29%2023-17-16.png)

<b>Pseudo MainServise</b>

![Screenshot from 2023-12-29 23-23-27.png](Screenshot%20from%202023-12-29%2023-23-27.png)
![Screenshot from 2023-12-29 23-23-40.png](Screenshot%20from%202023-12-29%2023-23-40.png)

```commandline
python manage.py runserver
```

```commandline
python -m celery -A core worker -l INFO
```

```commandline
python -m celery -A core beat -l INFO
```

```commandline
locust
```