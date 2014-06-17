# fixing path
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import unittest
import numpy as np
import lib.embed
import lib.helpers
import hashlib

class embedTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
      super(embedTests, self).__init__(*args, **kwargs)

    def test_checksum_zero_float(self):
      block = np.zeros((4,4))
      test_hash = hashlib.md5()
      test_hash.update("0"*12)
      expected_output = test_hash.hexdigest()[:4]
      test_checksum = lib.embed.checksum(block,4)

      self.assertEqual(test_checksum,expected_output)

    def test_checksum_integers(self):
      block = np.arange(16).reshape((4,4))
      test_hash = hashlib.md5()
      test_hash.update("01234567891011")
      expected_output = test_hash.hexdigest()[:4]
      test_checksum = lib.embed.checksum(block,4)

      self.assertEqual(test_checksum,expected_output)

    def test_errors_occured_True(self):
      block = np.arange(64).reshape((8,8))
      checksum = 0
      self.assertEqual(lib.embed.errors_occured(block,checksum),True)

    def test_errors_occured_False(self):
      block = np.arange(64).reshape((8,8))
      checksum = int(lib.embed.checksum(block),16)

      self.assertEqual(lib.embed.errors_occured(block,checksum),False)

    def test_errors_occured_binary(self):
      block = np.arange(64).reshape((8,8))
      check = int(lib.embed.checksum(block),16)
      checksum = "{0:b}".format(check) 

      self.assertEqual(lib.embed.errors_occured(block,checksum),False)

    def test_errors_occured_hex(self):
      block = np.arange(64).reshape((8,8))
      checksum = lib.embed.checksum(block)

      self.assertEqual(lib.embed.errors_occured(block,checksum),False)  

    def test_to_bin_str_length(self):
        A_blocks  = {'x': 10, 'y': 10, 't': 3, 's': lib.helpers.normalize(180,128),'o':lib.helpers.normalize(256,256)}
        B_blocks = np.arange(6)
        C_blocks = np.arange(6)+7

        bin_data = lib.embed.to_bin_str(A_blocks,B_blocks,C_blocks)

        self.assertEqual(len(bin_data),112)
    def test_to_bin_str_zeros(self):
        A_blocks  = {'x': 0, 'y': 0, 't': 0, 's': 0,'o': 0}
        B_blocks = 0*np.arange(6)
        C_blocks = 0*np.arange(6)

        bin_data = lib.embed.to_bin_str(A_blocks,B_blocks,C_blocks)

        self.assertEqual(bin_data,112*"0")

    def test_to_bin_str_negative(self):
        A_blocks  = {'x': 0, 'y': 0, 't': 0, 's': lib.helpers.normalize(-1,128),'o': lib.helpers.normalize(-5,256)}
        B_blocks = 0*np.arange(6)
        C_blocks = 0*np.arange(6)

        bin_data = lib.embed.to_bin_str(A_blocks,B_blocks,C_blocks)
        self.assertEqual(bin_data,17*"0"+"0111111"+"01111011"+80*"0")

    def test_to_bin_str_wrong_type(self):
        A_blocks  = {'x': 0, 'y': 0, 't': 0, 's': lib.helpers.normalize(-1,128),'o': lib.helpers.normalize(-5,256)}
        B_blocks = 1.0*np.arange(6)
        C_blocks = 0*np.arange(6)
        bin_data = lib.embed.to_bin_str(A_blocks,B_blocks,C_blocks)

        self.assertEqual(bin_data,-1)

    def test_to_data_types(self):
        A_blocks  = {'x': 10, 'y': 10, 't': 3, 's':  lib.helpers.normalize(180,128),'o': lib.helpers.normalize(256,256)}
        B_blocks = np.arange(6)
        C_blocks = np.arange(6)+7
        sym_checksum = 16*'0'

        binary = lib.embed.to_bin_str(A_blocks,B_blocks,C_blocks)
        binary += sym_checksum
        retrived_data = lib.embed.to_data(binary)

        self.assertIsInstance(retrived_data[0],dict)
        for coef in retrived_data[1]:
            self.assertIsInstance(coef,int)
        for coef in retrived_data[2]:
            self.assertIsInstance(coef,int)
        self.assertIsInstance(retrived_data[3],int)

    def test_to_data_range(self):
        A_blocks  = {'x': 10, 'y': 10, 't': 3, 's': lib.helpers.normalize(300,128),'o': lib.helpers.normalize(-300,256)}
        B_blocks = np.arange(6)
        C_blocks = np.arange(6)+7
        sym_checksum = 16*'0'

        binary = lib.embed.to_bin_str(A_blocks,B_blocks,C_blocks)
        binary += sym_checksum
        retrived_data = lib.embed.to_data(binary)

        self.assertLessEqual(retrived_data[0]['s'], 64)
        self.assertGreaterEqual(retrived_data[0]['s'], -64)
        self.assertLessEqual(retrived_data[0]['o'], 128)
        self.assertGreaterEqual(retrived_data[0]['o'], -128)

    def test_to_data_elem_num(self):
        pass

    def test_embed_watermark_return_type(self):
        wm_block = lib.embed.embed_watermark(np.zeros((8,8)),
            {'x': 10, 'y': 10, 't': 3, 's': 300,'o':lib.embed.normalize(-300,256)},
            [1]*40,[1]*40)
        self.assertIsInstance(wm_block,np.ndarray)

    def test_embed_watermark_changes_block(self):
        with self.assertRaises(AssertionError):
            wm_block = lib.embed.embed_watermark(np.zeros((8,8)),
                {'x': 10, 'y': 10, 't': 3, 's': 300,'o':-300},
                [1]*40,[1]*40)

            np.testing.assert_equal(wm_block,np.zeros((8,8)))

    def test_embed_watermark_embeds_correct(self):
        wm_block = lib.embed.embed_watermark(np.zeros((8,8)),
            {'x': 10, 'y': 10, 't': 3, 's': lib.helpers.normalize(300,128),'o':lib.helpers.normalize(-300,256)},
            [1]*40,[1]*40)
        data = lib.embed.to_bin_str({'x': 10, 'y': 10, 't': 3, 
            's': lib.helpers.normalize(300,128),
            'o': lib.helpers.normalize(-300,256)},
            [1]*40,[1]*40)
        ret = ''
        for i in range(7):
            for j in range(8):
                ret += "{0:02b}".format(int(wm_block[i,j]))

        self.assertEqual(ret,data)

    def test_retrieve_watermark_and_checksum_return_type(self):
        wm_block = lib.embed.embed_watermark(np.zeros((8,8)),
            {'x': 10, 'y': 10, 't': 0, 's': 300,'o':-300},
            [1]*40,[1]*40)

        retrived_data = lib.embed.retrieve_watermark_and_checksum(wm_block)
        self.assertIsInstance(retrived_data[0],dict)
        for coef in retrived_data[1]:
            self.assertIsInstance(coef,int)
        for coef in retrived_data[2]:
            self.assertIsInstance(coef,int)
        self.assertIsInstance(retrived_data[3],int)

    def test_retrive_watermark_and_checksum_returns_correct(self):
        bin_string = 17 *"0" + "1000000" + "10000000" + 96*"0" #62 -> 0 , 126 -> 0 
        data = lib.embed.to_data(bin_string)

        self.assertEqual(data[0],{'x': 0, 'y': 0, 't': 0, 
             's':0 ,
             'o':0 })

    def test_retrieve_watermark_and_checksum_data_correct_zeros(self):
        wm_block = lib.embed.embed_watermark(np.zeros((8,8)),
            {'x': 10, 'y': 10, 't': 0, 's': lib.helpers.normalize(10,128),
             'o': lib.helpers.normalize(10,256)},[1,2,3,4,5,6],[1,2,3,4,5,6])

        wm_block = lib.embed.embed_checksum(wm_block)
        checksum = lib.embed.checksum(wm_block)

        self.assertIsInstance(wm_block,np.ndarray)

        retrived_data = lib.embed.retrieve_watermark_and_checksum(wm_block)

        self.assertEqual(retrived_data[0], {'x': 10, 'y': 10, 't': 0, 
            's':10 ,
            'o':10 ,
            })
        self.assertEqual(retrived_data[1],[1,2,3,4,5,6])
        self.assertEqual(retrived_data[2],[1,2,3,4,5,6])
        self.assertEqual(retrived_data[3],int(checksum,16))

    def test_retrieve_watermark_and_checksum_data_correct_non_zeros(self):
        wm_block = lib.embed.embed_watermark(np.zeros((8,8))+5,
            {'x': 10, 'y': 10, 't': 0, 's': lib.helpers.normalize(10,128),
             'o': lib.helpers.normalize(10,256)},[1,2,3,4,5,6],[1,2,3,4,5,6])

        wm_block = lib.embed.embed_checksum(wm_block)
        checksum = lib.embed.checksum(wm_block)

        self.assertIsInstance(wm_block,np.ndarray)

        retrived_data = lib.embed.retrieve_watermark_and_checksum(wm_block)

        self.assertEqual(retrived_data[0], {'x': 10, 'y': 10, 't': 0, 
            's':10 ,
            'o':10 ,
            })
        self.assertEqual(retrived_data[1],[1,2,3,4,5,6])
        self.assertEqual(retrived_data[2],[1,2,3,4,5,6])
        self.assertEqual(retrived_data[3],int(checksum,16))

def main():
    unittest.main()

if __name__ == '__main__':
    main()