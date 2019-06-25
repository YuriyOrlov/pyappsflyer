from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyappsflyer',
      version='0.1',
      description='Unofficial python wrap for AppsFlyer API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/YuriyOrlov/pyappsflyer',
      author='Yuriy Orlov',
      author_email='navuchodonsr@yandex.ru',
      license='MIT',
      packages=['pyappsflyer'],
      install_requires=[
          'furl==2.0.0',
          'environs==4.2.0'
      ],
      zip_safe=False)