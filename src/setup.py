from setuptools import setup

setup(
    name='banana-inspector',
    version='0.0.1',
    packages=['banana_inspector', 'banana_inspector.apps', 'banana_inspector.util', 'banana_inspector.nodes',
              'banana_inspector.resources'],
    package_dir={'': 'src'},
    url='https://github.com/daliagachc/banana-inspector',
    license='MIT',
    author='diego aliaga',
    author_email='diego.aliaga',
    description='inspect atmospheric new particle formation events'
)
