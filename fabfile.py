from socket import error as socket_error
import os
from dotenv import load_dotenv

from fabric import Connection
from invoke import Responder
from paramiko.ssh_exception import AuthenticationException


class ExampleException(Exception):  # Should be your Exception
    pass


class Host(object):
    def __init__(self,
                 host_ip,
                 key_file_path):
        self.host_ip = host_ip
        self.key_file_path = key_file_path

    def _get_connection(self):
        connect_kwargs = {'key_filename': self.key_file_path}

        try:
            print("Connecting to host")
            connection = Connection(host=self.host_ip, connect_kwargs=connect_kwargs)
        except:
            print("Error connecting to host")
            connection = None

        return connection

    def run_command(self, command):
        try:
            with self._get_connection() as connection:
                print('Running `{0}` on {1}'.format(command, self.host_ip))
                result = connection.run(command, warn=True, hide='stderr')
                # print(result)
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

        if result.failed:
            raise ExampleException(
                'The command `{0}` on host {1} failed with the error: '
                '{2}'.format(command, self.host_ip, str(result.stderr)))

    def run_prompt_xpectd_command(self, command, res_str):
        try:
            with self._get_connection() as connection:
                print("Running prompt expected command `{0}` on {1}".format(command, self.host_ip))
                passing = Responder(
                    pattern = 'Do you want to continue?',
                    response = res_str
                )
                result = connection.run(command, warn=True, hide='stderr', pty=True, watchers=[passing])
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

        if result.failed:
            raise ExampleException(
                'The command `{0}` on host {1} failed with the error: '
                '{2}'.format(command, self.host_ip, str(result.stderr)))

    def put_file(self, local_path, remote_path):
        try:
            with self._get_connection() as connection:
                print('Copying {0} to {1} on host {2}'.format(
                    local_path, remote_path, self.host_ip))
                connection.put(local_path, remote_path)
        except (socket_error, AuthenticationException) as exc:
            self._raise_authentication_err(exc)

    def _raise_authentication_err(self, exc):
        raise ExampleException(
            "SSH: could not connect to {host} "
            "(username: {user}, key: {key}): {exc}".format(
                host=self.host_ip,
                key=self.key_file_path, exc=exc))


if __name__ == '__main__':
    
    load_dotenv()
    path  = os.getcwd() + "/" + os.getenv('SSH_KEY')
    
    remote_host = Host(host_ip=os.getenv('HOST'),
                       key_file_path=path)
    
    # remote_host.run_command('sudo whoami')
    # remote_host.run_command('whoami')
    remote_host.run_prompt_xpectd_command('sudo apt remove python3-pip', 'Y \n')