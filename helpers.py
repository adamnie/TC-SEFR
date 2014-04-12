def replacetwoLSB(n,lsb2,lsb):
	n = (n & ~(1 << 1)) | (lsb2 << 1)
	n = (n & ~1) | lsb
	return n
