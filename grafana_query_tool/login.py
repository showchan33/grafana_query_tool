from playwright.sync_api import sync_playwright
import os, time
from dotenv import load_dotenv
from websession.websession import WebSession

def login(
  websession: WebSession,
  grafana_version: str,
  env_file: str = ".env",
) -> WebSession:

  load_dotenv(env_file)

  grafana_username = os.getenv('GRAFANA_USERNAME')
  grafana_password = os.getenv('GRAFANA_PASSWORD')
  grafana_url = os.getenv('GRAFANA_URL')

  print(f"Attempting to login to {grafana_url}.")

  websession.page.goto(f"{grafana_url}/login")
  websession.page.get_by_placeholder("email or username").click()
  websession.page.get_by_placeholder("email or username").fill(grafana_username)
  websession.page.get_by_placeholder("password").click()
  websession.page.get_by_placeholder("password").fill(grafana_password)
  if grafana_version == "10.1":
    websession.page.get_by_label("Login button").click()
  else:
    websession.page.get_by_test_id("data-testid Login button").click()
  time.sleep(1)

  return websession

def logout(
  websession: WebSession,
) -> WebSession:

  print(f"Currently logged out.")

  grafana_url = os.getenv('GRAFANA_URL')
  websession.page.goto(f"{grafana_url}/logout")

  return websession

if __name__ == '__main__':

  with sync_playwright() as playwright:
    websession = WebSession(playwright)
    websession = login(websession)
