#!/usr/bin/env python

"""
A sample JSON to CSV program. Multivalued JSON properties are space delimited 
CSV columns. If you'd like it adjusted send a pull request!
"""

from twarc import json2csv

import os
import sys
import json
import codecs
import argparse
import fileinput
from dateutil.parser import parse as date_parse
from twarc.json2csv import *

if sys.version_info[0] < 3:
    try:
        import unicodecsv as csv
    except ImportError:
        sys.exit("unicodecsv is required for python 2")
else:
    import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', help='write output to file instead of stdout')
    parser.add_argument('--split', '-s', help='if writing to file, split into multiple files with this many lines per '
                                              'file', type=int, default=0)
    parser.add_argument('--extra-field', '-e', help='extra fields to include. Provide a field name and a pointer to '
                                                    'the field. Example: -e verified user.verified',
                        nargs=2, action='append')
    parser.add_argument('--excel', '-x', help='create file compatible with Excel', action='store_true')
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    file_count = 1
    csv_file = None
    if args.output:
        if args.split:
            csv_file = codecs.open(numbered_filepath(args.output, file_count), 'wb', 'utf-8')
            file_count += 1
        else:
            csv_file = codecs.open(args.output, 'wb', 'utf-8')
    else:
        csv_file = sys.stdout
    sheet = csv.writer(csv_file)

    extra_headings = []
    extra_fields = []
    if args.extra_field:
        for heading, field in args.extra_field:
            extra_headings.append(heading)
            extra_fields.append(field)

    sheet.writerow(get_headings(extra_headings=extra_headings))

    files = args.files if len(args.files) > 0 else ('-',)
    for count, line in enumerate(fileinput.input(files, openhook=fileinput.hook_encoded("utf-8"))):
        if args.split and count and count % args.split == 0:
            csv_file.close()
            csv_file = codecs.open(numbered_filepath(args.output, file_count), 'wb', 'utf-8')
            sheet = csv.writer(csv_file)
            sheet.writerow(get_headings(extra_headings=extra_headings))
            file_count += 1

        try:
            tweet = json.loads(line)

            row = get_row(tweet, excel=args.excel)

            if row is None:
                continue

            sheet.writerow(row)
        except Exception as e:
            print("Occur error")
            print(line)
            print(e)


def get_value(t, field_str):
    obj = t
    for field in field_str.split('.'):
        if obj and field in obj:
            obj = obj[field]
        else:
            return None
    return obj


def get_row(t, excel=False):
    get = t.get
    user = t.get('user').get

    place = get('place')

    if place is None:
        if 'retweeted_status' not in t:
            return None

        retweeted_status = get('retweeted_status')
        place = retweeted_status.get('place')

        if place is None:
            if 'quoted_status' not in retweeted_status:
                return None

            place = retweeted_status.get('quoted_status').get('place')

    if place is None:
        return None

    bounding_box = place.get('bounding_box')

    coordinates = bounding_box.get('coordinates')
    longitude_min = min(coordinates[0][0][0], coordinates[0][1][0], coordinates[0][2][0], coordinates[0][3][0])
    longitude_max = min(coordinates[0][0][0], coordinates[0][1][0], coordinates[0][2][0], coordinates[0][3][0])
    latitude_min = min(coordinates[0][0][1], coordinates[0][1][1], coordinates[0][2][1], coordinates[0][3][1])
    latitude_max = min(coordinates[0][0][1], coordinates[0][1][1], coordinates[0][2][1], coordinates[0][3][1])

    longitude = (longitude_max + longitude_min) / 2
    latitude = (latitude_max + latitude_min) / 2

    '''
    
        'id',
        'created_at',
        'parsed_created_at',
        'text',
        'bounding_box',
        'longitude',
        'latitude',
        'country_code',
        'location',
        'tweet_type',
        'lang',
        'user_id'
    '''


    return [
        get('id_str'),
        get('created_at'),
        date_parse(get('created_at')),
        text(t) if not excel else clean_str(text(t)),
        bounding_box,
        longitude,
        latitude,
        place.get('country_code'),
        user('location') if not excel else clean_str(user('location')),
        tweet_type(t),
        get('lang'),
        user('id_str'),
    ]


def numbered_filepath(filepath, num):
    path, ext = os.path.splitext(filepath)
    return os.path.join('{}-{:0>3}{}'.format(path, num, ext))


def get_headings(extra_headings=None):
    # fields = json2csv.get_headings()
    # if extra_headings:
    #     fields.extend(extra_headings)
    # return fields

    return [
        'id',
        'created_at',
        'parsed_created_at',
        'text',
        'bounding_box',
        'longitude',
        'latitude',
        'country_code',
        'location',
        'tweet_type',
        'lang',
        'user_id'
    ]


# def get_row(t, extra_fields=None, excel=False):
#     row = json2csv.get_row(t, excel=excel)
#     if extra_fields:
#         for field in extra_fields:
#             row.append(extra_field(t, field))
#     return row


def extra_field(t, field_str):
    obj = t
    for field in field_str.split('.'):
        if obj and field in obj:
            obj = obj[field]
        else:
            return None
    return obj


if __name__ == "__main__":
    main()
