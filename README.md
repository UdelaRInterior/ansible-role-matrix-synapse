# Ansibe Role Matrix Synapse
### From source with Nginx reverse proxy and PostgreSQL / SQLite

Role that automates the installation and configuration of a Matrix Synapse homeserver using the [`from source`](https://github.com/matrix-org/synapse/blob/master/INSTALL.md#installing-from-source) method, recommended option to have the most updated version that doesn't suffer known security vulnerabilities.

Also based on the recommendation, a Nginx reverse proxy and valid Let's Encrypt certificates are configured to simplify communication with clients and federated servers.

As a database server, it is possible to use PostgreSQL (recommended for production environments) and SQLite (recommended for small or testing environments). The role default option is PostgreSQL, contemplating its installation and configuration.


Requirements
------------

Ansible version >= 2.7

Role Variables
--------------

```yaml
# Location where synapse will be downloaded and installed from PyPI
synapse_installation_path: /var/lib/matrix-synapse

# Our public domain name for the Synapse server
synapse_server_name: "{{ inventory_hostname }}"

synapse_report_stats: 'no'

# Enable sign up for new users
synapse_enable_registration: "false"

# Install and configure Synapse with PostgreSQL Server
synapse_with_postgresql: true

# PostgreSQL credentials
synapse_psql_db_name: matrix-synapse
synapse_psql_db_host: localhost
synapse_psql_user: matrix-synapse
synapse_psql_password: secret-password
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