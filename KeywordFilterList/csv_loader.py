import csv

from StringIO import StringIO

class CSVRows(list):
    def to_csv(self):
        output = StringIO()
        try:
            fieldnames = self[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in self:
                writer.writerow(row)
            output.flush()
        except:
            pass
        return output.getvalue()


class CSVFilter():
    def __init__(self, filename):
        self.csv_data = []
        with open(filename, 'rU') as csvfile:
            try:
                self.reader = csv.DictReader(csvfile)
                for row in self.reader:
                    self.csv_data.append(row)
            except Exception, ex:
                print ex
            
    def __len__(self):
        return len(self.csv_data)
    
    def get(self, **kwargs):
        self.matches = CSVRows()
        for row in self.csv_data:
            values = [(k, row.get(k, None)) for k in kwargs.keys()]
            if (all([(v[-1] != None) and ( (v[-1] == kwargs.get(v[0], None)) or (v[-1] in kwargs.get(v[0], None)) ) for v in values])):
                self.matches.append(row)
        return self.matches
    

class KeywordFilterList():
    def __init__(self, filename=None):
        self.filename = filename
    
    @classmethod
    def load_csv(self, filename=None):
        if (filename):
            self.filename = filename
        else:
            filename = self.filename
        self.csv_filter = CSVFilter(filename)
        return self.csv_filter
    
