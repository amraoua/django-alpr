from openalpr import Alpr


# Initialize the library using United States style license plates.
# You can use other countries/regions as well (for example: "eu", "au", or "kr")
alpr = Alpr("eu", "/home/pi/openalpr3/config/openalpr.conf.defaults", "/home/pi/openalpr3/runtime_data")


# Make sure the library loaded before continuing.
# For example, it could fail if the config/runtime_data is not found
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# Optionally specify the top N possible plates to return (with confidences).  Default is 10
alpr.set_top_n(20)

# Optionally, provide the library with a region for pattern matching.  This improves accuracy by
# comparing the plate text with the regional pattern.
# alpr.set_default_region("md")

# Recognize an image file.  You could alternatively provide the image bytes in-memory.
results = alpr.recognize_file("/home/pi/Documents/projects/django-alpr/templates/alpr_capture.jpg")

# Iterate through the results.  There may be multiple plates in an image,
# and each plate returns the top N candidates.
i = 0
for plate in results['results']:
    i += 1
    print("Plate #%d" % i)
    print("   %12s %12s" % ("Plate", "Confidence"))
    for candidate in plate['candidates']:
        prefix = "-"
        if candidate['matches_template']:
            prefix = "*"
            print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

# Call when completely done to release memory
alpr.unload()