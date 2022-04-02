# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coolsql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coolsql',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/coolsql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

