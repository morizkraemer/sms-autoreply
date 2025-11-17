import serial
from modem.modem_helpers import readlines_helper, ConnectionError, parse_all_sms
import logging

class Modem:
    def __init__(self):
        self.m = self.create_connection()
        pass

    def readlines(self):
        if (not self.m):
            return
        else:
            return readlines_helper(self.m)

    def write_at(self, command):
        if (not self.m):
            return

        self.m.reset_input_buffer()
        self.m.reset_output_buffer()

        self.m.write(bytes(f'{command}\r\n'.encode('utf-8')))

        self.m.flush()

        return self.readlines()

    def create_connection(self):
        logging.info("Connecting to modem")
        try:
            ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=2)

            ser.write(b'ATE0\r\n')
            response = readlines_helper(ser)
            if (b'ERROR' in response):
                ser.close()
                raise ConnectionError("Connection failed")
            logging.info("Set no command echoing")

            ser.write(b'AT+CMEE=?\r\n')
            response = readlines_helper(ser)
            if (b'ERROR' in response):
                ser.close()
                raise ConnectionError("Connection failed")
            logging.info("Set verbose errors")

            ser.write(b'AT+CMGF=1')
            response = readlines_helper(ser)
            if (b'ERROR' in response):
                ser.close()
                raise ConnectionError("Connection failed")
            logging.info('Set sms mode')

            ser.write(b'AT\r\n')
            response = readlines_helper(ser)
            if (b'ERROR' in response):
                ser.close()
                raise ConnectionError("Connection failed")

            logging.info("Connected")
            return ser

        except Exception as e:
            logging.info(e)

    def test_connection(self):
        if (not self.m):
            return
        self.write_at('AT')

    def send_sms(self, number, message):
        if (not self.m):
            return
        response = self.write_at(f'AT+CMGS="{number}"')
        if not response or b'> ' not in response:
            logging.info("Message prompt failed", response)
            return
        response = self.write_at(f'{message} \x1a')
        if not response or any(b'ERROR' in item for item in response) or not b'OK\r\n' in response:
            logging.info("Message not sent, error")
            return False
        else:
            logging.info(f'Message sent to {number}!')
            return True

    def get_unread_sms(self):
        if (not self.m):
            return
        response = self.write_at(f'AT+CMGL="REC UNREAD"')
        return parse_all_sms(response)

    def get_all_sms(self):
        if not self.m:
            return
        response = self.write_at(f'AT+CMGL="ALL"')
        return parse_all_sms(response)

    def delete_sms(self, index):
        if not self.m:
            return
        response = self.write_at(f'AT+CMGD={index}')
        if not response or not b'OK\r\n' in response:
            logging.info("Delete message failed")
            return False
        return True

