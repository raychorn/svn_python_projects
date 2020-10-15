'''
https://gist.github.com/seemethere/8c264c31a277bab47f80cec3e53b7b79#file-csv_filter-ipynb
'''

filename = 'FL_insurance_sample.csv\FL_insurance_sample.csv'

if (__name__ == '__main__'):
    if (0):
        import csv
        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print ', '.join(row)
    else:
        from csv_loader import KeywordFilterList
        csv_filter = KeywordFilterList.load_csv(filename)
        print len(csv_filter)
        matches = csv_filter.get(policyID='119736')
        print len(matches)
        for row in matches:
            print row
        matches = csv_filter.get(policyID=('119736', '371891'))
        print len(matches)
        for row in matches:
            print row
        matches = csv_filter.get(line='Residential', construction='Wood', point_granularity='3', county='CLAY COUNTY', hu_site_limit='48115.94')
        print len(matches)
        for row in matches:
            print row
        print(csv_filter.get(line='Residential', construction='Wood', point_granularity='3', county='CLAY COUNTY', hu_site_limit='48115.94').to_csv())        
        pass
            