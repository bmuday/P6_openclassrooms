"""
Name: AD_CLIENT - Manage Active Directory Operations
Author :  Mickael MARTIAL
Email   : mickaelmartial22@gmail.com
Date Started : 12 AOUT 2021
Date Modified :
Description : Send Directory Service Commands to AD Bot

"""


import rpyc
import datetime
import csv


AD_SERVER_IP = '192.168.1.10'
AD_BOT_PORT = 19961
domain_controller = 'DC=pliane,DC=net'
users_ou = 'OU=siege,{}'.format(domain_controller)
groups_ou = 'OU=direction,{}'.format(domain_controller)


def send_command(command):
    if not command:
        return
    try:
        connection = rpyc.connect(AD_SERVER_IP, AD_BOT_PORT)
        connection.root.run_command(command)
    except Exception as Err:
        print('Error in send command', str(Err))


def create_users():
    """
    Create New user in AD
    :return:
    """
    with open('sample.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            username = row['username']
            employee_id = row['employee_id']
            display_name = row['display_name']
            print(username, employee_id, display_name)

            description = "Users added by AD BOT on  {}".format(datetime.datetime.now())
            default_password = 'P@ssw0rd'

            dn = '"CN={},{}"'.format(username, users_ou)
            groups = '"cn=siege,{}" ' \
             '"cn=USB_Deny,{}" '.format(groups_ou,
                                        groups_ou)
            command = 'dsadd user ' \
              '{} ' \
              '-samid "{}" ' \
              '-upn "{}" ' \
              '-display "{}" ' \
              '-empid "{}" ' \
              '-desc "{}" ' \
              '-pwd {} ' \
              '-pwdneverexpires yes ' \
              '-mustchpwd yes ' \
              '-memberof {} ' \
              '-acctexpires never ' \
              ''.format(
                dn,
                username,
                username,
                display_name,
                employee_id,
                description,
                default_password,
                groups,
                )
            send_command(command)


def create_user(username, employee_id, display_name):
    """
    Create New user in AD
    :param username:
    :param employee_id:
    :param display_name:
    :return:
    """
        
    description = "User added by AD BOT on  {}".format(datetime.datetime.now())
    default_password = 'P@ssw0rd'

    dn = '"CN={},{}"'.format(username, users_ou)
    groups = '"cn=siege,{}" ' \
             '"cn=USB_Deny,{}" '.format(groups_ou,
                                        groups_ou)
    command = 'dsadd user ' \
              '{} ' \
              '-samid "{}" ' \
              '-upn "{}" ' \
              '-display "{}" ' \
              '-empid "{}" ' \
              '-desc "{}" ' \
              '-pwd {} ' \
              '-pwdneverexpires yes ' \
              '-mustchpwd yes ' \
              '-memberof {} ' \
              '-acctexpires never ' \
              ''.format(
                dn,
                username,
                username,
                display_name,
                employee_id,
                description,
                default_password,
                groups,
                )
    send_command(command)
    print("création de l'utilisateur {}".format(username))


def manage_user(username, mode):
    """
    This function can manage active directory users
    :param username:
    :param mode:
    :return:
    """
    dn = 'CN={},{}'.format(username, users_ou)
    cmd = ''
    if mode == 'disable':
        cmd = 'dsmod user {} -disabled yes'.format(dn)
    elif mode == 'enable':
        cmd = 'dsmod user {} -disabled no'.format(dn)
    elif mode == 'delete':
        cmd = 'dsrm -noprompt "cn={},{}"'.format(username, users_ou)
    send_command(cmd)
    


def manage_users(mode):
    """
    This function can manage active directory users
    :param mode:
    :return:
    """
    with open('sample.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            username = row['username']
            
            dn = 'CN={},{}'.format(username, users_ou)
            cmd = ''
            if mode == 'disable':
                cmd = 'dsmod user {} -disabled yes'.format(dn)
            elif mode == 'enable':
                cmd = 'dsmod user {} -disabled no'.format(dn)
            elif mode == 'delete':
                cmd = 'dsrm -noprompt "cn={},{}"'.format(username, users_ou)
            send_command(cmd)
    print('suppression de tous les comptes utilisateurs')

def user_password_change(username, new_password):
    """
    This function can change active directory password
    :param new_password:
    :param username:
    :return:
    """
    dn = 'CN={},{}'.format(username, users_ou)
    cmd = 'dsmod user {} -pwd {} -mustchpwd yes'.format(dn, new_password)
    send_command(cmd)


def ad_group(group_name, mode):
    """
    Add and Remove Group
    :param group_name:
    :param mode:
    :return:
    """
    cmd = ''


    if mode == 'add':
        group_description = 'Group created by AD Bot'
        cmd = 'dsadd group "cn={}, {}"' \
              ' -desc "{}"'.format(group_name, groups_ou, group_description)
    elif mode == 'remove':
        cmd = 'dsrm -noprompt "cn={},{}"'.format(group_name, groups_ou)
    send_command(cmd)


def group_user(group_name, mode, username):
    """
    Add and Remove User from groups
    :param group_name:
    :param mode:
    :param username:
    :return:
    """
    dn = 'CN={},{}'.format(username, users_ou)
    cmd = ''
    if mode == 'add':
        cmd = 'dsmod group "cn={},{}"' \
              ' -addmbr "{}"'.format(group_name, groups_ou, dn)
    elif mode == 'remove':
        cmd = 'dsmod group "cn={},{}"' \
              ' -rmmbr "{}"'.format(group_name, groups_ou, dn)
    send_command(cmd)