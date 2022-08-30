from setuptools import setup


setup(
   name='auth',
   version='0.1.0',
   author='Command number FOUR',
   packages=[
      'auth_client',
      'auth_client.core',
      'auth_client.src.errors',
      'auth_client.src.exceptions',
      'auth_client.tests',
      'auth_client.src',
      'auth_client.src.services',
      'auth_client.src.services.access',
      'auth_client.src.messages',
   ],
   install_requires=[
         "backoff == 2.1.2",
         "grpcio == 1.47.0",
         "grpcio-tools == 1.47.0",
         "protobuf == 3.20.1",
         "pydantic == 1.9.1",
         "six == 1.16.0",
         "PyJWT == 2.4.0",
         "Flask == 2.1.2",
   ],
)
