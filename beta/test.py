import pickle;

with open('trains.txt', 'r') as f:
    d = pickle.load(f)
    for key in sorted(d):
        train = d[key]
        print "%s %10s %10s" % (train.no, train.from_station, train.to_station)
