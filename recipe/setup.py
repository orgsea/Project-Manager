from setuptools import setup

entry_point = 'virtenv:Virtenv'
entry_points = {"zc.buildout": ["virtenv = %s" % entry_point]}

setup(
    name='recipe',
    entry_points=entry_points,
    install_requires=[
        'virtualenv>=1.4',
        ],

    )
