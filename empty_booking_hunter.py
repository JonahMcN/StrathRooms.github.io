
import pandas as pd
# Load room details and bookings
room_list = pd.read_csv("room_details.csv")
room_bookings = pd.read_csv("room_bookings.csv")
# Change time format from csv
room_bookings['Start'] = pd.to_datetime(room_bookings['Start'], format='%H:%M').dt.time
room_bookings['End'] = pd.to_datetime(room_bookings['End'], format='%H:%M').dt.time

import csv
# empty bookings writer
empty_bookings_file = open('empty_bookings.csv', 'w+', newline='')
d_fieldnames = ['Room Code','Day','Free From','Free Till']
writer = csv.DictWriter(empty_bookings_file,fieldnames=d_fieldnames)
writer.writeheader()

from datetime import datetime
open_time = datetime.strptime("8:00", '%H:%M').time()   
close_time = datetime.strptime("17:00", '%H:%M').time()

## Find times when each room is free
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
# room loop
for r in range(len(room_list)):
    room_code = room_list.iloc[r]['Room Code']
    # day loop
    for day in days:
        time = open_time
        current_room_bookings = room_bookings[room_bookings['Room'] == room_code]
        bookings_today = current_room_bookings[current_room_bookings['Day'] == day]

        if bookings_today.empty:
            free_from = open_time
            free_till = close_time
            writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
            continue

        for i in range(len(bookings_today)):
                           
            # if first booking of the day check if there is space before 
            if i == 0:
                if bookings_today.iloc[i]['Start'] > open_time:
                    free_from = open_time
                    free_till = bookings_today.iloc[i]['Start']
                    writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
            # if last booking in the day check if there is space before close
            if  i == len(bookings_today)-1:
                if bookings_today.iloc[i]['End'] < close_time:
                    free_from = bookings_today.iloc[i]['End']
                    free_till = close_time
                    writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
            # if not the first or last booking in the day check if there is space between bookings
            if bookings_today.iloc[i-1]['End'] < bookings_today.iloc[i]['Start']:
                free_from = bookings_today.iloc[i-1]['End']
                free_till = bookings_today.iloc[i]['Start']
                writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
                    
    