import uuid

def portal_jwt_token_update(user_obj,token):
    try:
        token['nonce']=uuid.uuid4().hex
        return token
    except Exception as err:
        raise Exception("Error in Token Gen",err)