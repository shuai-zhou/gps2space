from setuptools import setup

setup(name='GPS2space',
      version='0.1',
      description='Toolbox for building spatial data and activity space from raw GPS data',
      url='https://github.com/shuai-zhou/GPS2space',
      author='Shuai Zhou',
      author_email='sxz217@psu.edu',
      license='MIT',
      packages=['GPS2space'],
      include_package_data=True,
      install_requires=['pandas',
                                  'geopandas',
                                  'numpy',
                                  'scipy',
                                  'shapely'],
      zip_safe=False)
