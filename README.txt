If you run with gunicorn please use below command, otherwise my login flow is not working properly
gunicorn server:app --workers=1