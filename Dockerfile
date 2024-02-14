FROM python:3.10-slim
WORKDIR tasks/

COPY . .

RUN pip install -r ./requirements.txt --no-cache-dir
#RUN python3 tmanager/manage.py migrate
#RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.kz', 'pass1')" | python3 manage.py shell
#RUN python3 tmanager/manage.py makemigrations
#RUN python3 tmanager/manage.py migrate
EXPOSE 8000

ENTRYPOINT ["sh", "tmanager/run.sh"]