import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ntp_package(host):
    p = host.package('ntp')
    assert p.is_installed


@pytest.mark.parametrize('ntpserver', ['0', '1', '2', '3'])
def test_ntp_client(host, ntpserver):
    ntpconf = host.file('/etc/ntp.conf')
    assert ntpconf.exists
    assert ntpconf.user == 'root'
    assert ntpconf.group == 'root'
    assert ntpconf.contains("server %s.us.pool.ntp.org" % ntpserver)


def test_ntp_service(host):
    assert host.service('ntpd').is_enabled
    assert host.service('ntpd').is_running
