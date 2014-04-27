def replacetwoLSB(n,lsb2,lsb):
	n = (n & ~(1 << 1)) | (lsb2 << 1)
	n = (n & ~1) | lsb
	return n

def get_quantizaton_coefficients(quant_block):
	quant_block = round(quant_block)

	coefficients = []
	coefficients.append(quant_block[0,0])
	coefficients.append(quant_block[0,1])
	coefficients.append(quant_block[1,0])
	coefficients.append(quant_block[2,0])
	coefficients.append(quant_block[1,1])
	coefficients.append(quant_block[0,2])

	return coefficients