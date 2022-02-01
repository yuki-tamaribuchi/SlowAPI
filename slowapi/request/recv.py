def recv_request(client_sock):
	return client_sock.recv(4096)



"""
受信するデータ量を拡張するため、複数回recvを呼び出そうとしたが、受信データが終わった時点で、ソケットがハングする。
setblockingをFalseに設定やタイムアウトの設定をしたがBlockingIOError: [Errno 11] Resource temporarily unavailableがでる。
現状では4096bytes以下ということで開発を行う。
"""

#import errno
#
#def recv_all(client_sock):
#	#client_sock.setblocking(False)
#
#	try:
#		chunk = client_sock.recv(16)
#		return chunk
#	except IOError as e:
#		if e.errno == errno.EWOULDBLOCK:
#			print('err called')
#			recv_all(client_sock)
#
#def recv_request(client_sock):
#	#client_sock.setblocking(False)
#	request = b''
#
#	while True:
#		chunk = recv_all(client_sock)
#		if not chunk: break
#		request+=chunk
#	print(request)
#	return request