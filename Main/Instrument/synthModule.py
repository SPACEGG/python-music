from typing import AbstractSet


from abc import *

class SynthModule(metaclass = ABCMeta):
    
    @abstractmethod
    def output(self, *args):
        pass