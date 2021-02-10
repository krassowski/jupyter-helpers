from setuptools import setup
from setuptools import find_packages


try:
    from pypandoc import convert

    def get_long_description(file_name):
        return convert(file_name, 'rst', 'md')

except ImportError:

    def get_long_description(file_name):
        with open(file_name) as f:
            return f.read()


if __name__ == '__main__':
    setup(
        name='jupyter_helpers',
        packages=find_packages(),
        version='0.2.2',
        license='MIT',
        description='A collection of helpers for using IPython in Jupyter(Lab)',
        long_description=get_long_description('README.md'),
        author='Michal Krassowski',
        author_email='krassowski.michal+pypi@gmail.com',
        url='https://github.com/krassowski/jupyter-helpers',
        keywords=['ipython', 'jupyter', 'jupyterlab', 'notebook', 'helpers'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Framework :: IPython',
            'Framework :: Jupyter',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Topic :: Utilities',
            'Topic :: Software Development :: User Interfaces',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.9'
        ],
        install_requires=[
            'pandas', 'pygments', 'ipywidgets', 'IPython', 'jupyterlab_widgets'
        ],
    )
