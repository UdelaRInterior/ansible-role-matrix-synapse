# Ansibe Role Matrix Synapse

[![Build Status](https://travis-ci.com/UdelaRInterior/ansible-role-matrix-synapse.svg?branch=master)](https://travis-ci.com/github/UdelaRInterior/ansible-role-matrix-synapse) [![Galaxy](https://img.shields.io/badge/galaxy-UdelaRInterior.matrix__synapse-blue.svg)](https://galaxy.ansible.com/udelarinterior/matrix_synapse) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/udelarinterior/ansible-role-matrix-synapse?label=release&logo=github&style=social) ![GitHub stars](https://img.shields.io/github/stars/udelarinterior/ansible-role-matrix-synapse?style=social) ![GitHub forks](https://img.shields.io/github/forks/udelarinterior/ansible-role-matrix-synapse?style=social)

### Automated installation from source with Nginx reverse proxy and PostgreSQL database

Role that automates the installation, upgrade and configuration of a Matrix Synapse homeserver using the [`from source`](https://github.com/matrix-org/synapse/blob/master/INSTALL.md#installing-from-source) method, recommended option to have the most updated version that doesn't suffer known security vulnerabilities.

Also based on the recommendation, a Nginx reverse proxy and valid Let's Encrypt certificates are configured to simplify communication with clients and federated servers.

As a database server, it is possible to use PostgreSQL (recommended for production environments) and SQLite (recommended for small or testing environments). The role default option is PostgreSQL, contemplating its installation and configuration.

A simple Postfix local installation or a external SMTP server makes it possible to send notifications, account recovery, etc. via email. With easily customizable templates through variables.

Optionally this role allows provisioning a CoTURN installation to [enable VoIP relaying on your matrix homeserver with TURN](https://github.com/matrix-org/synapse/blob/master/docs/turn-howto.md).

Through authentication providers it's possible to integrate decentralized logins. This role implements integration with LDAP optionally.

Finally, this role also allows you to serve the [Element](https://app.element.io/) (formerly Riot) web application together with Synapse. This feature is disabled by default (`synapse_installation_with_element: false`) due to the [project security recommendation](https://github.com/vector-im/element-web/#important-security-note). But serve Element is very useful. Fully recommended if you have the posibility to destiny different domain names for Synapse and Element (`synapse_server_name` != `element_server_name`). Otherwise you can install both in the same domain name at your own risk (`synapse_server_name` == `element_server_name`).

Since version 3.0.0, this role is compatible with [Element web app version 1.7.15](https://github.com/vector-im/element-web/releases/tag/v1.7.15) and above, but is not compatible with Riot/Element versions 1.7.14 and olders.

Deployment diagram
------------

## Basic installation

The essential installation to have your own matrix homeserver ready for production (Note that this is the role's default behavior):
```
                        80,443,8448/tcp           25/tcp
                              |                     |
+-----------------------------|------------+   +----+----+
|                             |            |   | Postfix |
|  Nginx server               |            |   +----^----+
|                   +---------v----------+ |        |
|                   | Reverse Proxy Site | |        |
|                   +----------------^---+ |        |
+------------------------------------|-----+        |
                                     | 8008/tcp     |
                                  +--v--------------+-----+
   +-------------------+ 5432/tcp |                       |
   | PostgreSQL Server |<---------+ Matrix Synapse Server |
   +-------------------+          |                       |
                                  +-----------------------+
```

## Full installation

The typical and recommended use case consists on deploy the following architecture (Note that this is the role's default behavior, with the addition of setting `synapse_installation_with_element` and `synapse_with_turn` to `true` ):
```
         +~~~~~~~~~~~~~~~~~~~~~~~~~+
         |    Element Web App      |
         | (Run on client browser) |<----<---+
         +~~~~~~~~~~~~~~~~~~~~~~~~~+         |
                                 ^           v
                                 ^           |                         3478,5349/tcp&upd
   GET on 80,443/tcp will return ^       443,8448/tcp         25/tcp    49152:65535/udp
                  |                          |                   |         |
+-----------------|--------------------------|-------------------|---------|------+
|                 |                          |                   |         |      |
|  +--------------|--------------------------|----------+   +----+----+    |      |
|  | Nginx server |                          |          |   | Postfix |    |      |
|  |   +----------v--------+                 |          |   +----^----+    |      |
|  |   |   Standard Site   |     +-----------v--------+ |        |         |      |
|  |   |  (Serve riot.js)  |     | Reverse Proxy Site | |        |         |      |
|  |   +-------------------+     +----------------^---+ |        |         |      |
|  +----------------------------------------------|-----+        |         |      |
|                                                 | 8008/tcp     |         |      |
|                                             +---v--------------+----+    |      |
|              +-------------------+ 5432/tcp |                       |    |      |
|              | PostgreSQL Server |<---------+ Matrix Synapse Server |    |      |
|              +-------------------+          |                       |    |      |
|                                             +--------------------^--+    |      |
|                                                                  |       |      |
|                                                3478,5349/tcp&upd |       |      |
|                                                      +-----------v-------v-+    |
|                                                      |    coTURN Server    |    |
|   Your Debian                                        +---------------------+    |
|   based server                                                                  |
+---------------------------------------------------------------------------------+
```

Requirements
------------

Ansible version >= 2.7

Role Variables
--------------

```yaml
# Our friendly and public domain name for the Synapse
# server (the one that conforms user ID and room alias)
# eg: my-organization.org (you would get @users:my-organization.org and #rooms:my-organization.org)
synapse_server_name: "{{ inventory_hostname }}"

# FQDN of the server that effectively hosting synapse (matrix endpoint)
# eg: matrix.my-organization.org
synapse_server_fqdn: "{{ inventory_hostname }}"

# Location where synapse will be downloaded and installed from PyPI
synapse_installation_path: /var/lib/matrix-synapse

# present : Keep the same version once synapse was installed or
# latest : upgrade it if there is a new upgrade available from pip
# IF YOU PLAN TO UPGRADE, CHECK FIRST: https://github.com/matrix-org/synapse/blob/master/UPGRADE.rst
synapse_pip_state: present

# If you want to install specific version of matrix-synapse
# change it for something like: "matrix-synapse==1.12.4"
matrix_synapse_pip_pkg: "matrix-synapse"

# Enable sign up for new users
synapse_enable_registration: "false"
synapse_enable_registration_with_captcha: false
synapse_recaptcha_public_key: 2Q1toXytnLYl4WIrpWgvBJOaQS1Ym36tNAJnKcZY
synapse_recaptcha_private_key: QgsOB0r79J9fpn8fAAnEIiITv7IMnjnUftdJwThs

synapse_report_stats: 'no'

# The largest allowed upload size in bytes
synapse_max_upload_size: 10M

# Endpoints for administering your Synapse instance are placed under /_synapse/admin. These require
# authentication through an access token of an admin user. However as access to these endpoints grants
# the caller a lot of power, we do not recommend exposing them to the public internet without good reason.
# See https://matrix-org.github.io/synapse/latest/reverse_proxy.html
synapse_enable_admin_endpoints: false

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

synapse_smtp_host: localhost
synapse_smtp_port: 25
# synapse_smtp_user: synapse
# synapse_smtp_pass: secret

synapse_email_hostname: "{{ synapse_server_fqdn }}"
synapse_email_notif_from: "MyOrganization Matrix Homeserver <matrix@myorganization.com>"

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

###  TURN
synapse_with_turn: false
synapse_turn_uri: "{{ synapse_server_fqdn }}"
synapse_turn_port: 3478  # TURN listener TCP&UDP port: 3478(default) 5349(for TLS)
synapse_turn_shared_secret: 5Eydym68SovsZkYLT8G9TOSCFwc2E6ijVLwL4FQgbukKPUalQZOe5gj22E9EhYrm # change it and put it from a vault
synapse_turn_user_lifetime: 86400000
synapse_turn_allow_guests: True
synapse_turn_denied_peer_ip:
  - 10.0.0.0-10.255.255.255
  - 172.16.0.0-172.31.255.255
  - 192.168.0.0-192.168.255.255
synapse_turn_allowed_peer_ip:
    # The turn server itself (special case) so that client->TURN->TURN->client flows work
  - "{{ ansible_default_ipv4.address if(ansible_default_ipv4.address) is defined else '' }}"
  - "{{ ansible_default_ipv6.address if(ansible_default_ipv6.address) is defined else '' }}"

### Element Web App
# Also install the Element web application along synapse
synapse_installation_with_element: false
element_installation_path: /var/www/element
# Our public domain name for the Element Web client
# eg: element.my-organization.org
element_server_name: "{{ synapse_server_name }}"
# Look https://github.com/vector-im/element-web/releases to use the latest version
element_version: '1.7.15'
element_jitsi_preferred_domain: jitsi.riot.im
# Name to display for the server
element_display_name: 'My Org Chat'
element_default_theme: light # 'light', 'dark' or your own 'custom-${theme-name}' (see element_custom_themes below)
element_default_country_code: GB

### Element UI customization
element_customatize_ui: false

element_welcome_page_template_src: var/www/element/custom-welcome.html.j2   # Leave it empty if you don't want to overwrite the default Element welcome page
element_welcome_logo_url: welcome/images/logo.svg
element_welcome_title: 'Welcome to Element!'
element_welcome_description: 'Decentralised, encrypted chat &amp; collaboration powered by [matrix]'

element_custom_branding:
  welcomeBackgroundUrl: themes/element/img/backgrounds/lake.jpg
  authHeaderLogoUrl: themes/element/img/logos/element-logo.svg
  authFooterLinks:
    - text: blog
      url: https://element.io/blog
    - text: twitter
      url: https://twitter.com/element_hq
    - text: github
      url: https://github.com/vector-im/riot-web

element_custom_themes:
  - name: "Deep Purple"
    is_dark: true
    colors:
      accent-color: "#6503b3"
      primary-color: "#368bd6"
      warning-color: "#b30356"
      sidebar-color: "#15171B"
      roomlist-background-color: "#22262E"
      roomlist-text-color: "#A1B2D1"
      roomlist-text-secondary-color: "#EDF3FF"
      roomlist-highlights-color: "#343A46"
      roomlist-separator-color: "#a1b2d1"
      timeline-background-color: "#181b21"
      timeline-text-color: "#EDF3FF"
      timeline-text-secondary-color: "#A1B2D1"
      timeline-highlights-color: "#22262E"
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
