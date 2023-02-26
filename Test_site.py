
from faker import Faker
from selenium import webdriver
from BaseClass import generate_random_number, generate_random_text
from selenium.webdriver.common.by import By
import string
import random
import pytest
import time
import pyautogui

fake = Faker()

firstname = fake.first_name()
lastname = fake.last_name()
email_ = fake.email()
characters = list(string.ascii_lowercase)


@pytest.fixture()
def setup_Web_Driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def random_date():
    """
    Fixture that generates a random date in the yy/mm/dd format
    """
    """
        Fixture that generates a random date in the yyyy-mm-dd format
        """
    return fake.date_object().strftime('%Y-%m-%d')


def test_register_candidate(setup_Web_Driver):
    driver = setup_Web_Driver
    driver.maximize_window()

    # navigate to the registration page
    driver.get("https://automations.elevatus.io/register")
    time.sleep(1)
    # Accept cookies Popup :
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/button[1]").click()
    # find the input fields and fill in the details
    # Enter First and Last Name :
    first_name = driver.find_element(By.NAME, "firstName")
    first_name.send_keys(firstname)

    last_name = driver.find_element(By.NAME, "lastName")
    last_name.send_keys(lastname)

    # Enter Email
    email = driver.find_element(By.NAME, "email")
    email.send_keys(email_)

    # Enter Password and Confirmation :
    password = driver.find_element(By.NAME, "password")
    password.send_keys("Mypassword123@")
    confirm_password = driver.find_element(By.NAME, "confirmPassword")
    confirm_password.send_keys("Mypassword123@")

    # Enter Phone number :
    phone_number = driver.find_element(By.XPATH, "//*[@id='SharedPhoneControlRef--0---0-0-phone_number']")
    RandomNumber = generate_random_number()
    phone_number.send_keys(RandomNumber)

    # check the checkbox
    checkbox = driver.execute_script("return document.querySelector('#customCheckLogin')")
    # click the checkbox to check it
    driver.execute_script("arguments[0].click();", checkbox)

    # assert that the checkbox is checked
    assert checkbox.is_selected()

    # scroll down to the submit_button
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # identify element at page end
    submit_Btn = driver.find_element(By.XPATH, "//*[@id='__next']/div/div/div/div[1]/div/form/div[8]/button")
    assert checkbox.is_selected()
    # Click on Submit button :
    driver.execute_script("arguments[0].click()", submit_Btn)
    # Print All values:
    print("\nFirst name is " + firstname)
    print("\nLast name is " + lastname)
    print("\nemail" + email_)
    print("\nPhone number: " + RandomNumber)
    time.sleep(5)
    # Assert on Sucess Page :
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    assert 'Registered successfully' in body_text
    assert 'Follow the instructions sent to your email to complete your registration' in body_text

def test_Login(setup_Web_Driver,random_date):
    driver = setup_Web_Driver
    driver.maximize_window()

    # navigate to the registration page
    driver.get("https://automations.elevatus.io/login")
    time.sleep(1)
    # Accept cookies Popup :
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/button[1]").click()
    # enter the username
    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys("test@test.com")
    # enter the password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("Talal123@")
    # submit the form
    login_button = driver.find_element(By.XPATH, "//*[@id='__next']/div/div/div/div[1]/div/form/div[4]/button")
    driver.execute_script("arguments[0].click()", login_button)
    # verify that the user is logged in
    time.sleep(3)

    #build CV manually will be added in to a test case after figure out how to verfy email
    driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[2]/div[3]/button").click()
    time.sleep(2)

    #decription:
    description_field = driver.find_element(By.ID,"description")
    description_field.send_keys(generate_random_text(characters, 100))
    #Fill Random Date of birth:
    dateOfBirth_field = driver.find_element(By.ID,"date-picker-dialog")
    dateOfBirth_field.send_keys(random_date)
    #############
    #Fill Gender:
    Gender=driver.find_element(By.NAME,"gender")
    Gender.click()
    time.sleep(2)
    gender_choice = ["#gender-option-1", "#gender-option-0"]
    random_string = random.choice(gender_choice)
    assert random_string in gender_choice
    driver.find_element(By.CSS_SELECTOR, "{}".format(random_string)).click()

    # Nationality :
    nationality = driver.find_element(By.NAME, "nationality")
    nationality.click()
    time.sleep(2)
    nationality__choice = ["#nationality-option-0", "#nationality-option-0",
                           "#nationality-option-0"]
    random_nationality = random.choice(nationality__choice)
    driver.find_element(By.CSS_SELECTOR, "{}".format(random_nationality)).click()
    time.sleep(3)



    #fill address
    address_field = driver.find_element(By.ID, "address")
    address_field.send_keys(generate_random_text(characters, 20))
    time.sleep(3)

    #fill City

    city_field = driver.find_element(By.ID, "city")
    city_field.send_keys(generate_random_text(characters, 10))
    time.sleep(3)

    #Fill country :

    location=driver.find_element(By.NAME,"location.country_uuid")
    location.click()
    time.sleep(2)
    country__choice = ["location.country_uuid-option-0", "location.country_uuid-option-1","location.country_uuid-option-2","location.country_uuid-option-3"]
    random_country= random.choice(country__choice)
    driver.find_element(By.ID,"{}".format(random_country)).click()
    time.sleep(3)

    #Scroll to CV :
    link = driver.find_element(By.ID,"job_types")
    # Execute JavaScript to scroll to the element
    driver.execute_script("arguments[0].scrollIntoView();", link)

    time.sleep(3)
    file_path = "pdf-test.pdf"
    cv_input = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div/div[12]/div/div/div")
    cv_input.click()
    cv_input.send_keys(file_path)
    pyautogui.PAUSE = 1

    # Move the mouse to the center of the screen to avoid accidentally clicking other elements
    pyautogui.moveTo(pyautogui.size()[0] / 2, pyautogui.size()[1] / 2)

    # Click the address bar to give it focus
    pyautogui.click(325, 105)

    # Type the file path into the address bar and press Enter
    pyautogui.write(file_path)
    pyautogui.press("enter")

    # Wait for the file to be uploaded
    pyautogui.PAUSE = 5
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)




def test_applyJob(setup_Web_Driver,random_date):
        driver = setup_Web_Driver
        driver.maximize_window()

        # navigate to the registration page
        driver.get("https://automations.elevatus.io/login")
        time.sleep(1)
        # Accept cookies Popup :
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/button[1]").click()
        # enter the username
        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys("test@test.com")
        # enter the password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("Talal123@")
        # submit the form
        login_button = driver.find_element(By.XPATH, "//*[@id='__next']/div/div/div/div[1]/div/form/div[4]/button")
        driver.execute_script("arguments[0].click()", login_button)
        # verify that the user is logged in
        time.sleep(3)
        driver.get("https://automations.elevatus.io/")
        time.sleep(1)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[2]/div[3]/a/button").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div[2]/div/div/div/div/div/div[4]/button").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div[2]/div/div[7]/button").click()

        time.sleep(5)
