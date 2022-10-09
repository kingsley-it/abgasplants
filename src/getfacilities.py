import sys
import os
import getopt
import requests
import validators
import pandas as pd

#09-13-036-25W4

def download_facilities(url, output):
    try:
        r = requests.get(url, allow_redirects=True)
        open(output, 'wb').write(r.content)
    except Exception as e:
        print("Something went wrong:", e)
        return False

    return True

def build_lsd(rec):
    #print("*" + rec['LSD'] + "*")
    #print(rec['SEC'])
    #print(rec['TWP'])
    #print(rec['RNG'])
    #print(rec['MER'])

    if len(rec['LSD'].strip()) > 0 :
        return "{0:02d}-{1:02d}-{2:03d}-{3:02d}{4}".format(int(rec['LSD']), int(rec['SEC']), int(rec['TWP']),
                                                           int(rec['RNG']), rec['MER'])
    else:
        return "{0:02d}-{1:03d}-{2:02d}{3}".format( int(rec['SEC']), int(rec['TWP']),
                                                           int(rec['RNG']), rec['MER'])

def get_parameters( ):

    params = {"url": None, "output": None}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:o:c:", ["url=", "output=", "csv="])
    except getopt.GetoptError:
        print('getfacilities.py -u <url> -o <output> -c <csv>')
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-h':
                print ('getfacilities.py -u <url> -o <output> -c <csv>')
                sys.exit()
            elif opt in ("-u", "--url"):
                params['url'] = arg
            elif opt in ("-o", "--output"):
                params['output'] = arg
            elif opt in ("-c", "--csv"):
                params['csv'] = arg

    return params

def get_export_columns():
    col_names = [
        'Facility ID',
        'Facility Name',
        'Operator Code',
        'Operator Name',
        'Sub Type Code',
        'Sub Type',
        'Licence Number',
        'EDCT Code',
        'EDCT Description',
        'Licensee Code',
        'Status',
        'Survey']
    return col_names

def export_facilities( facilities, file_path ):

    df = pd.DataFrame(data=facilities, columns=get_export_columns())

    df.to_csv(file_path, index=False, header=True)

def copy_facility(src) :
    dst = {'Facility ID': src['Facility ID'], 'Facility Name': src['Facility Name'],
           'Operator Code': src['Operator Code'], 'Operator Name': src['Operator Name'],
           'Sub Type Code': src['Sub Type Code'], 'Sub Type': src['Sub Type'], 'Licence Number': src['Licence Number'],
           'EDCT Code': src['EDCT Code'], 'EDCT Description': src['EDCT Description'],
           'Licensee Code': src['Licensee Code'], 'Status': src['Status']}
    return dst

if __name__ == '__main__':

    params = get_parameters()  # next section explains the use of sys.exit

    if not download_facilities(params['url'], params['output']):
        sys.exit(2)

    col_names = [
    'Facility ID',
    'Facility Name',
    'Operator Code',
    'Operator Name',
    'Sub Type Code',
    'Sub Type',
    'LE',
    'LSD',
    'SEC',
    'TWP',
    'RNG',
    'MER',
    'Licence Number',
    'EDCT Code',
    'EDCT Description',
    'Licensee Code',
    'Status']

    facilities =[]

    dngCNT = 0

    df = pd.read_table(params['output'], skiprows=5, sep='\t', names=col_names, encoding='latin1')

    for rec in df.to_records():

        if type(rec['Facility ID']) is not str or "*" in rec['Facility ID'] :
            continue

        print(rec['Facility ID'])

        facility = copy_facility(rec)
        facility['Survey'] = build_lsd(rec)
        facilities.append(facility)
        dngCNT += 1
#       if dngCNT > 2:
#       break
#       print(dngCNT)

export_facilities(facilities, params['csv'])