from .models import BlackList, db
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from .models import db, BlackList


def adicionar_email(request):
   
   email = request.json.get('email')
   blocked_reason = request.json.get('blocked_reason')
   app_uuid = request.json.get('app_uuid')

   if email is None:
      return "El campo email no se encuentra definido", 412
   if app_uuid is None:
      return "El campo app_uuid no se encuentra definido", 412


   ip = request.remote_addr


   existe_email = BlackList.query.filter(BlackList.email == email).first()
   if existe_email:
      return f"El email, {email} ya existe", 412
   
   nuevo_registro = BlackList(email=email, blocked_reason=blocked_reason, 
                              app_uuid=app_uuid, ip=ip)
   db.session.add(nuevo_registro)
   db.session.commit()

   return f'{nuevo_registro.email}', 201

def search_email(email):
   current_user = get_jwt_identity()
   if current_user != 'root':
      return jsonify({"msg": "Token invalido"}), 401

   get_query=BlackList.query.filter(BlackList.email==email).first()
   if get_query is None:
    return jsonify({'exist': False}), 200
   
   response = {'exist': True, 'blocked_reason': get_query.blocked_reason}
   return jsonify(response), 200

def generate_token():
   access_token = create_access_token('root')
   return jsonify(access_token=access_token), 200
   
