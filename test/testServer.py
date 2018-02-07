from unittest import TestCase
from unittest.mock import MagicMock, call

from brickpi_remote_control.server.main_upd_server import listen_for_data
from brickpi_remote_control.utils import MoveCmd, END_FLAG


class StopException(Exception):
    pass


class ListenServer(TestCase):
    def setUp(self):
        self.mock_server = MagicMock()
        self.mock_cmd = MagicMock(spec=MoveCmd)

    def test_listen_for_data1(self):
        # set up the mock
        self.mock_server.recv.side_effect = [[1, END_FLAG, 2, 3, END_FLAG, 4], StopException()]

        # call test method
        self.assertRaises(StopException, listen_for_data, self.mock_server, self.mock_cmd)

        # test that it read the cmd
        self.mock_cmd.write.assert_called_with(2, 3)

    def test_listen_for_data1a(self):
        # set up the mock
        self.mock_server.recv.side_effect = [[1, END_FLAG], StopException()]

        # call test method
        self.assertRaises(StopException, listen_for_data, self.mock_server, self.mock_cmd)

        # test that it not read the cmd
        self.mock_cmd.write.assert_not_called()

    def test_listen_for_data2(self):
        # set up the mock
        self.mock_server.recv.side_effect = [[0, 1, END_FLAG, 2, 3, END_FLAG, 4], [5, END_FLAG], StopException()]

        # call test method
        self.assertRaises(StopException, listen_for_data, self.mock_server, self.mock_cmd)

        # test that it read the cmd
        self.mock_cmd.write.assert_has_calls([call(2, 3), call(4, 5)])

    def test_listen_for_data3(self):
        # set up the mock
        self.mock_server.recv.side_effect = [[END_FLAG, 2, 3, END_FLAG, 4], [5, END_FLAG, 6, 7, 8, END_FLAG], StopException()]

        # call test method
        self.assertRaises(StopException, listen_for_data, self.mock_server, self.mock_cmd)

        # test that it read the cmd
        self.mock_cmd.write.assert_has_calls([call(2, 3), call(4, 5)])

    def test_listen_for_data4(self):
        # set up the mock
        self.mock_server.recv.side_effect = [[3, END_FLAG, 4], [5, END_FLAG, 6, END_FLAG], StopException()]

        # call test method
        self.assertRaises(StopException, listen_for_data, self.mock_server, self.mock_cmd)

        # test that it read the cmd
        self.mock_cmd.write.assert_has_calls([call(4, 5)])
