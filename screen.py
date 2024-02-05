from selenium import webdriver


def get_url(ticker_symbol, url):
    # Create a new instance of the Chrome webdriver
    driver = webdriver.Chrome()

    # Open the web page
    driver.get(url)

    # Capture a screenshot and save it as a PNG file
    driver.save_screenshot(f"{ticker_symbol}/homepage.png")

    # Close the browser
    driver.quit()


def main():
    get_url("TSLA", "https://www.apple.com")


if __name__ == "__main__":
    main()
