from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="api-categorisation-messages",
    version="1.0.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="API Django REST pour la catégorisation automatique de messages SMS/transactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/projet_categorisation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-django>=4.5.2",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "mypy>=1.5.1",
            "bandit>=1.7.5",
            "safety>=2.3.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "categorisation-api=projet_categorisation.manage:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 