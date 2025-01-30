import logging
import logging.handlers

# Create a logger
logger = logging.getLogger('TCPLogger')
logger.setLevel(logging.DEBUG)  # Adjust log level as needed

# Define the remote IP and port to send logs to
remote_ip = '10.10.10.42'  # Replace with the actual IP address
remote_port = 514  # Replace with the desired port number

# Create a TCP SocketHandler to send logs to the remote server
socket_handler = logging.handlers.SocketHandler(remote_ip, remote_port)

# Set a log formatter (optional)
formatter = logging.Formatter('%(message)s')
socket_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(socket_handler)

# Example log messages
logger.debug('Debug message')
logger.info('Information message')
logger.warning('Warning message')
logger.error('Error message')
