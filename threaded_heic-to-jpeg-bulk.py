"""A heic to jpeg bulk converter tool"""
import os, subprocess, shutil, sys, threading, time, argparse
from os.path import join


def convert_from_heic_to_jpg(heic_file, jpeg_file, out_path):
    """Feed filenames to magick convert utility and execute the conversion itself"""
    try:
        cmd = f"magick {heic_file} {jpeg_file}"
        c = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        c.communicate()
        if not c:
            sys.exit(1)
        else:
            shutil.move(jpeg_file, out_path)
            return True
    except Exception as e:
        print(e)
        return False

def main():
    parser=argparse.ArgumentParser(description="HEIC Bulk Converter", \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--source", required=True, type=str, help="Source directory. Supports subdirectories")
    parser.add_argument("--destination", required=True, type=str, help="Output directory")
    config=vars(parser.parse_args())

    # Get values from arguments dictionary config[]
    base_path=config['source']
    out_path=config['destination']

    threads=[]
    
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            if filename.lower().endswith(".heic"):
                fname_heic = str(join(root, filename))
                fname_jpg = str(join(root, filename.split(".")[0]+".jpg"))
                t = threading.Thread(target=convert_from_heic_to_jpg, args=(fname_heic, fname_jpg, out_path))
                threads.append(t)
                print(f"starting threaded execution... for {t}")
                t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    exec_time = end_time - start_time
    print("Time for execution: ", exec_time)