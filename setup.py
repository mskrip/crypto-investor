from setuptools import setup, find_packages

requirements = [
    'flask',
    'pyyaml',
    'requests',
    'uwsgi'
]

test_requirements = []

try:
    with open('requirements/test.txt', 'r') as f:
        test_requirements = [line.strip() for line in f]
except FileNotFoundError:
    pass

setup(
    name='crypto-investor',
    version='1.0.0',
    description='Project for course Extreme programming',
    url='https://github.com/mskrip/crypto-investor',
    author='Tomas Slama, Samuel Wendl, Matej Vilk, Marian Skrip',
    author_email='marian.skripp@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    keywords='crypto cryptocurrency game simulator',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'test': test_requirements
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cryptoinvestor=cryptoinvestor.main:main'
        ]
    }
)
