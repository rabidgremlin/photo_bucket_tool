import glob
import os
from exif import Image
from datetime import datetime
import argparse
from tqdm import tqdm


# set up args parser
parser = argparse.ArgumentParser("set_dates", description="Set file dates from EXIF data")
parser.add_argument("-d","--directory", type=str, help="Directory containing images",required=True)
parser.add_argument("-r","--recursive", action="store_true", help="Recursively search for images in subdirectories", default=False)
args = parser.parse_args()

# build the search pattern using os.path.join
# TODO: support more then just .jpg files
if args.recursive:
    search_pattern = os.path.join(args.directory, "**", "*.jpg")
else:
    search_pattern = os.path.join(args.directory, "*.jpg")


files = glob.glob(search_pattern)
print(f"Found {len(files)} files matching pattern: {search_pattern}")

for file in tqdm(files, desc="Processing files", unit="file"):
    with open(file, "rb") as img_file:
        #TODO: update progress wil file name & warnings for missing EXIF data
        image = Image(img_file)
        if image.has_exif:        
            dt_created = datetime.strptime(image.datetime_original, "%Y:%m:%d %H:%M:%S")            
            file_ts = dt_created.timestamp()
            os.utime(file, (file_ts, file_ts))

print("All files processed.")            
    