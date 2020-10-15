@echo off
set PYTHONPATH=c:\python25;Z:\python projects\@lib;Z:\python projects\_django_0_96_3;Z:\python projects\_pyax-0.9.7.2-py2.5;Z:\python projects\_django-projects\@projects\www_pypi_info\django;Z:\python projects\_django_tagging;Z:\python projects\@SQLAlchemy-0_5_3\lib;
python manage.py syncdb --settings=settings
