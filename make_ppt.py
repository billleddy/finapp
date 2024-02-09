from datetime import date, datetime, timedelta
import xml.etree.ElementTree as ET
from pdf2image import convert_from_path
import configparser

import os
import shutil
import zipfile
from yf_charts import default_narration, get_charts, narration
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

# "This is a review of {company} and its financial outlook using publicly available data, some AI interpretation of that data and random commentary."

page_map = {
    "title": "slide1",
    "disclaimer": "slide2",
    "overview": "slide3",
    "long_term_chart": "slide4",
    "headlines": "slide7",
    "EPS": "slide10",
}

# Whenever the Template.pptx gets updated, it seems that the image names
# get shuffled so this mapping needs to be adjusted
image_map = {
    "logo": "image2.png",
    "recommendations": "image4.png",
    "90 Day_candle": "image7.png",
    "up_down": "image5.png",
    "earnings": "image8.png",
    "90_bollinger": "image9.png",
    "90_rsi": "image12.png",
    "homepage": "image3.png",
    "90_macd": "image11.png",
    "insider": "image13.png",
    "5 Day_candle": "image10.png",
    "5 Year_candle": "image6.png",
    "365_ma": "image14.png",
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


def update_narration(slidename, str):
    filename = notes_dir + slidename.replace("slide", "notesSlide") + ".xml"
    try:
        # Open the file in read mode
        with open(filename, "r") as file:
            # Read the content of the file
            content = file.read()

        # Replace '_narration_' with the str
        updated = content.replace("_narration_", str)

        # Open the file in write mode to overwrite
        with open(filename, "w") as file:
            # Write the updated content back to the file
            file.write(updated)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    update_narration(
        page_map["title"],
        f"This is a review of {company} and its financial outlook using publicly available data, some AI interpretation of that data and random commentary.",
    )


def eps(company, ticker_symbol):
    filename = slide_dir + page_map["EPS"] + ".xml"
    try:
        # Open the file in read mode
        with open(filename, "r") as file:
            # Read the content of the file
            content = file.read()

        # Replace Tagline
        global config
        updated = content.replace("Next_EPS", narration["next_EPS"])

        # Open the file in write mode to overwrite
        with open(filename, "w") as file:
            # Write the updated content back to the file
            file.write(updated)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    update_narration(page_map["EPS"], narration["EPS"])


def overview(company, ticker_symbol):
    filename = slide_dir + page_map["overview"] + ".xml"
    try:
        # Open the file in read mode
        with open(filename, "r") as file:
            # Read the content of the file
            content = file.read()

        # Replace Tagline
        global config
        updated = content.replace("Tagline", config["tagline"])

        # Open the file in write mode to overwrite
        with open(filename, "w") as file:
            # Write the updated content back to the file
            file.write(updated)

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def headlines(company, ticker_symbol):
    global narration
    slidename = slide_dir + page_map["headlines"] + ".xml"
    try:
        # Open the file in read mode
        with open(slidename, "r") as file:
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
        with open(slidename, "w") as file:
            # Write the updated content back to the file
            file.write(content)

    except FileNotFoundError:
        print(f"File '{slidename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    update_narration(page_map["headlines"], narration["Headlines"])


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

    os.makedirs(ticker_symbol, exist_ok=True)

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
    open_template("Template2.pptx", ticker_symbol)
    title(company, ticker_symbol)
    overview(company, ticker_symbol)
    headlines(company, ticker_symbol)
    eps(company, ticker_symbol)
    replace_images(company, ticker_symbol)

    zip_ppt("temp", f"{ticker_symbol}.pptx")


if __name__ == "__main__":
    main()
