from setuptools import setup

dependency_links = [
    'git+https://github.com/KaiHannemann/coordination-simulation'
]


setup(
    name='simianarmy',
    version='0.1.0',
    description='Basic fault injection framework',
    url='https://github.com/KaiHannemann/simian-army',
    author='Kai Arne Hannemann',
    author_email='kaiha@mail.upb.de',
    packages=['simianarmy', 'simianarmy.Monkeys', 'simianarmy.metrics', 'simianarmy.eval'],
    zip_safe=False
)
