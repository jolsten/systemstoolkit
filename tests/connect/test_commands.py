import pytest
import datetime
import mock
import systemstoolkit.connect.commands as commands
from systemstoolkit.connect import Connect
from systemstoolkit.connect.objects import Satellite


def test_set_state_cartesian_1():
    exp = 'SetState */Satellite/ERS1 Cartesian J4Perturbation "01 Nov 2000 00:00:00.000" "01 Nov 2000 08:00:00.000" 60 J2000 "01 Nov 2000 00:00:00.000" -5465000.513055 4630000.194365 0.0 712.713627 841.292034 7377.687805'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        c = Connect()
        c.connect()
        got = commands.set_state_cartesian(
            Satellite(c, '*/Satellite/ERS1'),
            epoch=datetime.datetime(2000, 11, 1),
            state=(
                '-5465000.513055', '4630000.194365', '0.0',
                '712.713627', '841.292034', '7377.687805'
            ),
            interval=(datetime.datetime(2000,11,1), datetime.datetime(2000,11,1,8)),
            stepsize='60',
            prop='J4Perturbation',
            coord='J2000',
        )

        got = c._socket.sendall.call_args[0][0].decode().strip()
        assert got == exp

