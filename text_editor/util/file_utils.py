import os


class FileUtils:

    @staticmethod
    def get_app_root_path():
        parts = os.path.realpath(__file__).split("/")[:-4]
        return "/".join(parts)
