from setuptools import setup, find_packages


long_description = """
     So, its simple libriary for easy managment of json files and for creating a data model in them. 
     And also an appeal to models in the most simple and beautiful form
"""

short_description = 'Create models in json file.'
version = '1.0.0'

setup(
     name='json_orm',
     version=version,
     description=short_description,
     long_description=long_description,
     long_description_content_type='text/markdown',
     url='https://github.com/shayzi3/json_orm',
     author='shayzi3',
     author_email='tecnomega@mail.ru',
     packages=find_packages(),
     keywords='json orm model file python',
     requires=[
          'pydantic',
          'typing_extensions'
     ]
)


