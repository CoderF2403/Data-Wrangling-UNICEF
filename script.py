import dataset
from csv import reader
import csv

"""
Usage: python script.py

This script is used to intake the male survey data from UNICEF and save it to a simple csv file
(or a MySQL Database if wished) after it has been checked for duplicates and missing data and after the headers 
have been properly matched with the data.

It expects there to be a 'mn.csv' file with the data and the 'mn_headers_updated.csv' file in a sub-folder called 
'unicef' within a data folder in this directory. It also expects there to be a MySql database called datawrangling.
Finally, it expects to utilize the dataset library (http://dataset.readthedocs.org/en/latest/).

If the script runs without finding any errors, it will save the cleaned data to the 'unicef_survey' folder in the MySQL 
or if wished can be saved into 'Data Files'.

The saved data will have the following structure:
- question: string
- question_code: string
- answer: string

If you have any questions, please feel free to contact me via faisalofficial2403@gmail.com
"""

# TODO : Please give the names of respective directories & url for database connection.
data_path = 'NAME OF DIRECTORY WHERE THE mn.csv IS SAVED'
header_path = 'NAME OF DIRECTORY WHERE mn_headers_updated.csv IS SAVED'
url = 'CHECK THE DATASET LIBRARY FOR MySQL URL FOR THIS SCRIPT'
file_path = 'PATH FOR ALL THE RESPONSES TO BE SAVED IN DIRECTORY'


def get_rows(data_file_path, headers_file_path):

    """
    This functions creates the list for all the rows in mn.csv and mn_headers_updated.csv.
    It uses list comprehension for creating both the lists, for headers_rows the headers present not present
    in data_rows[0] are eliminated.
    It returns both data_rows(with data of mn.csv) and headers_rows(with data of mn_headers_updated.csv.
    """

    data_reader = reader(open(data_file_path))
    header_reader = reader(open(headers_file_path))
    data_rows = [row for row in data_reader]
    header_rows = [headers for headers in header_reader if headers[0] in data_rows[0]]
    return data_rows, header_rows


def eliminator(data_rows, header_rows):

    """
    Return index numbers to skip in a list and final header rows in a list
    when given header rows and data rows from a UNICEF dataset. This
    function assumes the data_rows object has headers in the first element.
    It assumes those headers are the shortened UNICEF form. It also assumes
    the first element of each header row in the header data is the
    shortened UNICEF form. It will return the list of indexes to skip in the
    data rows (ones that don't match properly with headers) as the first element
    and will return the final cleaned header rows as the second element.
    """

    all_abbreviations = [h[0] for h in header_rows]
    skip_index = []
    final_header_rows = []
    for header in data_rows[0]:
        if header not in all_abbreviations:
            index = data_rows[0].index(header)
            skip_index.append(index)
        else:
            for head in header_rows:
                if head[0] == header:
                    final_header_rows.append(head)
    return final_header_rows, skip_index


def matched_data(data_rows, skip_index):

    """
    Here all the rows except the data_rows[0] are iterated and enumerate function is being used,
    for enumerating the data_rows.
    Then the enumeration is being searched in skip_index, if it is present in skip_index we do
    not append it in new_row.
    Then new_rows are being added to the new_data list.
    All data is now matched with headers.
    It returns new_data list.
    """

    new_data = []
    for row in data_rows[1:]:
        new_row = []
        for i, data in enumerate(row):
            if i not in skip_index:
                new_row.append(data)
        new_data.append(new_row)
    return new_data


def zipped_data(final_headers_row, new_data):

    """
    Final_header_rows and new_data is now zipped together and appended in zipped_rows
    zipped_rows is returned.
    """

    zipped_rows = []
    for d_row in new_data:
        zipped_rows.append(zip(final_headers_row, d_row))
    return zipped_rows


def duplicates_removal(zipped_rows):

    """
    Unzipping all the zipped rows into a list, of two tuples
    Which creates first tuples for all the questions and second tuple
    for all the answers.
    We iterate of the first tuple & append them into cleaned_header if not
    already present for eliminating duplicate data.
    As we do so, the second tuples of answer is also being searched for respective
    answers and appended to answer_lists.
    both cleaned header and answer header list are returned.
    """

    cleaned_header = []
    answer_list = []
    unzipped_data = list(zip(*zipped_rows))
    for headers in unzipped_data[0]:
        if headers not in cleaned_header:
            cleaned_header.append(headers)
            index = unzipped_data[0].index(headers)
            answer_list.append(unzipped_data[1][index])
    return cleaned_header, answer_list


def missing_answer(header, answer):

    """
    Returns a count of how many answers are missing in an entire set of zipped
    data. This function assumes all responses are stored as the second element.
    It also assumes every response is stored in a list of these matched question
    answer groupings. It returns an integer.
    """

    missing = 0
    for i in header[0]:
        index = header[0].index(i)
        if answer[index] is None:
            missing += 1
    return missing


def cleaned_data(zipped_rows):

    """
    Zipped rows are iterated, a counter is being set for numbering responses
    from each male, file name will be saved according to the response number.

    Duplicate data is now called for removing duplicate data,
    Missing function is also being called for searching for any missing
    answers. If found error is shown to developer.

    Inside iteration of zipped rows we iterate over headers returned by
    duplicate_removal, a dictionary is made for saving all the responses,
    for each question and answer.
    That dictionary is then appended to data list.

    data list saves each responses for each questions for each person.

    And finally we call the function to save all data into file.
    """

    for i in range(len(zipped_rows)):
        counter = i + 1
        filename = f'Response_{counter}.csv'
        header, answer = duplicates_removal(zipped_rows[i])
        missing = missing_answer(header, answer)
        if missing:
            print(f'{missing} Data Missing! PLease look up once!')
            break
        data = []
        for j in range(len(header)):
            data_dict = {
                'Question Code': header[j][0],
                'Question': header[j][1],
                'Answer': answer[j],
            }
            data.append(data_dict)
        headers = ['Question Code', 'Question', 'Answer']
        print(f'Saving Response {counter}')

        # TODO: YOU CAN ALSO USE THE DATABASE FUNCTION HERE
        # IF YOU WANT TO STORE DATA INTO DATA BASE
        write_to_file(file_path, filename, headers, data)


def save_to_database(data_dict, counter):

    """
    Data can also be saved to database if desired.
    """

    db = dataset.connect(url)
    table = db[f'Response_{counter}']
    table.insert(data_dict)


def write_to_file(file_path_save, filename, header, rows):

    """
    Make files for each response and save it to desired folder
    """

    with open(f'{file_path_save}{filename}', 'w') as file:
        file_csv = csv.DictWriter(file, header)
        file_csv.writeheader()
        file_csv.writerows(rows)


def main():

    """
    Import all data into rows, clean it, and then if
    no errors are found, save it to MySQl database or to folder as csv files.
    If there are errors found, print out details so
    developers can begin work on fixing the script
    or seeing if there is an error in the data.
    """

    data_rows, header_rows = get_rows(data_path, header_path)
    final_header_rows, skip_index = eliminator(data_rows, header_rows)
    new_data = matched_data(data_rows, skip_index)
    zipped_rows = zipped_data(final_header_rows, new_data)
    cleaned_data(zipped_rows)


if __name__ == '__main__':
    main()
