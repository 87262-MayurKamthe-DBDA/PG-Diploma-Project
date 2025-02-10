# import the packages
import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver as webdriver
from time import sleep
import re
import time



# crate the class name as time_travel
# where it crates and returns the traveling time

class Time_travel:

    def __init__(self, destination: str, source: str, driver: webdriver):
        """
        Initialize the TimeTravel object with a destination, source, and Selenium WebDriver.
        """
        self.destination = destination
        self.source = source
        self.driver = driver.Chrome()
        self.__url = ""

    def car_button_click(self):
        """
        Constructs the Google Maps URL, opens it in the driver, and clicks the car button to set route mode to driving.
        """
        # Construct URL for Google Maps directions from source to destination
        base_url = "https://www.google.com/maps/dir/"
        self.__url = f"{base_url}{self.source}/{self.destination}/"

        # Open the URL in the driver
        self.driver.get(self.__url)
        print(f"Navigating to URL: {self.__url}")
        sleep(10)  # Wait for the page to load


        car_button = self.driver.find_element(By.XPATH,
            "/html/body/div[2]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button")
        car_button.click()

        # Update the URL after selecting the driving mode
        self.__url = self.driver.current_url
        print(f"Updated URL with driving mode: {self.__url}")

    def add_time_traveling(self, time_stamp: int):
        """
        Modifies the URL to include a specific travel time based on a timestamp (in milliseconds).
        Retrieves the estimated travel time from the web page.
        """
        # Add timestamp to the current URL
        if not self.__url:
            raise ValueError("URL is not set. Please call car_button_click() first.")

        current_url = self.__url
        add_8_index = re.search(r"4m1", current_url)

        if add_8_index:
            current_url = current_url[:add_8_index.end()] + "8" + current_url[add_8_index.end()+1:]

        add_7_index = re.search(r"8!4m1", current_url)
        if add_7_index:
            current_url = current_url[:add_7_index.end()] + "7" + current_url[add_7_index.end()+1:]

        unknown_part = "!2m3!6e0!7e2!8j"
        timestamp_str = str(int(time_stamp / 1000))  # Convert to seconds
        car_code = "!3e0"
        new_url = current_url + unknown_part + timestamp_str + car_code

        print(f"Modified URL with timestamp: {new_url}")
        self.driver.get(new_url)

        # Fetch the estimated travel time
        sleep(5)  # Allow some time for the page to update

        try:
            distance_element = self.driver.find_element(By.XPATH,
                "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[5]/div[1]/div[1]/div/div[1]/div[1]")
            traveling_distance = self.driver.find_element(By.XPATH,
                "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[5]/div[1]/div[1]/div/div[1]/div[2]")
            travel_time = distance_element.text
            print(travel_time, traveling_distance.text)
            return travel_time, traveling_distance.text
        except Exception as e:
            print(f"Error fetching travel time: {e}")
            return None




