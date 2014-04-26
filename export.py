

def export_to_csv(stars):
    raise NotImplementedError()

def export_to_pickle(stars, filename):
    import pickle
    output = open(filename, "wb")
    pickle.dump(stars, output, -1)
    output.close()