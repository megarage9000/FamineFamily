CONNECTION_REQ = b'0001'  # <ASK SERVER TO CONNECT> <USERNAME>
CONNECTION_ACK = b'0011'  # <SERVER CONNECTED>
USER_COUNT = b'0010'  # <NUMBER OF USERS IN THE ROOM>
START = b'1111'
END = b'0000'

SPAWN_CHIP = b'1000'
CHIP_STATE_UPDATE = b'1100' # client --> server when state changes
CHIP_POS_UPDATE = b'1110' # client --> server when they move chips 
