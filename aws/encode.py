import binascii

import base64

thumbprint_hex = 'E916D1BD3434F984326365431C822DE64AD66AAA'

thumbprint_binary = binascii.unhexlify(thumbprint_hex)

x5t_compliant = base64.b64encode(thumbprint_binary).decode('utf-8')

print(x5t_compliant)