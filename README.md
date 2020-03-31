# Ansibe Role Matrix Synapse 

[![Build Status](https://travis-ci.org/UdelaRInterior/ansible-role-matrix-synapse.svg?branch=master)](https://travis-ci.org/UdelaRInterior/ansible-role-matrix-synapse)
[![Galaxy](https://img.shields.io/badge/galaxy-UdelaRInterior.matrix_synapse-blue.svg)](https://galaxy.ansible.com/udelarinterior/matrix_synapse)

### Automated installation from source with Nginx reverse proxy and PostgreSQL database

Role that automates the installation, update and configuration of a Matrix Synapse homeserver using the [`from source`](https://github.com/matrix-org/synapse/blob/master/INSTALL.md#installing-from-source) method, recommended option to have the most updated version that doesn't suffer known security vulnerabilities.

Also based on the recommendation, a Nginx reverse proxy and valid Let's Encrypt certificates are configured to simplify communication with clients and federated servers.

As a database server, it is possible to use PostgreSQL (recommended for production environments) and SQLite (recommended for small or testing environments). The role default option is PostgreSQL, contemplating its installation and configuration.

A simple Postfix installation makes it possible to send notifications, account recovery, etc. via email. With easily customizable templates through variables.

Through authentication providers it's possible to integrate decentralized logins. This role implements integration with LDAP optionally.

Finally, this role also allows you to serve the [Riot web](https://riot.im/app/#/welcome) application together with Synapse. This feature is disabled by default (`synapse_installation_with_riot: false`) due to the [project security recommendation](https://github.com/vector-im/riot-web/#important-security-note). But serve Riot is very useful. Fully recommended if you have the posibility to destiny different domain names for Synapse and Riot (`synapse_server_name` != `riot_server_name`). Otherwise you can install both in the same domain name at your own risk (`synapse_server_name` == `riot_server_name`).

Deployment diagram
------------

The typical use case consists on deploy the following architecture (Note that this is the role's default behavior, only with the addition of setting `synapse_installation_with_riot` to `true`):

```
                80,443/tcp        80,443,8448/tcp           25/tcp
                    |                   |                     |
+-------------------|-------------------|------------+   +----+----+
|  Nginx server     |                   |            |   | Postfix |
|                   |                   |            |   +----^----+
|   +---------------v---+     +---------v----------+ |        |
|   |  Standard  Site   |     | Reverse Proxy Site | |        |
|   +--------+----------+     +---^------------^---+ |        |
+------------|--------------------|------------|-----+        |
             |             443/tcp|            | 8008/tcp     |
             |              ______|         +--v--------------+-----+
             |             /                |                       |
      +------v-------+    /                 | Matrix Synapse Server |
      | Riot Web App |___/                  |                       |
      +--------------+                      +------------+----------+
                                                         | 5432/tcp
                                              +----------v--------+
                                              | PostgreSQL Server |
                                              +-------------------+
```

Requirements
------------

Ansible version >= 2.7

Role Variables
--------------

```yaml
# Our friendly and public domain name for the Synapse
# server (the one that conforms user ID and room alias)
synapse_server_name: "{{ inventory_hostname }}"
# FQDN of the server that effectively hosting synapse
synapse_server_fqdn: "{{ inventory_hostname }}"

# Location where synapse will be downloaded and installed from PyPI
synapse_installation_path: /var/lib/matrix-synapse

# present : Keep the same version once synapse was installed or
# latest : update it if there is a new update available from pip
synapse_pip_state: present

# Enable sign up for new users
synapse_enable_registration: "false"
synapse_report_stats: 'no'

# Local sources to templates and configuration files, useful
# for overwriting if you want to use your own templates in conf.d
synapse_confd_templates_src: var/lib/matrix-synapse/conf.d

### Install and configure Synapse with PostgreSQL Server
synapse_with_postgresql: true
# PostgreSQL credentials
synapse_psql_db_name: matrix-synapse
synapse_psql_db_host: localhost
synapse_psql_user: matrix-synapse
synapse_psql_password: secret-password

### Email
# If email is not configured, password reset, registration and notifications via email will be disabled.
synapse_email_enable: true
synapse_email_hostname: "{{ synapse_server_fqdn }}"
synapse_email_notif_from: "YourFriendlyhomeserver" # without spaces

synapse_email_with_custom_templates: false
# If true, remember use a customized version of the template conf.d/email.yaml.j2 to reference them
synapse_email_templates_src: email_notif_templates
synapse_email_templates_dest: "{{ synapse_installation_path }}/email_notif_templates"

###  LDAP
synapse_with_ldap_authentication: false
synapse_ldap_uri: ldap.example.com:389
synapse_ldap_start_tls: 'true'
synapse_ldap_base: ou=users,dc=example,dc=com
synapse_ldap_uid: cn
synapse_ldap_mail: email
synapse_ldap_name: givenName
synapse_ldap_bind_dn: ""
synapse_ldap_bind_password: ""

### Riot Web App
# Also install the riot web application along synapse
synapse_installation_with_riot: false
riot_installation_path: /var/www/riot
# Our public domain name for the Riot Web client
riot_server_name: "{{ synapse_server_name }}"
# Look https://github.com/vector-im/riot-web/releases to use the latest version
riot_version: '1.5.6'
# Name to display for the server
riot_display_name: 'My Org Chat'
riot_default_theme: light # light or dark
riot_default_country_code: GB
```

Dependencies
------------

This role depends of [geerlingguy.certbot](https://galaxy.ansible.com/geerlingguy/certbot) to generate and renew valid Let's Encrypt certificates that allow proper communication with clients and other federated servers

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
    - role: udelarinterior.matrix_synapse
      vars:
        synapse_enable_registration: "true"
        synapse_with_postgresql: true
        synapse_psql_db_name: matrix-synapse
        synapse_psql_db_host: localhost
        synapse_psql_user: matrix-synapse
        synapse_psql_password: my-password
        certbot_admin_email: admin@my-organization.org
        certbot_certs:
          - domains:
            - "{{ synapse_server_name }}"
            - 'msg.my-organization.org'
            - 'chat.my-organization.org'
```

License
-------

(c) Universidad de la República (UdelaR), Red de Unidades Informáticas de la UdelaR en el Interior. Licenced under GPL-v3.


Author Information
------------------

[@santiagomr](https://github.com/santiagomr)
[@UdelaRInterior](https://github.com/UdelaRInterior)
https://proyectos.interior.edu.uy/
