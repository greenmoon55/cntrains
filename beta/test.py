import codecs;
import pickle;

out = codecs.open("out.txt", "w", "utf-8")
with open('trainsbak.txt', 'r') as f:
    d = pickle.load(f)
    for key in sorted(d):
        train = d[key]
        out.write( "%s %10s %10s\n" % (train.no, train.from_station, train.to_station))
