"""
Name: Active Directory Operations
Author :  Mickael MARTIAL
Email   : mickaelmartial22@gmail.com
Date Started : 12 AOUT 2021
Description : Desktop client for Stdio Line Production pipeline

"""
import adClient


#adClient.create_users()
adClient.create_user('bmuday', 'BAM', 'Baptiste MUDAY')
#adClient.manage_users( mode='delete') 
#adClient.manage_user('bmuday', mode='delete') 
#adClient.manage_user('ajean','enable') 
#adClient.manage_user('ajean','disable') 
#adClient.ad_group('info', mode='add') 
#adClient.ad_group('info', mode='remove')
#adClient.group_user('info','add', 'ajean')
#adClient.group_user('tech','add','jbique')
#adClient.user_password_change('ajean', 'Pleld2000')