class LFRHelper:

    @staticmethod
    def extract_key(key):
        if len(key) is 2:
            size, mix = key
            overlap = ''
            return size, mix, overlap

        size, mix, overlap = key
        return size, mix, overlap
