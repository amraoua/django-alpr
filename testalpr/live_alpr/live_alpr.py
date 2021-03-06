from openalpr import Alpr
from argparse import ArgumentParser
import csv, os, sys, threading

parser = ArgumentParser(description="Live ALPR")

parser.add_argument("-c", "--country", dest="country", action="store", default="eu",
                    help="License plate Country of Origin")
                    
parser.add_argument("-r", "--region", dest="region", action="store", default="",
                    help="License plate Regions of Origin")
                    
parser.add_argument("-i", "--config_file", dest="config_file", action="store", default="/home/pi/openalpr3/config/openalpr.conf.defaults",
                    help="Path to openalpr.conf config file")
                    
parser.add_argument("-d", "--runtime_data", dest="runtime_dir", action="store", default="/home/pi/openalpr3/runtime_data",
                    help="Path to openalpr runtime data directory")
                    
parser.add_argument("-p", "--image_folder", dest="image_folder", action="store", default="/home/pi/Documents/projects/django-alpr/testalpr/live_alpr/images",
                    help="Path to images that will automaticly be processed")
                    
parser.add_argument("-f", "--csv_file", dest="csv_file", action="store", default="/home/pi/Documents/projects/django-alpr/testalpr/live_alpr/database.csv",
                    help="Path to the csv file that license plates will be matched to")

parser.add_argument("-t", "--move_to", dest="image_dest", action="store", default="/home/pi/Documents/projects/django-alpr/testalpr/live_alpr/images/done",
                    help="Path to moce processed images to when done")

parser.add_argument("-v", "--verbose", dest="verbose", action="store", default="true")

options = parser.parse_args()

alpr = Alpr(options.country, options.config_file, options.runtime_dir)

if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

alpr.set_top_n(20)
#alpr.set_default_region(options.region)

print("%-24s%-12s%-6s%-40s" % ("Image Name", "Plate", "Conf", "Details"))


def search_database(lpNumber):
        with open(options.csv_file) as database:
                reader = csv.DictReader(database)
                for row in reader:
                        if row['lp_number'].lower() == lpNumber.lower():
                                return row['LastName'] + ", " + row['FirstName'] + " " + row['Department']
                        else:
                                return ""


def process_results(fileName, results):
        for plate in results['results']:
                for candidate in plate['candidates']:
                        resultStr = search_database(candidate['plate'])
                        if resultStr != "":
                                print("%-24s%-12s%-6.2f%-40s" % (fileName, candidate['plate'], candidate['confidence'], resultStr))
                        elif options.verbose == "true":
                                print("%-24s%-12s%-6.2s%-40s" % (fileName, candidate['plate'],candidate['confidence'], "No match"))


def process_images():
        for file in os.listdir(options.image_folder):
                if file.endswith(".jpg") or file.endswith(".png"):
                        results = alpr.recognize_file(options.image_folder + file)
                        process_results(file, results)
                        os.rename(options.image_folder + file, options.image_dest + file)
        threading.Timer(1, process_images).start()
        
process_images()
