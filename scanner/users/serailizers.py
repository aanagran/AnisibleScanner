from rest_framework import serializers
from django.conf import settings


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    # def email_validator(self,value):
        # EMAIL_REGEX=settings.EMAIL_REGEX
        # if not re.search(EMAIL_REGEX, str(value).lower()):
        #     return False
        # return True

    # def validate(self,validated_data):
    #     user = validated_data.get('user',None)
    #     requested_time = validated_data.get('requested_time',None)
    #     if not user or not requested_time:
    #         logging.error('Credentials not provided')
    #         raise serializers.ValidationError("Credentials not provided")
    #     decrypt_secret=aes.getKeyFromEpoch(requested_time)
    #     dec_value,status=aes.decrypt(user,decrypt_secret,requested_time)
        
    #     if status:
    #         logging.info('successfully decrypted credentials')
    #         value=json.loads(dec_value)
    #         return value
    #     else:
    #         logging.error('Failed to decrypt the credentials')
    #         raise serializers.ValidationError('Unable to fetch the credentials!')
