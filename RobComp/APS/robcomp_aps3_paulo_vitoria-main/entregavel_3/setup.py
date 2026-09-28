from setuptools import find_packages, setup

package_name = 'entregavel_3'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='borg',
    maintainer_email='paulodoliveira13@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "quadrado = entregavel_3.quadrado:main",
            "limpador = entregavel_3.limpador:main",
            "indeciso = entregavel_3.indeciso:main",
        ],
    },
)
