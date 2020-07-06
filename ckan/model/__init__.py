# We only need to return the type of a dataset
# if one already exists. For our purposes we can
# assume that none already exist, hence just return None.
class Package:
    @staticmethod
    def get(name):
        return None
