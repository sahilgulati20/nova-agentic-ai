import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def enter_location_details(driver, nova_speak, nova_listen):
    wait = WebDriverWait(driver, 20)

    try:
        # 🚕 Step 1: Ask for Pickup Location
        nova_speak("Where should I pick you up from?")
        pickup_location = nova_listen()
        if not pickup_location:
            nova_speak("I didn't hear the pickup location.")
            return

        # Step 2: Click Pickup button
        pickup_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="pudo-button-pickup"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pickup_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", pickup_button)
        print("✅ Pickup button clicked!")

        # Step 3: Enter pickup location
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Pickup location"]'))
        )
        input_box.send_keys(pickup_location)
        print(f"✅ Pickup location entered: {pickup_location}")
        time.sleep(2)

        # Step 4: Select the first suggestion
        first_option = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="option"]'))
        )
        driver.execute_script("arguments[0].click();", first_option)
        print("✅ First pickup suggestion selected")

        # 🛬 Step 5: Ask for Destination
        nova_speak("Where are you going?")
        destination = nova_listen()
        if not destination:
            nova_speak("I didn't hear the destination.")
            return

        # Step 6: Enter destination
        time.sleep(1)
        destination_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Dropoff location"]'))
        )
        destination_box.send_keys(destination)
        print(f"✅ Destination entered: {destination}")
        time.sleep(2)

        # Step 7: Select the first destination suggestion
        dest_suggestion = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="option"]'))
        )
        driver.execute_script("arguments[0].click();", dest_suggestion)
        print("✅ Destination suggestion selected")

    except Exception as e:
        print("❌ Error in entering locations:", e)
        nova_speak("Something went wrong while entering the locations.")
