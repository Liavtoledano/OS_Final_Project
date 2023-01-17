def bytes2int(str):
 return int(str.encode('hex'), 16)

def bytes2hex(str):
 return '0x'+str.encode('hex')

def int2bytes(i):
 h = int2hex(i)
 return hex2bytes(h)

def int2hex(i):
 return hex(i)

def hex2int(h):
 if len(h) > 1 and h[0:2] == '0x':
  h = h[2:]

 if len(h) % 2:
  h = "0" + h

 return int(h, 16)

def hex2bytes(h):
 if len(h) > 1 and h[0:2] == '0x':
  h = h[2:]

 if len(h) % 2:
  h = "0" + h

 return h.decode('hex')