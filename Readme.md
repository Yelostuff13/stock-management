# Django + Postgres + Docker compose

รันคำสั่งนี้ก่อน

```bash
docker-compose up -d --build
```

ต่อด้วย

```bash
docker-compose exec web python manage.py migrate   
```

สร้าง User 

```bash
docker-compose exec web python manage.py createsuperuser
```