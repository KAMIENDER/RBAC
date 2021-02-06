### 准备工作
* 需要的依赖，可以见infrastructure/config/dependency.txt
* 数据库建立，本地mysql的root用户，密码设置为123456，建立名字为rbac的数据库

`
update dtabase struct：python manage.py db upgrade
`

`
deploy gunicorn command: gunicorn --config=gunicorn_config.py wsgi:app
`

