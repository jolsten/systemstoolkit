import pytest
import datetime
import mock
from systemstoolkit.connect import Connect
from systemstoolkit.connect.objects import Satellite


def test_set_state_cartesian():
    exp = 'SetState */Satellite/ERS1 Cartesian J4Perturbation "01 Nov 2000 00:00:00.000" "01 Nov 2000 08:00:00.000" 60 J2000 "01 Nov 2000 00:00:00.000" -5465000.513055 4630000.194365 0.0 712.713627 841.292034 7377.687805'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Satellite(c, '*/Satellite/ERS1')
            sat_obj.set_state_cartesian(
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


def test_set_state_classical():
    exp = 'SetState */Satellite/ERS1 Classical LOP UseScenarioInterval 86400 J2000 "01 Oct 1999 00:00:00.000" 42164000.0 0.0 0.0 0.0 269.3 0.0'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Satellite(c, '*/Satellite/ERS1')
            sat_obj.set_state_classical(
                epoch=datetime.datetime(1999, 10, 1),
                state=(
                    '42164000.0', '0.0', '0.0',
                    '0.0', '269.3', '0.0'
                ),
                stepsize='86400',
                prop='LOP',
                coord='J2000',
            )

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_set_state_equi():
    exp = 'SetState */Satellite/ERS1 Equi J4Perturbation "01 Nov 2000 00:00:00.000" "01 Nov 2000 08:00:00.000" 60 MeanOfDate "01 Nov 2000 00:00:00.000" 7163000.137079 0.0 0.0 0.55697636 -0.65743965 220.270122 Retrograde'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Satellite(c, '*/Satellite/ERS1')
            sat_obj.set_state_equi(
                epoch=datetime.datetime(2000, 11, 1),
                state=(
                    '7163000.137079', '0.0', '0.0', 
                    '0.55697636', '-0.65743965', '220.270122',
                ),
                direction='Retrograde',
                interval=(datetime.datetime(2000,11,1), datetime.datetime(2000,11,1,8)),
                stepsize='60',
                prop='J4Perturbation',
                coord='MeanOfDate',
            )

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_set_state_from_file_1():
    exp = r'SetState */Satellite/Shuttle FromFile "C:\stk\User\Data\EphemFile.e"'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Satellite(c, '*/Satellite/Shuttle')
            sat_obj.set_state_from_file(
                filepath=r'C:\stk\User\Data\EphemFile.e',
            )

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp


def test_set_state_from_file_2():
    exp = r'SetState */Satellite/Shuttle FromFile "C:\stk\User\Data\EphemFile.e" StartTime "01 Jun 2003 14:00:00.000"'
    with mock.patch('socket.socket') as mock_sock:
        mock_sock.return_value.recv.return_value = b'ACK'

        with Connect() as c:
            print(c)
            sat_obj = Satellite(c, '*/Satellite/Shuttle')
            sat_obj.set_state_from_file(
                filepath=r'C:\stk\User\Data\EphemFile.e',
                epoch=datetime.datetime(2003, 6, 1, 14),
            )

            got = c._socket.sendall.call_args[0][0].decode().strip()
            assert got == exp
