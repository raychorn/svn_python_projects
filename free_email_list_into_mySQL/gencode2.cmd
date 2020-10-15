@echo off


sqlautocode -t freeemailhost__c mysql://root:peekaboo@localhost:3306/free_email_list -o free_email_tables.py
