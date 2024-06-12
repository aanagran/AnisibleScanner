from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics,status
from cis.serializers import HostConfigSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from cis.models import HostConfig
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import paramiko,re
from cis.tasks import anisblerunner


class HostConfigAPIView(generics.ListCreateAPIView):
    serializer_class = HostConfigSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return HostConfig.objects.all().order_by('-created_on')

    def post(self, request, *args, **kwargs):
        payload=request.data
        payload['created_by']=request.user.id
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message":"Host is added Successfully."}, 
                        status=status.HTTP_201_CREATED, headers=headers)


class HostAuditRedemAPIView(generics.CreateAPIView):
    http_method_names = ['post']
    # permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self,request):
        host_id=request.data.get("host_id")
        operation=request.data.get("operation")
        host_obj=get_object_or_404(HostConfig,pk=host_id)
        if operation == 1:
            msg="Aduit Started Successfully.You will received email"
        elif operation == 2:
            msg = "Remediation Started Successfully.You will received email"
        if host_obj.os_type == HostConfig.UBUNTU:
            if operation == 1:
                playbook_path = settings.ANISBLE_PLAYBOOK_UBUNTU_AUDIT_DIR
            elif operation == 2:
                playbook_path = settings.ANISBLE_PLAYBOOK_UBUNTU_REMED_DIR
        elif host_obj.os_type == HostConfig.CENTOS:
            if operation == 1:
                playbook_path = settings.ANISBLE_PLAYBOOK_CENTOS_AUDIT_DIR
            elif operation == 2:
                playbook_path = settings.ANISBLE_PLAYBOOK_CENTOS_REMED_DIR
        private_data_dir = settings.ANISBLE_PLAYBOOK_PRIVATE_DIR
        a=anisblerunner.delay(host_id,operation,playbook_path,private_data_dir)
        return Response({"message":msg}, status=status.HTTP_200_OK)
    


class HostConnectionCheck(generics.CreateAPIView):
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]


    def run_cat_command(self,private_ip, username, password):
        try:
            # Establish an SSH connection
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(private_ip, username=username, password=password)

            # Execute the cat command on the remote server
            command = f"cat /etc/os-release"
            _, stdout, stderr = client.exec_command(command)
            
            # Check for errors
            error_message = stderr.read().decode('utf-8').strip()
            if error_message:
                print(f"Error executing command: {error_message}")
                return '',status.HTTP_400_BAD_REQUEST

            # Print the output of the cat command
            output = stdout.read().decode('utf-8')
            print(f"Contents of OS on {private_ip}:\n{output}")

            # Close the SSH connection
            client.close()

            return output,status.HTTP_200_OK
        except Exception as e:
            print(f"Error: {e}")
            return '',500

    def post(self, request):
        host_id=request.data.get("ip_address")
        uname=request.data.get("username")
        pwd = request.data.get("password")
        os_type = request.data.get("os_type")

        # connects via ssh connection and returns the OS details as output
        output,statusCode = self.run_cat_command(host_id, uname, pwd)

        if statusCode != status.HTTP_200_OK:
            return Response({"message":"connection failed"},status=status.HTTP_400_BAD_REQUEST)

        # os details are filtered and converted to a python readable dictionary
        os_config = dict(re.findall(r'(\S+)=(\S+)', output))
        print("os_config: ", os_config)

        # Eg. NAME: Ubuntu | VERSION_ID: 22.04
        os_name = os_config["NAME"].replace('"','')
        os_version_id = os_config["VERSION_ID"].replace('\"','')

        print(f"os_name: {os_name} | ui os_type: {os_type}")
        if os_name.lower() != os_type.lower():
            return Response({"message":"os mismatch, please provide valid input"},status=status.HTTP_400_BAD_REQUEST)

        return Response({"os_name": os_name, "os_version_id":os_version_id}, 
                        status=status.HTTP_200_OK)

    


