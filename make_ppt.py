from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET
from pdf2image import convert_from_path
import configparser

import os
import shutil
import zipfile
from yf_charts import default_narration, get_charts
from screen import get_url

image_clips = []
audio_clips = []
starts = []
config = {}

root_dir = "temp/ppt/"
slide_dir = "temp/ppt/slides/"
notes_dir = "temp/ppt/notesSlides/"
notes_mp4_folder = "temp/notes_mp4"
media = "temp/ppt/media/"


page_map = {
    "title": "slide1",
    "disclaimer": "slide2",
    "overview": "slide3",
    "long_term_chart": "slide4",
    "headlines": "slide7",
}
narration = {
    "Headline1": "First headline",
    "Headline2": "Second longer line from some article",
    "Headline3": "Third",
    "Headline4": "Fourth 4444444 4  4 4 4 4 4  4 4 4 4  4 4 ",
    "Headline5": "Five",
    "Headline6": "Six",
    "Headline7": "Seven",
    "Headline8": "Eight",
}

image_map = {
    "logo": "image1.png",
    "recommendations": "image2.png",
    "up_down": "image3.png",
    "earnings": "image4.png",
    "90_bollinger": "image5.png",
    "90_rsi": "image6.png",
    "homepage": "image7.png",
    "90_macd": "image8.png",
    "insider": "image9.png",
    "5 Day_candle": "image10.png",
    "365_ma": "image11.png",
    "90 Day_candle": "image12.png",
    "5 Year_candle": "image13.png",
}


def replace_images(company, ticker_symbol):
    for key, value in image_map.items():
        dst = media + value
        src = f"{ticker_symbol}/{key}.png"
        shutil.copy(src, dst)


def clean_up():
    if os.path.exists("temp_images"):
        shutil.rmtree("temp_images")
    if os.path.exists("temp"):
        shutil.rmtree("temp")


def open_template(template_file, ticker_symbol):
    if not os.path.exists(notes_mp4_folder):
        os.makedirs(notes_mp4_folder)

    # Uzip the input ppt file
    with zipfile.ZipFile(template_file, "r") as zip_ref:
        zip_ref.extractall("temp")


def zip_ppt(temp_folder, output_file):
    with zipfile.ZipFile(output_file, "w") as zip_ref:
        for foldername, subfolders, filenames in os.walk(temp_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_folder)
                zip_ref.write(file_path, arcname)


def title(company, ticker_symbol):
    filename = slide_dir + page_map["title"] + ".xml"
    try:
        # Open the file in read mode
        with open(filename, "r") as file:
            # Read the content of the file
            content = file.read()

        # Replace 'Company' with company
        updated = content.replace("Company", company)
        # Replace the date
        today = date.today().strftime("%m/%d/%Y")
        updated = updated.replace("Date", today)

        # Open the file in write mode to overwrite
        with open(filename, "w") as file:
            # Write the updated content back to the file
            file.write(updated)

        print(f"Replacement successful. '{filename}' has been updated.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def overview(company, ticker_symbol):
    filename = slide_dir + page_map["overview"] + ".xml"
    try:
        # Open the file in read mode
        with open(filename, "r") as file:
            # Read the content of the file
            content = file.read()

        # Replace Tagline
        global config
        t = config["tagline"]
        updated = content.replace("Tagline", config["tagline"])

        # Open the file in write mode to overwrite
        with open(filename, "w") as file:
            # Write the updated content back to the file
            file.write(updated)

        print(f"Replacement successful. '{filename}' has been updated.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def headlines(company, ticker_symbol):
    filename = slide_dir + page_map["headlines"] + ".xml"
    try:
        # Open the file in read mode
        with open(filename, "r") as file:
            # Read the content of the file
            content = file.read()

        # Replace 'Company' with company
        i = 0
        while i < 8:
            target = f"Headline{i+1}"
            update = content.replace(target, narration[target])
            content = update
            i += 1

        # Open the file in write mode to overwrite
        with open(filename, "w") as file:
            # Write the updated content back to the file
            file.write(content)

        print(f"Replacement successful. '{filename}' has been updated.")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_logo(ticker_symbol):
    global config
    dst = f"{ticker_symbol}/logo.png"
    logo = config["logo"]
    shutil.copy(config["logo"], dst)


def setup():
    os.makedirs("temp", exist_ok=True)

    temp_images_folder = "temp/temp_images"
    if not os.path.exists(temp_images_folder):
        os.makedirs(temp_images_folder)


def usage():
    print("\nUsage:\npython3 make_ppt.py config")
    exit(0)


def read_config_file(file_path):
    cfg = configparser.ConfigParser()
    cfg.read(file_path)

    # Check if the section 'settings' exists in the configuration file
    if "settings" in cfg:
        # Convert the settings from the configuration file to a dictionary
        settings_dict = dict(cfg["settings"])
        return settings_dict
    else:
        print("Error: 'settings' section not found in the configuration file.")
        return {}


def main():
    clean_up()
    setup()

    global config
    config = read_config_file("config.ini")
    company = config["company"]
    ticker_symbol = config["ticker"]
    url = config["url"]

    get_logo(ticker_symbol)

    # Create the charts
    today_date = datetime.now().date()
    five_years = (datetime.now() - timedelta(days=365 * 5)).date()

    # Initialize the relatively static narration
    default_narration(company, ticker_symbol, today_date)
    # Plot the candlestick chart
    get_charts(ticker_symbol, five_years, today_date)
    get_url(ticker_symbol, url)

    # Start with the template
    open_template("template.pptx", ticker_symbol)
    title(company, ticker_symbol)
    overview(company, ticker_symbol)
    headlines(company, ticker_symbol)
    replace_images(company, ticker_symbol)

    zip_ppt("temp", f"{ticker_symbol}.pptx")


if __name__ == "__main__":
    main()
