import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_nginx_is_installed(host):
	nginx = host.package("nginx")
	assert nginx.is_installed

def test_nginx_is_enabled_and_running(host):
	nginx = host.service("nginx")
	assert nginx.is_running
	assert nginx.is_enabled

def test_postfix_is_installed(host):
	postfix = host.package("postfix")
	assert postfix.is_installed

def test_postfix_is_enabled_and_running(host):
	postfix = host.service("postfix")
	assert postfix.is_running
	assert postfix.is_enabled

def test_postgresql_is_installed(host):
	postgresql = host.package("postgresql")
	assert postgresql.is_installed

def test_postgresql_is_enabled_and_running(host):
	postgresql = host.service("postgresql")
	assert postgresql.is_running
	assert postgresql.is_enabled

def test_homeserver_file_exists(host):
  f = host.file('/var/lib/matrix-synapse/homeserver.yaml')
  assert f.exists
  assert f.user == 'root'
  assert f.group == 'root'

def test_synapse_is_enabled_and_running(host):
	assert host.service("matrix-synapse")
