import csv
# details reader
room_list = open('room_details.csv',newline='')
room_list_reader = csv.DictReader(room_list)
# bookings reader
room_bookings = open('room_bookings.csv',newline='')
room_bookings_reader = csv.DictReader(room_bookings)
room_bookings = list(room_bookings_reader)

# empty bookings writer
empty_bookings_file = open('empty_bookings.csv', 'w+', newline='')
d_fieldnames = ['Room Code','Day','Free From','Free Till']
writer = csv.DictWriter(empty_bookings_file,fieldnames=d_fieldnames)
writer.writeheader()

from datetime import datetime
open_time = datetime.strptime("8:00", '%H:%M').time()   
close_time = datetime.strptime("17:00", '%H:%M').time()

## Find times when each room is free
days = ["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]
# room loop
for row_room in room_list_reader:
    room_code = row_room['Room Code']
    # day loop
    for day in days:
        time = open_time
        # booking loop
        for i in range(len(room_bookings)):
            if room_bookings[i]['Room'] == room_code: # check current booking matches current room
                if room_bookings[i]['Day'] == day: # check current booking matches current day
                    booking_start = datetime.strptime(room_bookings[i]['Start'], '%H:%M').time()
                    booking_end = datetime.strptime(room_bookings[i]['End'], '%H:%M').time()
                    if booking_start > time and booking_end <= close_time:
                        free_from = time
                        free_till = booking_start
                        writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
                    if i+1 < len(room_bookings):
                        if (room_bookings[i+1]['Day'] != day or i+1 > len(room_bookings)) and booking_end < close_time:
                            free_from = room_bookings[i]['End']
                            free_till = close_time
                            writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
                    elif booking_end < close_time:
                        free_from = room_bookings[i]['End']
                        free_till = close_time
                        writer.writerow({'Room Code':room_code,'Day':day,'Free From':str(free_from)[:5],'Free Till':str(free_till)[:5]})
                    time = booking_end
          
                       
                