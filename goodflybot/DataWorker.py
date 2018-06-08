import logging
import pickle
from abc import ABCMeta
import os.path as Path


class FSWorker(metaclass=ABCMeta):

    @classmethod
    def log(cls, *args):
        log_path = Path.join(Path.dirname(__file__), 'debug.log')
        formatt = '[%(levelname)s] %(asctime).19s [%(filename)s_Line:%(lineno)d] %(message)s'

        logging.basicConfig(
            level=logging.DEBUG,
            format=formatt,
            filename=log_path,
            filemode='w'
        )

        logger = logging.getLogger()

        logger.debug(args)

    @classmethod
    def get_static(cls):
        path = Path.join(Path.dirname(__file__), 'common/conf.pickle')
        if not Path.exists(path):
            cls.log("path '{}' doesn't exist".format(path))
            return
        with open(path, 'rb') as f:
            tree = pickle.load(f)
            return tree
