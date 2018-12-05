'''
download_weather.py
downloads grib2 files from the National Weather Services' Rapid Refresh Model (RAP)
currently formatted for GCloud remote machine
'''


from subprocess import call
import os
import sys
import logging

def download(FILE,URL):
    """ 
    calls CURL to pull the file from a given URL
        URL is the target URL on remote
        FILE is the output file location on local
    requirements: "from subprocess import call"
        import removed from function for speed
    """
    CMD = ['curl','-o',FILE,URL]
    call(CMD)


# destination directory for saving files
folder = "/home/tbowling/airline/data/weather/"

# domain from which RAP data will be downloaded
domain = 'https://nomads.ncdc.noaa.gov/data/rucanl/'

# forecast to be downloaded
# hours in simulation time
# for rapid refresh model analysis, options are '000' (0 hours) and '001' (1 hour)
# for rapid refresh forcasts, options are from '000' to '018'
# forecast = '000' can be assumed to represent the real atmospheric state
forecast = '000'

# years to download
years = ['2017','2018']

# months per year to download
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

# days per month to download
# if days > actual days in a given month, will download non-existent (small) file
days = []
for i in range(1,31):
    if i < 10:
        days.append('0'+str(i))
    else:
        days.append(str(i))


# hours per day to download
# if hours > hours available in a given day, will download non-existent (small) file       
hours = []
for i in range(23):
    if i < 10:
        hours.append('0'+str(i)+'00')
    else:
        hours.append(str(i)+'00')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    # loop through time, download successive grib2 files
    for year in years:
        for month in months:
            for day in days:
                for hour in hours:
                    file = f'rap_130_{year}{month}{day}_{hour}_{forecast}.grb2'
                    url = domain + f'{year}{month}/' + f'{year}{month}{day}/' + file
                    destination = folder + file
                    try:
                        download(destination,url)
                        logging.info('Downloaded: ' + file)
                    except:
                        logging.info('No File: ' + file)
                        continue