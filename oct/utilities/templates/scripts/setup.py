from setuptools import setup


setup(
    name='{{ name }}',
    version='0.1',
    install_requires=[
        {% for item in turrets_requirements %}
        '{{ item }}',
        {% endfor %}
        'oct-turrets'
    ]
)
