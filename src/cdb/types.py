import copy
import yaml

class Dictionary(dict):

    def __init__(self):
        super(Dictionary, self).__init__()

    def __hash__(self):
        hashcode: int = 1
        for e in self:
            hashcode = 31 * hashcode + (0 if e is None else hash(e))
        return hashcode

    def __deepcopy__(self, memodict={}):
        out = Dictionary()
        for k, v in self.items():
            out[copy.deepcopy(k, memodict)] = copy.deepcopy(v, memodict)
        return out

    def load_file(self, filename: str):
        with open(filename) as file:
            self.load(file)

    def load(self, bytes: bytes):
        loaded = yaml.safe_load(bytes)
        self.update(loaded)
