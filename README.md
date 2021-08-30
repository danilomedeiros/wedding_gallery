# Wedding Gallery

Collaborative weddding photo album. Invited friends can upload photos for Husband and wife approve.

flask, vue.js, mongoddb, veutify

## Get Started

Clone the project
```
git clone https://github.com/danilomedeiros/wedding_gallery.git
cd wedding_gallery
```

Create a python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt 
```
Environment Variables:

edit the .env file based with the rigth parameter values
```
jwt_secret_key=123
database_url=mongodb+srv://<user>:<password>@url
s3_bucket=FFFFFF
aws_access_key_id=XXXXX
aws_secret_access_key=YYYYY
```

build the frontend application 
```
cd frontend && npm run build 
```
Run the app
```
gunicorn app:app
```
