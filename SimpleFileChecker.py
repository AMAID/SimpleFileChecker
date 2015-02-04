# encoding:utf-8
import struct


class FileType:
    def __init__(self,types=None):
        self.types = types

    def _bytes2hex(self,bytes):
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()

    def _filetype(self,myfile):
        tl = self.types
        ftype = 'unknown'
        for hcode in tl.keys():
            numOfBytes = len(hcode) / 2
            myfile.seek(0)
            hbytes = struct.unpack_from("B"*numOfBytes, myfile.read(numOfBytes)) # 一个 "B"表示一个字节
            f_hcode = self._bytes2hex(hbytes)
            if f_hcode == hcode:
                ftype = tl[hcode]
                break
        return ftype
    def _checkfile(self,file):
        ftype = self._filetype(file)
        if ftype != "unknown":
            return True
        else:
            return False

    def isImage(self, file):
        self.types = {"FFD8FF": "JPEG", "89504E47": "PNG", "47494638": "GIF"}
        return self._checkfile(file)

    def isExcel(self, file):
        self.types = {"D0CF11E0": "XLS"}
        return self._checkfile(file)

    def isCustomType(self, file, types):
        self.types = types
        return self._checkfile(file)

if __name__ == '__main__':
    checkfile = FileType()
    myfile = open("c://foo.jpg", 'rb')
    print(checkfile.isImage(myfile))
    print(checkfile.isExcel(myfile))
    print(checkfile.isCustomType(myfile,{"FFD8FF": "JPEG","D0CF11E0": "XLS"}))
    myfile.close()