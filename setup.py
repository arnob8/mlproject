from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
  #in short => My function will return a liist
  '''
  This function will return the list of requirements
  '''
  requirements=[]
  with open(file_path) as file_obj:
     #temp file object ccreated
     requirements=file_obj.readlines()
     requirements = [req.replace("\n","")for req in requirements]

     if HYPEN_E_DOT in requirements:
      requirements.remove(HYPEN_E_DOT)
  return requirements

setup(
    name = 'mlproject',
    version = '0.0.1',
    author = 'Arnob',
    author_email = 'arnob8@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)