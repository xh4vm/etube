from setuptools import setup

setup(
   name='jaeger_telemetry',
   version='0.1.0',
   author='Command number FOUR',
   packages=[
      'jaeger_telemetry',
      'jaeger_telemetry.configurations',
   ],
   install_requires=[
        'opentelemetry-api >= 1.12.0',
        'opentelemetry-sdk >= 1.12.0',
        'opentelemetry-exporter-jaeger >= 1.12.0',
   ],
)
