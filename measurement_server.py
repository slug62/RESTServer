from socket import socket
import json
from db_util import db
import re
from sock_util.reader_writer import reader_writer
from sock_util.socket_util import *
import logging

__author__ = 'peter'

def server_port():
    return 12345

if __name__ == "__main__":

    logging.basicConfig(filename='example.log', level=logging.INFO)

    # setting up a listener socket
    sock = socket()
    sock.bind(('', server_port()))
    sock.listen(0)  # 0 backlog of connections
    ACCEPTABLE_REQUEST_TYPES = [re.compile('/area'),
                                re.compile('/area/(\d+)/location'),
                                re.compile('/area/(\d+)/category'),
                                re.compile('/area/(\d+)/average_measurement'),
                                re.compile('/area/(\d+)/number_locations'),
                                re.compile('/location/(\d+)/measurement')]

    while True:
        (conn, address) = sock.accept()
        rw = reader_writer(conn)
        logging.info('Connection made: {}'.format(conn))
        first_line = read_line(rw)
        logging.info('Client request: {}'.format(first_line))
        response = ''

        if any(re.search(regex, first_line) for regex in ACCEPTABLE_REQUEST_TYPES):
            if re.search(ACCEPTABLE_REQUEST_TYPES[5], first_line):
                ml_id = re.split('/', first_line)
                response = db.do_command('SELECT * FROM measurement WHERE measurement_location=?', [ml_id[2]])
            elif re.search(ACCEPTABLE_REQUEST_TYPES[4], first_line):
                la_id = re.split('/', first_line)
                response = db.do_command('SELECT COUNT(*) AS Number_of_Locations FROM location WHERE location_area=?', [la_id[2]])
            elif re.search(ACCEPTABLE_REQUEST_TYPES[3], first_line):
                am_id = re.split('/', first_line)
                response = db.do_command('SELECT AVG(value) AS Average_Measurement FROM measurement WHERE measurement_location=?', [am_id[2]])
            elif re.search(ACCEPTABLE_REQUEST_TYPES[2], first_line):
                cat_id = re.split('/', first_line)
                response = db.do_command('SELECT name from category NATURAL JOIN category_area WHERE area_id=?', [cat_id[2]])
            elif re.search(ACCEPTABLE_REQUEST_TYPES[1], first_line):
                loc_id = re.split('/', first_line)
                response = db.do_command('SELECT name, altitude FROM location WHERE location_area=?', [loc_id[2]])
            elif re.search(ACCEPTABLE_REQUEST_TYPES[0], first_line):
                response = db.do_command('SELECT * FROM area')
            logging.info('Server response: {}'.format(response))
            send_binary_response(rw, json.dumps(response).encode())
        else:
            logging.info('Bad request: {}: sending failed response'.format(first_line))
            send_binary_response(rw, "You have requested an unsupported request".encode(), status=400, status_remark='Bad Request')

        conn.shutdown(1)  ## shutdown the sending side
        conn.close()
        logging.info("Closed connection")
