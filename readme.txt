1. Клонировать репозиторий с проектом, зайти в корневую папку. 
2. Прописать команду docker run --name python --network host -v ${PWD}:/drf -it python bash
3. Перейти  директорию drf 
4. Установить django: pip install django , устновить зависимости pip install -r requirement.txt
5. В другом окне консоли запустить контейнер с postgres 
	docker run --name postgres5 -p 5434:5432 -e POSTGRES_PASSWORD=passvord \
	-e POSTGRES_DB=public -e POSTGRES_HOST_AUTH_METHOD=md5 \
	-v/home/yanochkina_sl/db_1:/var/lib/postgresql/data postgres
6. В консоли проекта внести измения в файле settings.py (название базы, пароль, host)
7. Выполнить миграции python3 manage.py migrate
8. Запустить сервер python3 manage.py runserver

P.s. только так у меня получилось... и на это ушло три дня(
