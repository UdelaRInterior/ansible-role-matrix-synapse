# Change Log

## [v3.3.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v3.3.0)

* Now it is possible to configure an external mail server to send notifications. Postfix is kept as the default option but it is not installed and configured unnecessarily if it will not be used.

## [v3.2.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v3.2.0)

* Now the nginx reverse proxy settings are based on the [official Matrix Synapse documentation](https://matrix-org.github.io/synapse/latest/reverse_proxy.html). Additionally, the `synapse_enable_admin_endpoints` boolean variable was added to enable or disable publishing of admin API endpoints.

## [v3.1.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v3.1.0)

* Small change on python package name and the role now support Debian Bullseye. The psycopg2 package name is inferred from the system to maintain backward compatibility with Stretch and Buster.

## [v3.0.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v3.0.0)

* Version 2.0.0 of the role is not able to install Element web app from version 1.7.15. Since version 3.0.0, this role is compatible with [Element web app version 1.7.15](https://github.com/vector-im/element-web/releases/tag/v1.7.15) and above, but is not compatible with Riot/Element versions 1.7.14 and olders.

## [v2.0.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v2.0.0)

* Fix coTURN configuration issues. Now the default value of `synapse_turn_port` is set to at 3478
* [Riot is now Element!](https://element.io/blog/welcome-to-element/). Due to the rebrand of the web client, the documentation and all variables `riot_*` were renamed to `element_*` to keep up to date.

## [v1.6.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.6.0)

* Now you can manage max upload file size

## [v1.5.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.5.0)

* Now you can manage reCAPTCHA registration and tokens

## [v1.4.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.4.0)

* Added CoTURN installation and integration

## [v1.3.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.3.0)

* Added Riot web app UI customization
  * Custom welcome page template
  * [Branding](https://github.com/vector-im/riot-web/blob/develop/docs/config.md)
  * [Custom themes](https://github.com/vector-im/riot-web/blob/develop/docs/theming.md#custom-themes)

## [v1.2.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.2.0)

* Added LDAP integration

## [v1.1.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.1.0)

* Added Postfix and mailing configuration

* Added upgrade option from parameter

## [v1.0.0](https://github.com/UdelaRInterior/ansible-role-matrix-synapse/tree/v1.0.0)

* First stable version. Includes: Nginx reverse proxy, PostgreSQL database and Riot web client