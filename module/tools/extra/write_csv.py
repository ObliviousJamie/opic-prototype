import csv

from tqdm import tqdm


class WriteCSV:

    @staticmethod
    def write_scores(header, scores, save_location, beta=1):
        print('Writing...')
        with open(f"{save_location}f{beta}.csv", 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            for method, fscores in tqdm(scores.items(), desc="Writing to CSV"):
                row = [str(method)]
                for score in fscores:
                    row.append(str(score[beta - 1]))
                writer.writerow(row)
