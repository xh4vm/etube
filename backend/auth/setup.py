from setuptools import setup


setup(
   name='auth',
   version='0.1.0',
   author='Command number FOUR',
   packages=[
      'auth_client',
      'auth_client.core',
      'auth_client.errors',
      'auth_client.tests',
      'auth_client.src',
      'auth_client.src.grpc',
      'auth_client.src.local',
      'auth_client.src.grpc.messages'
   ],
   install_requires=[
        "grpcio >= 1.47.0",
        "grpcio-tools >= 1.47.0",
        "protobuf >= 3.20.1",
        "pydantic >= 1.9.1",
        "six >= 1.16.0",
        "PyJWT >= 2.4.0",
        "Flask >= 2.1.2",
   ],
)
