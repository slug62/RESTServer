
def read_line(rw):
    """
    Reads and returns one line from rw

    Line endings could be \n or \r\n

    :param rw:  reader_writer
    :return:
    """
    the_line = ""
    ch = rw.read()
    while ch != '\r' and ch != '\n':
        the_line += ch
        ch = rw.read()
    ch = rw.read() # is this /n?
    if ch != '\n' and ch != '\r':
        rw.unread(ch)
    return the_line

def send_binary_response(rw, data, content_type='text/plain', status =200, status_remark='OK'):
    """

    :param rw:     A reader_writer to use to send the response
    :param message:
    :param content_type:
    :param status:
    :param status_remark:
    :return:
    """
    #  first line
    #  content-type
    # content-length  (bytes)
    # blank line
    # content
    rw.write("HTTP/1.1 {} {}\r\n".format(status, status_remark))
    rw.write("Content-type: {}\r\n".format(content_type))
    rw.write("Content-length: {}\r\n".format(len(data)))
    rw.write("\r\n")
    rw.socket.sendall(data)
