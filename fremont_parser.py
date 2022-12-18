# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:42:25 2019

@author: mark
"""

import os, re, sys



def dms_to_decimal(raw_dms_reading):
    """Takes a list of [D, M, S] and returns decimal reading"""
#    print(raw_dms_reading)
    degrees = int(raw_dms_reading[0])
    minutes = int(raw_dms_reading[1])
    seconds = int(raw_dms_reading[2])
#    print(seconds)
    decimal_reading = (seconds/3600) + (minutes/60) + degrees
    return decimal_reading
    
def main():
    current_filename_and_path = sys.argv[0]
    base_path = os.path.dirname(current_filename_and_path)
    print('test github')
    print(base_path)    
    filename = 'fremont_1843_1844.txt'
    out_folder = 'fremont_text_by_day'
    with open(os.path.join(base_path, filename)) as infile:
        file_str = infile.read()
    
    
    len(re.findall(r"[0-9]{3}° [0-9]{1,2}' [0-9]{1,3}", file_str))
    len(re.findall(r"[0-9]{2}° [0-9]{1,2}' [0-9]{1,3}", file_str))
    
    
    
    # In the original text all months are in CAPS and nothing else follows this pattern
    # so it is easy to split based on month. This makes a list that alternates between
    # the month and then the text for that month which can be iterated through
    
    months_text = re.split(r'\n([A-Z\.]{3,10})\n', file_str)
    
    days_list = []
    month = ''
    year = '1843'
    file_num_sequence = 1 
    for text in months_text[1:]:
        # months are less than 20 characters long.  The expedition ended in 1844 so 
        # the year only needs to be incremented once
        if len(text) < 20:
            month = text
            if month == 'JANUARY.':
                year = '1844'
    #        print(month, year)
        else: # else parse the text for that month
            # days are referenced either as 'on the 8th' or simply '1st.'  etc.
            iter_days = re.finditer(r'([0-9]){1,2}[dsth]{1,2}\.--', text)
            iter_days_on_the = re.finditer(r'[oO]n the ([0-9]{1,2}[dsth]{1,2})', text)
            days_list = [x for x in iter_days]
            for x in iter_days_on_the:
                days_list.append(x)
        #    print(text[0:100])
    #        print('days:{}\t days on the:{}\t text length:{}'.format(len(days), 
    #                      len(days_on_the),
    #                        len(text) ))
            # sorts by earliest index  match position
            days_list.sort(key=lambda x: x.span(0)[0])
        
            start_index = 0
            last_day = 1
            for day in days_list[1:]:
                current_day = int(re.search(r'[0-9]{1,2}', day.group()).group())
                # Some days reference other days this checks to see if all are in
                # order.  If not pass.
                if current_day > last_day:
                    
                    long = re.findall(r"[0-9]{3}° [0-9]{1,2}' [0-9]{1,3}", text[start_index:day.span(0)[0]])
                    lat = re.findall(r" [0-9]{2}° [0-9]{1,2}' [0-9]{1,3}", text[start_index:day.span(0)[0]])
                    
                    ofname = '{}_{}_{}_{}.txt'.format(file_num_sequence,
                                                      year, 
                                                      month.replace('.',''), 
                                                      last_day)
                    file_num_sequence += 1
                    if (len(long) == 1) and (len(lat) == 1):
                        dec_lon = 0 -dms_to_decimal(long[0].replace('°','').replace("'", '').split(' '))
                        dec_lat = dms_to_decimal(lat[0].replace('°','').replace("'", '').split(' ')[1:])
    #                    print(ofname, dec_lon, dec_lat )
                        
                    elif (len(long) == 0) and (len(lat) == 1):
    #                    dec_lon = 0 -dms_to_decimal(long[0].replace('°','').replace("'", '').split(' '))
                        dec_lat = dms_to_decimal(lat[0].replace('°','').replace("'", '').split(' ')[1:])
                        print(ofname, lat )
                    elif (len(long) > 1) and (len(lat) > 1):
    #                    dec_lon = 0 -dms_to_decimal(long[0][0].replace('°','').replace("'", '').split(' '))
    #                    dec_lat = dms_to_decimal(lat[0][0].replace('°','').replace("'", '').split(' ')[1:])
                        print(ofname, year, month, last_day, long, lat )
                        print('\n')
                    with open(os.path.join(base_path, out_folder, ofname), 'w') as ofile:
    #                    ofile.write(long)
    #                    ofile.write(lat)
                        ofile.write(text[start_index:day.span(0)[0]])
                        start_index = day.span(0)[0]
                    last_day = current_day
                    
if __name__ == '__main__':
    main()
    