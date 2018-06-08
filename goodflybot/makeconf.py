import pickle


with open("conf.pickle", 'rb') as f:
    print(pickle.load(f))