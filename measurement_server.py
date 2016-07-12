from socket import socket
import json
import re
from db_util import db

import logging

__author__ = 'peter'


def server_port():
    return 12345


encoding = 'UTF-8'


if __name__ == "__main__":

    logging.basicConfig(filename='example.log', level=logging.INFO)

    # setting up a listener socket
    sock = socket()
    sock.bind(('', server_port()))
    sock.listen(0)  # 0 backlog of connections
    ACCEPTABLE_REQUEST_TYPES = ["/area",
                                "/area/(\d+)/location",
                                "/location/(\d+)/measurement",
                                "/area/(\d+)/category",
                                "/area/(\d+)/average_measurement",
                                "/area/(\d+)/number_locations"]

    while True:
        (conn, address) = sock.accept()
        logging.info("connection made {}".format(conn))
        logging.info(str(address))

        # get data from client (request)
        data_string = ""
        bytes = conn.recv(2048)
        while len(bytes) > 0:
            # we actually got data from the client
            bytes_str = bytes.decode(encoding)
            logging.info("data received: |{}|".format(bytes_str))
            data_string += bytes_str
            bytes = conn.recv(2048)

        logging.info("all data received: " + data_string)
        response = 'response was not properly set'


        if data_string not in ACCEPTABLE_REQUEST_TYPES:
            logging.error('Invalid request syntax |{}|'.format(data_string))
            response = {'e': 'Invalid Request, to appropriate reqeusts are {}'.format(ACCEPTABLE_REQUEST_TYPES)}
        else:
            if data_string == ACCEPTABLE_REQUEST_TYPES[0]:
                try:
                    response = json.dumps(db.do_command('Select * from area'))
                except:
                    response = {'e': "There was an error proccessing your 'area' request"}

        conn.sendall(response.encode(encoding))
        conn.shutdown(1)  ## shutdown the sending side
        conn.close()
        logging.info("connection closed")
