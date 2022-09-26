from setuptools import setup, find_packages

setup(name="project-test-client",
      version="0.0.3",
      description="project-test-client",
      author="Pavel Zabrovskiy",
      author_email="pavel.zabrovskiy@bk.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
