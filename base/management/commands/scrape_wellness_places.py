import html
import json
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from base.models import UserProfile, WellnessPlace


class Command(BaseCommand):
    help = "Scrapes wellness places from JSON and saves them to the database."

    JSON_FILE = "base/data/places.json"

    def handle(self, *args, **kwargs):
        with open(self.JSON_FILE, "r", encoding="utf-8") as file:
            places_data = json.load(file)

        for location, categories in places_data.items():
            for category, urls in categories.items():
                for url in urls:
                    # Scrape Arabic version
                    arabic_data = self.scrape_url(url)
                    if not arabic_data:
                        # self.stdout.write(self.style.ERROR(f"Failed to scrape: {url}"))
                        continue

                    name, description, image_url = arabic_data
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
                    )

                    # Fetch English version
                    english_url = url.replace("/ar/", "/en/")
                    english_data = self.scrape_url(english_url)
                    if english_data:
                        name, description, _ = english_data  # Keep same image
                        place_en = WellnessPlace.objects.create(
                            name=name,
                            description=description,
                            location=location,
                            image=image_url,  # Same image as Arabic
                            language="en",
                            experience_type=experience_type,
                            health_condition=health_condition,
                        )

                    self.stdout.write(self.style.SUCCESS(f"Saved: {name} ({location})"))
                    time.sleep(2)

    def scrape_url(self, url):
        """Scrapes meta content from the given URL."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to fetch {url}: Status code {response.status_code}"
                    )
                )
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            name = self.get_meta_content(soup, "og:title")
            description = self.get_meta_content(soup, "og:description")
            image_url = self.get_first_valid_image_url(response.text)

            if not (name and description and image_url):
                return None

            return name, description, image_url
        except requests.RequestException:
            return None

    def get_meta_content(self, soup, property_name):
        """Extracts content from meta tags."""
        tag = soup.find("meta", property=property_name)
        return tag["content"] if tag else None

    def get_first_valid_image_url(self, html_content):
        """Finds the first image URL matching the specified pattern, handling HTML entities."""
        # Decode HTML entities
        decoded_html = html.unescape(html_content)  # Converts &#34; to "

        # Find all matching image URLs
        matches = re.findall(
            r'"(https://scth\.scene7\.com/is/image/scth/[^"]+)"', decoded_html
        )
        return random.choice(matches) if matches else None
