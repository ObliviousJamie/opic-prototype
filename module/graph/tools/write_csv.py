import csv


class WriteCSV:

    @staticmethod
    def write(rows_dict, save_location):
        print('Writing...')
        fieldnames = sorted(list(rows_dict.keys()))
        with open(save_location, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames= fieldnames)
            writer.writeheader()
            writer.writerow(rows_dict)
        print('Done')
