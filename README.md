# ISAAC-Django-Vue3-Framework

💡 **「About」**

ISAAC-Django-Vue3-Framework is a comprehensive basic development platform based on the RBAC (Role-Based Access Control) model for permission control, with column-level granularity. It follows a frontend-backend separation architecture, with Django and Django Rest Framework used for the backend, and Vue3, Composition API, TypeScript, Vite, and Element Plus used for the frontend.

## framework introduction

* 🧑‍🤝‍🧑Front-end adoption Vue3+TS+pinia+fastcrud。
* 👭The backend uses the Python language Django framework as well as the powerful[Django REST Framework](https://pypi.org/project/djangorestframework)。
* 👫Permission authentication use[Django REST Framework SimpleJWT](https://pypi.org/project/djangorestframework-simplejwt)，Supports the multi-terminal authentication system.
* 👬Support loading dynamic permission menu, multi - way easy permission control.
* 👬Enhanced Column Permission Control, with granularity down to each column.

## Online experience

👩‍👧‍👦👩‍👧‍👦 demo address:TBD

* demo account：superadmin

* demo password：admin123456

👩‍👦‍👦docs:TBD

## source code url:

## core function

1. 👨‍⚕️Menu Management: Configure system menus, operation permissions, button permission flags, backend interface permissions, etc.
2. 🧑‍⚕️Department Management: Configure system organizational structure (company, department, role).
3. 👩‍⚕️Role Management: Role menu permission assignment, data permission assignment, set role-based data scope permissions by department.
4. 🧑‍🎓Button Permission Control: Authorize role-specific button permissions and interface permissions, enabling authorization of data scope for each interface.
5. 🧑‍🎓Field Column Permission Control: Authorize page field display permissions, specifically for the display permissions of a certain column.
6. 👨‍🎓User Management: Users are system operators, and this function is mainly used for system user configuration.
7. 👬API Whitelist: Configure interfaces that do not require permission verification.
8. 🧑‍🔧Dictionary Management: Maintain frequently used and relatively fixed data in the system.
9. 🧑‍🔧Region Management: Manage provinces, cities, counties, and districts.
10. 📁File Management: Unified management of all files, images, etc., on the platform.
11. 🗓️Operation Logs: Record and query logs for normal system operations and exceptional system information.


## Repository Branch Explanation 💈
Main Branch: master (stable version)
Development Branch: develop

## before start project you need:

~~~

1) Python >= 3.11.0 (Minimum version 3.9+)
# 1 craete file：pip.ini 

[global]
index-url=https://artifactory-esc.corp.knorr-bremse.com:8482/artifactory/api/pypi/py-python.org/simple/
[install]
trusted-host=artifactory-esc.corp.knorr-bremse.com

# 2 put pip.ini into %APPDATA%pip

2) Node.js >= 16.0

# 1 create file: .npmrc

strict-ssl=false
# registry=https://registry.npmmirror.com
registry=https://artifactory-esc.corp.knorr-bremse.com:8482/artifactory/api/npm/npm-public/

# 2 put .npmrc into C:\Users\{yourusername}

3) Mysql >= 8.0 (Optional, default database: SQLite3, supports 5.7+, recommended version: 8.0)
# you need to create your own database in mysql and type in username/password/database name into your env file

4) Redis (Optional, latest version)

~~~



## frontend♝

```bash
# enter code dir
cd web

# install dependence
pnpm install
# Start service
pnpm run dev
# Visit http://localhost:8080 in your browser
# Parameters such as boot port can be configured in the #.env.development file
# Build the production environment
# yarn run build
```
## backend💈

~~~bash
1. enter code dir cd backend
2. copy ./conf/env.example.py to ./conf dir，rename as env.py
3. in env.py configure database information
 mysql database recommended version: 8.0
 mysql database character set: utf8mb4
4. install pip dependence  # please create virtual environemnt by using "virtualenv my_project_env"  then use "my_project_env\Scripts\activate" to activate the environment
 pip install -r requirements.txt
5. Execute the migration command:
 python manage.py makemigrations
 python manage.py migrate
6. Initialization data
 python manage.py init
7. Initialize provincial, municipal and county data:
 python manage.py init_area
8. start backend
 python manage.py runserver 0.0.0.0:8000
or daphne :
 daphne -b 0.0.0.0 -p 8000 application.asgi:application
~~~

### visit backend swagger

* visit url：[http://localhost:8080](http://localhost:8080) (The default address is this one. If you want to change it, follow the configuration file)
* account：`superadmin` password：`admin123456`

### docker-compose


~~~shell
docker-compose up -d
# Initialize backend data (first execution only)
docker exec -ti dvadmin3-django bash
python manage.py makemigrations 
python manage.py migrate
python manage.py init_area
python manage.py init
exit

frontend url：http://127.0.0.1:8080
backend url：http://127.0.0.1:8080/api
# Change 127.0.0.1 to your own public ip address on the server
account：`superadmin` password：`admin123456`

# docker-compose stop
docker-compose down
#  docker-compose restart
docker-compose restart
#  docker-compose on start build
docker-compose up -d --build
~~~

