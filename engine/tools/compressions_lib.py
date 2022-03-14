import gzip
import lzma
import brotli
import deflate



def brotli_compress(data, temp_fileIO, level=7):
    """
    note:

    :temp_fileIO is an empty temporary file handler and must be in wb mode 
    """
    temp_fileIO.write(brotli.compress(quality=level))
    temp_fileIO.close()


def gzip_compress(data, temp_fileIO, level=5):
    temp_fileIO.write(gzip.compress(data, compresslevel=level))
    temp_fileIO.close()


def lzma_compress(data, temp_fileIO, level=5):
    temp_fileIO.write(lzma.compress(data, preset=level))
    temp_fileIO.close()


def deflate_compress(data, temp_fileIO, level=1):
    temp_fileIO.write(deflate.gzip_compress(data, compresslevel=level))