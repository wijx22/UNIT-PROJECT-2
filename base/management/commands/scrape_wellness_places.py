import html
import json
import random
import re
import time

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from base.models import UserProfile, WellnessPlace


class Command(BaseCommand):
    help = "Scrapes wellness places from JSON and saves them to the database."

    JSON_FILE = "base/data/places.json"

    def handle(self, *args, **kwargs):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # service = Service("chromedriver")
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

        with open(self.JSON_FILE, "r", encoding="utf-8") as file:
            places_data = json.load(file)

        for location, categories in places_data.items():
            for category, urls in categories.items():
                for url in urls:
                    # Scrape Arabic version
                    arabic_data = self.scrape_url(driver, url)
                    if not arabic_data:
                        continue

                    name, description, image_url, content = arabic_data
                    experience_type = random.choice(UserProfile.EXPERIENCE_CHOICES)[0]
                    health_condition = random.choice(UserProfile.HEALTH_CHOICES)[0]

                    # Save Arabic entry
                    place_ar = WellnessPlace.objects.create(
                        name=name,
                        description=description,
                        location=location,
                        image=image_url,
                        language="ar",
                        experience_type=experience_type,
                        health_condition=health_condition,
                        content=content,
                    )

                    # Fetch English version
                    english_url = url.replace("/ar/", "/en/")
                    english_data = self.scrape_url(driver, english_url)
                    if english_data:
                        name, description, _, content = english_data  # Keep same image
                        place_en = WellnessPlace.objects.create(
                            name=name,
                            description=description,
                            location=location,
                            image=image_url,  # Same image as Arabic
                            language="en",
                            experience_type=experience_type,
                            health_condition=health_condition,
                            content=content,
                        )

                    self.stdout.write(self.style.SUCCESS(f"Saved: {name} ({location})"))
                    time.sleep(2)

        driver.quit()  # Close the Selenium driver

    def scrape_url(self, driver: webdriver.Chrome, url):
        """Scrapes meta content from the given URL using Selenium."""
        try:
            driver.get(url)
            time.sleep(3)  # Wait for page to load fully

            soup = BeautifulSoup(driver.page_source, "html.parser")

            name = self.get_meta_content(soup, "og:title")
            description = self.get_meta_content(soup, "og:description")
            image_url = self.get_first_valid_image_url(driver.page_source)
            content = self.get_content(driver.page_source)

            if not (name and description and image_url):
                return None

            return name, description, image_url, content
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch {url}: {e}"))
            return None

    def get_content(self, html_content):
        """Extracts and formats content from divs with specific classes, styled with Tailwind CSS."""
        soup = BeautifulSoup(html_content, "html.parser")
        left_col = soup.find("div", class_="leftCol2")

        if not left_col:
            return ""

        formatted_content = ""

        for section in left_col.find_all(
            "div", class_=re.compile("text-default flex w-full flex-col bg-transparent")
        ):
            h3 = section.find("h3")
            p = section.find("p")

            if h3 and p:
                formatted_content += f"""
                    <div class="mb-4 p-4">
                        <h3 class="text-lg font-semibold text-gray-800">{h3.text.strip()}</h3>
                        <p class="text-gray-600 mt-2">{p.text.strip()}</p>
                    </div>
                """

        return formatted_content

    def get_meta_content(self, soup, property_name):
        """Extracts content from meta tags."""
        tag = soup.find("meta", property=property_name)
        return tag["content"] if tag else None

    def get_first_valid_image_url(self, html_content):
        """Finds the first image URL with class 'lazyloaded'."""
        soup = BeautifulSoup(html_content, "html.parser")
        img_tag = soup.find("img", class_="lazyloaded")

        if img_tag and "src" in img_tag.attrs:
            return img_tag["src"]

        return None
