__author__ = 'Ben Setzer'

import re

"""
    This provides reading and writing of characters for sockets.
    This is already provided by the Python library, but it looked interesting
        to try working it out directly.
"""


class reader_writer:
    """
    Provides reading and writing character services.
    Coding and decoding is handled.
    Data is transmitted in packets so there should be no decoding anomalies.
    """

    char_chunk_size = 128
    byte_buffer_size = 16*char_chunk_size

    def __init__(self, socket, encoding='utf-8'):
        self.socket = socket
        self.in_char_buffer = ""
        #self.out_char_buffer = ""
        self.stream_done = False
        self.encoding = encoding

    def read(self):
        """
        read one character and return
        return "" if the stream is done
        :return: the character read
        """
        if len(self.in_char_buffer) == 0:
            self.fill_char_buffer()
            if self.stream_done:
                return ""
        if len(self.in_char_buffer) > 0:
            rtval = self.in_char_buffer[0]
            self.in_char_buffer = self.in_char_buffer[1:]
            return rtval
        else:
            return ""

    def unread(self, ch):
        self.in_char_buffer = ch + self.in_char_buffer

    def fill_char_buffer(self):
        """
        Get some more bytes for the data buffer
        """
        data_bytes = self.socket.recv(reader_writer.byte_buffer_size)
        #print("Server received data bytes %d" % len(data_bytes))
        if len(data_bytes) > 0:
            self.in_char_buffer += data_bytes.decode(self.encoding)
        else:
            self.stream_done = True

    def write(self, data):
        """
        write a string to the socket.
        """
        self.socket.sendall(data.encode(self.encoding))

        # i = 0
        # while i < len(data):
        #     data_bytes = data[i:i+reader_writer.char_chunk_size].encode(self.encoding
        #     self.socket.send(data_bytes)
        #     i += reader_writer.char_chunk_size
        #     #print("\n\nblock sent\n\n")

    def next_word(self):
        """
            Get the next word from the input stream of the socket.
            :return: the next word, empty if the input is exhausted
        """
        c = self.read()
        while re.match(r'\s', c):
            c = self.read()
        if len(c) > 0:
            word = c
            c = self.read()
            while re.match(r'\S', c):
                word += c
                c = self.read()
            return word
        else:
            return ''

    def close_read(self):
        self.socket.shutdown(0)

    def close_write(self):
        self.socket.shutdown(1)

    def encoded_length(self, message):
        return len(message.encode(self.encoding))

