from setuptools import setup

setup(
   name='vivarium',
   version='0.0',
   description='Ecological Environment based on SimplePlaygrounds (former Flatland)',
   author='Younès Rabii',
   author_email='yrabii@ensc.fr',
   packages=['vivarium'],  #same as name
   install_requires=['simple_playgrounds=0.9.18','tqdm'],
)
