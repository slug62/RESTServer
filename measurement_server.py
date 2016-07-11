from socket import socket
import json

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
    ACCEPTABLE_REQUEST_TYPES = ["E", "S"]

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

        values = data_string.split(' ')
        logging.info("values: {}".format(values))
        logging.info("Peter test: {}, number of values: {}".format(values[0][0], len(values)))
        if len(values) <= 1 or values[0][0] not in ACCEPTABLE_REQUEST_TYPES:
            logging.error("Invalid request syntax |{}|".format(data_string))
            response = 'XInvalid request syntax, Your request either did not start with an E or S,' \
                       ' or you had too few arguments'
        else:
            if values[0][0] == ACCEPTABLE_REQUEST_TYPES[0]:
                try:
                    x = float(values[0][1:])
                    poly = [float(x) for x in values[1:]]
                    result = polynomials.evaluate(x, poly)
                    logging.info("Evaluating {} for {}".format(x, poly))
                    print("Result: ", result)
                    response = "E" + str(result)
                except:
                    response = 'Xinvalid numeric format'
            elif values[0][0] == ACCEPTABLE_REQUEST_TYPES[1]:
                try:
                    a = float(values[0][1:])
                    b = float(values[1])
                    poly = [float(x) for x in values[2:len(values) - 1]]
                    tolerance = float(values[len(values) - 1])
                    logging.info("Bisection with a:{}, b{}, poly{}, tolerance{}".format(a, b, poly, tolerance))
                    result = polynomials.bisection(a, b, poly, tolerance)
                    response = "S" + str(result)
                except:
                    response = 'Xinvalid numeric format'

        conn.sendall(response.encode(encoding))
        conn.shutdown(1)  ## shutdown the sending side
        conn.close()
        logging.info("connection closed")
