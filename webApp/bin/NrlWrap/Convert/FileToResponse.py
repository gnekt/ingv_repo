from obspy.io.xseed.scripts import dataless2resp
from obspy.io.xseed import Parser


class Converter:
    def __init__(self, file_src=None, folder_dst=None):
        if not file_src is None or not folder_dst is None:
            self.parser_object = Parser(file_src)
            self.folder_destination = folder_dst
        else:
            raise NotImplementedError("path file or folder destination must be valid ")

    def parse(self):
        raise NotImplementedError


class DatalessToResp(Converter):
    def __init__(self, file_src=None, folder_dst=None):
        super(DatalessToResp, self).__init__(file_src=file_src, folder_dst=folder_dst)

    def parse(self):
        self.parser_object.write_resp(folder=self.folder_destination, zipped=False)


class DatalessToXSeed(Converter):
    def __init__(self, file_src=None, folder_dst=None):
        super(DatalessToXSeed, self).__init__(file_src=file_src, folder_dst=folder_dst)

    def parse(self):
        self.parser_object.write_xseed(filename="converted.xml")

class DatalessToSeed(Converter):
    def __init__(self, file_src=None, folder_dst=None):
        super(DatalessToXSeed, self).__init__(file_src=file_src, folder_dst=folder_dst)

    def parse(self):
        self.parser_object.write_seed(filename="converted.xml")

