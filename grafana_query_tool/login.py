from playwright.sync_api import sync_playwright
import os, time
from dotenv import load_dotenv
from websession.websession import WebSession

def login(
  websession: WebSession,
  env_file: str = ".env",
) -> WebSession:

  load_dotenv(env_file)

  GRAFANA_USERNAME = os.getenv('GRAFANA_USERNAME')
  GRAFANA_PASSWORD = os.getenv('GRAFANA_PASSWORD')
  GRAFANA_URL = os.getenv('GRAFANA_URL')

  print(f"Attempting to login to {GRAFANA_URL}.")

  websession.page.goto(f"{GRAFANA_URL}/login")
  websession.page.get_by_placeholder("email or username").click()
  websession.page.get_by_placeholder("email or username").fill(GRAFANA_USERNAME)
  websession.page.get_by_placeholder("password").click()
  websession.page.get_by_placeholder("password").fill(GRAFANA_PASSWORD)
  websession.page.get_by_label("Login button").click()
  time.sleep(1)

  return websession

if __name__ == '__main__':

  with sync_playwright() as playwright:
    websession = WebSession(playwright)
    websession = login(websession)
