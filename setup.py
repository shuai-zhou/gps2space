from setuptools import setup

setup(name='gps2space',
      version='0.2',
      description='Toolbox for building spatial data and activity space and shared space from raw GPS data',
      url='https://github.com/shuai-zhou/gps2space',
      author='Shuai Zhou',
      author_email='sxz217@psu.edu',
      license='MIT',
      packages=['gps2space'],
      include_package_data=True,
      install_requires=['pandas',
                        'geopandas',
                        'numpy',
                        'scipy',
                        'shapely'],
      zip_safe=False)
