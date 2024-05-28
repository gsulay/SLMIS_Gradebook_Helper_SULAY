from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException


class SLMISHandler:
    def __init__(self):
        """
        Initializes a new instance of the class.

        This constructor initializes the `driver` attribute of the class by creating a new instance of the `Chrome` webdriver.

        Parameters:
            None

        Returns:
            None
        """
        self.driver = webdriver.Chrome()
        
    def go_to_home_page(self):
        """
        Navigates the webdriver to the home page of the SLMIS website.

        This function uses the `driver` attribute of the class to navigate to the specified URL.
        The URL is the home page of the SLMIS website, which is located at:
        "https://slmis.xu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=CO_EMPLOYEE_SELF_SERVICE&amp;FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE&amp;IsFolder=true".

        Parameters:
            self (SLMISHandler): The instance of the SLMISHandler class.

        Returns:
            None
        """
        self.driver.get("https://slmis.xu.edu.ph/psp/ps/EMPLOYEE/HRMS/s/WEBLIB_PTPP_SC.HOMEPAGE.FieldFormula.IScript_AppHP?pt_fname=CO_EMPLOYEE_SELF_SERVICE&amp;FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE&amp;IsFolder=true")

    def check_if_loaded(self,by, filter):
        """
        Check if an element is loaded on the webpage.

        This function uses Selenium's WebDriverWait to wait for an element to be present on the webpage. It takes in two parameters:
        - `by`: a Selenium By locator that specifies how to find the element.
        - `filter`: a string that specifies the value of the locator.

        The function tries to find the element using the specified locator and filter. If the element is found within 10 seconds, the function returns without raising an exception. If the element is not found within 10 seconds, a TimeoutException is raised and a message is printed to the console.

        Parameters:
            by (By): A Selenium By locator that specifies how to find the element.
            filter (str): A string that specifies the value of the locator.

        Returns:
            None

        Raises:
            TimeoutException: If the element is not found within 10 seconds.
        """
        try:    
            element_present = EC.presence_of_element_located((by, filter))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            print("Took too long to load")
    def get_faculty_schedule(self):
        """
        Retrieves the faculty schedule from the SLMIS website.

        This function navigates to the faculty center page and retrieves the teaching schedule. It uses Selenium WebDriver to interact with the website.

        Returns:
            courses_dictionary (dict): A dictionary containing the course names as keys and the corresponding table rows as values.
        """
        self.go_to_home_page()
        #Going to faculty center
        self.check_if_loaded(By.XPATH, '//*[@id="ptifrmtgtframe"]')
        faculty_center = self.driver.find_element(By.XPATH, '//*[@id="ptifrmtgtframe"]')
        self.driver.switch_to.frame(faculty_center)
        faculty_center_button = self.driver.find_element(By.XPATH, '//*[@id="ptppscappnavtbl"]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr[2]/td/ul/li[1]/a')
        faculty_center_button.click()
        self.driver.switch_to.default_content()
        #Techhing schedule
        self.check_if_loaded(By.XPATH, '//*[@id="ptifrmtgtframe"]')
        teaching_schedule = self.driver.find_element(By.XPATH, '//*[@id="ptifrmtgtframe"]')
        self.driver.switch_to.frame(teaching_schedule)
        main_table = self.driver.find_element(By.XPATH,'//*[@id="INSTR_CLASS_VW$scroll$0"]/tbody/tr[1]/td/table')
        all_rows = main_table.find_elements(By.TAG_NAME, "tr")

        r = all_rows[1]
        courses_dictionary = {}
        for r in tqdm(all_rows):
            all_cells = r.find_elements(By.TAG_NAME, "td")
            #Get the name of the course

            for cell in all_cells:
                try:
                    cell_element = cell.find_element(By.TAG_NAME, "span")
                    if "CLASS_TIT" in cell_element.get_attribute('id'):
                        course_element = cell_element.find_element(By.TAG_NAME, "a")
                        course_name = course_element.get_attribute('innerHTML')
                        courses_dictionary[course_name] = r
                except NoSuchElementException:
                    continue
        return courses_dictionary

    def authentication(self, username, password):
        """
        Authenticates the user by entering the provided username and password into the login form.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the authentication is successful, False otherwise.

        Raises:
            NoSuchElementException: If the login form elements are not found.
        """
        try:
            user_element = self.driver.find_element(By.XPATH, '//*[@id="userid"]')
            pass_element = self.driver.find_element(By.XPATH, '//*[@id="pwd"]')
            ActionChains(self.driver) \
                .click(user_element) \
                .key_down(Keys.CONTROL) \
                .send_keys("a") \
                .key_up(Keys.CONTROL) \
                .send_keys(username)\
                .click(pass_element) \
                .key_down(Keys.CONTROL) \
                .send_keys("a") \
                .key_up(Keys.CONTROL) \
                .send_keys(password)\
                .key_down(Keys.ENTER) \
                .perform()
            
            if "errorCode" in self.driver.current_url:
                print("Authentication Failed")
                return False
            return True
        except NoSuchElementException:
            print("Already Logged in")
        