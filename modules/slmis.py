import math
from itertools import chain
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

import sys
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QModelIndex, QAbstractTableModel
import os


class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.percent = 0

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

        return None



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
        cache_path = os.path.join(os.getcwd(),'cache')
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : cache_path}
        chromeOptions.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(options=chromeOptions)
        self.driver.get("https://slmis.xu.edu.ph/")
    
    def init_sections(self):
        self.sections_dict = self.get_faculty_schedule()
        self.sections = [self.view_cleaner(i) for i in self.sections_dict.keys()]
    
    def view_cleaner(self, val):
        return val.replace("<br>\n"," ").replace("   "," ")
        
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

    def check_if_loaded(self,by, filter, timeout=10):
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
            WebDriverWait(self.driver, timeout).until(element_present)
            print("found element", filter)
        except TimeoutException:
            print("Took too long to load")
            raise TimeoutException
    def get_faculty_schedule(self):
        """
        Retrieves the faculty schedule from the SLMIS website.

        This function navigates to the faculty center page and retrieves the teaching schedule. It uses Selenium WebDriver to interact with the website.

        Returns:
            courses_dictionary (dict): A dictionary containing the course names as keys and the corresponding table rows as values.
        """
        self.go_to_home_page()
        #Click on Self Service
        self.check_if_loaded(By.XPATH, '//*[@id="fldra_CO_EMPLOYEE_SELF_SERVICE"]')
        self_service = self.driver.find_element(By.XPATH, '//*[@id="fldra_CO_EMPLOYEE_SELF_SERVICE"]')
        self_service.click()
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
            self.check_if_loaded(By.XPATH, '//*[@id="userid"]')
            user_element = self.driver.find_element(By.XPATH, '//*[@id="userid"]')
            pass_element = self.driver.find_element(By.XPATH, '//*[@id="pwd"]')
            #With ctrl A
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

    def click_gradebook(self, val):
        """
        Clicks the gradebook button for a given section.

        Args:
            val (int): The index of the section in the `all_sections_dict` dictionary.

        Returns:
            None

        Raises:
            IndexError: If the `val` is out of range of the `all_sections_dict` keys.

        This function retrieves the `all_sections_dict` dictionary by calling the `get_faculty_schedule` method.
        It then retrieves the `current_row` by indexing the `all_sections_dict` dictionary with the `val` parameter.
        The function searches for the first element in `current_row` that has an `id` attribute containing the string 'GRADEBOOK'.
        It clicks on this element.
        """
        all_sections_dict = self.get_faculty_schedule()
        current_row = all_sections_dict[list(all_sections_dict.keys())[val]]
        [i for i in current_row.find_elements(By.TAG_NAME, "a") if 'GRADEBOOK' in i.get_attribute('id')][0].click()
        
    def get_no_pages(self, gradebook_no):
        self.click_gradebook(gradebook_no)
        
        page_no = 1
        while True:
            try:
                #Switching to default content
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.driver.find_element(By.NAME, "TargetContent"))
                time.sleep(0.5)
                next_bttn_element = self.driver.find_element(By.XPATH, '//a[@name="DERIVED_LAM_RIGHT_MOVE"]')
                print("found next button", next_bttn_element.get_attribute('innerHTML'))
                next_bttn_element.click()
                page_no += 1
                time.sleep(0.5)
            except StaleElementReferenceException:
                print("StaleElementReferenceException")
                break
            except NoSuchElementException:
                print("NoSuchElementException")
                break
            
        return page_no
    
    def generate_headers(self, gradebook_no):
        pages_no = self.get_no_pages(gradebook_no)
        self.click_gradebook(gradebook_no)

        all_desc = []
        print(f"preparing {pages_no} pages")
        for i in range(pages_no):
            self.driver.switch_to.default_content()
            self.check_if_loaded(By.NAME, "TargetContent")
            self.driver.switch_to.frame(self.driver.find_element(By.NAME, "TargetContent"))
            #Going to faculty center
            time.sleep(1)
            desc = [i.get_attribute("innerHTML") for i in self.driver.find_elements(By.TAG_NAME, 'span') if "DERIVED_LAM_ASSIGNMENT_DESCR" in i.get_attribute("id")]
            all_desc.append(desc)

            if i != pages_no - 1:
                print("Next page")
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.driver.find_element(By.NAME, "TargetContent"))
                table = self.driver.find_element(By.XPATH, '//table[@role="presentation"]')
                self.check_if_loaded(By.XPATH, '//table[@role="presentation"]')
                next_bttn_element = table.find_element(By.XPATH, '//a[@name="DERIVED_LAM_RIGHT_MOVE"]')
                next_bttn_element.click()

        return all_desc
    def formatter(self, file_path: str, out_path: str):
        try:
            df = pd.read_csv(file_path, encoding='latin-1', encoding_errors='ignore')
        
        except pd.errors.ParserError:   #Error handling for csv with multiple delimiter (Specifically for name with a comma)
            with open(f"{file_path}", 'r', encoding='latin-1') as f:
                #Finds the lines with different lengths and saves their index
                lengths = []
                all_lines = f.readlines()
                all_lines = [i.removesuffix('\n') for i in all_lines]
                for i in all_lines[1:]:
                    lengths.append(len(i.split(',')))
                mode_length = max(set(lengths), key=lengths.count)
                idx_modify = [i-1 for i in lengths if i != mode_length]

                #Gets all the data and removes the 2nd element for the lines with differing lengths
                new_csv = []
                for idx,i in enumerate(all_lines):
                    if idx in idx_modify:
                        val = i.split(',')
                        popped = val.pop(1) #Removes 2nd element and merges to the first (deals with names like "DelaCruz, Jr" which has a comma)
                        val[0] = val[0] + ' ' + popped
                        new_csv.append(','.join(val))
                    else:
                        new_csv.append(i)

            #Saves the cleaned csv
            with open(f"{file_path}", 'w') as f:
                for i in new_csv:
                    f.write(f"{i}\n")
            df = pd.read_csv(f"{file_path}", encoding='latin-1', encoding_errors='ignore')
                
        df['Names'] = df[['Last Name', 'First Name']].apply(lambda x: ','.join(x), axis=1)
        col_names = df.columns.to_list()
        col_names = col_names[-1:] + col_names[:-1]
        df = df[col_names]
        df.drop(columns=['First Name', 'Last Name','Student ID'], inplace=True)
        df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        df.to_excel(out_path, index=False)

    def generate_template(self, gradebook_no):
        """
        Generates a template Excel file with empty columns for each assignment description in the specified gradebook.

        Args:
            gradebook_no (int): The number of the gradebook to generate the template for.

        Returns:
            None

        Raises:
            None

        Side Effects:
            Creates an Excel file with the name specified by `self.sections[gradebook_no]` in the current directory.

        """
        #Delete all files in cache first
        to_delete = []
        for i in os.listdir('cache'):
            if 'csv' in i:
                to_delete.append(os.path.join('cache', i))
        for i in to_delete:
            os.remove(i)

        self.click_gradebook(gradebook_no)
        self.driver.switch_to.default_content()
        self.check_if_loaded(By.NAME, "TargetContent")
        self.driver.switch_to.frame(self.driver.find_element(By.NAME, "TargetContent"))
        print('Switched to TargetContent')
        self.check_if_loaded(By.XPATH, '//*[@id="DERIVED_LAM_EXPORT"]')
        export_button = self.driver.find_element(By.XPATH, '//*[@id="DERIVED_LAM_EXPORT"]')
        export_button.click()

        time.sleep(1)


        file_path = None
        for i in os.listdir('cache'):
            if 'csv' in i:
                file_path = i
                break
        if file_path == None:
            print('No File Found')
            return False
        
        file_path = os.path.join('cache', file_path)
        out_path = f"{self.sections[gradebook_no]}.xlsx"
        self.formatter(file_path, out_path=out_path)
        os.remove(file_path)
        return out_path

        

    def grade(self, df, gradebook_no):
        self.click_gradebook(gradebook_no)

        def set_grade(grade, name):
                    ActionChains(self.driver) \
                    .click(self.driver.find_element(By.ID, name)) \
                    .key_down(Keys.CONTROL) \
                    .send_keys("a") \
                    .key_up(Keys.CONTROL) \
                    .send_keys(f"{round(grade,2)}")\
                    .click(self.driver.find_element(By.ID, name)) \
                    .key_down(Keys.CONTROL) \
                    .send_keys("a") \
                    .key_up(Keys.CONTROL) \
                    .send_keys(f"{round(grade,2)}")\
                    .perform()

        for i in range(math.ceil(df.shape[1]/2)):
            print(f"on page:",i)
            saved_df = df.iloc[:,i*7+1:1+(i+1)*7]
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_element(By.NAME, "TargetContent"))
            self.check_if_loaded(By.XPATH, '//table[@role="presentation"]')
            table = self.driver.find_element(By.XPATH, '//table[@role="presentation"]')
            self.check_if_loaded(By.XPATH , '//input[@type="text"]')
            time.sleep(0.5)
            inputs = self.driver.find_elements(By.XPATH , '//input[@type="text"]')
            element_names = [i.get_attribute("id") for i in inputs if "DERIVED_LAM_GRADE" in i.get_attribute("id")]

            
            for name in tqdm(element_names):
                try:
                    col, row = [int(i) for i in name[18:].split('$')]
                    col = col-1
                    grade = saved_df.iloc[row, col]
                    
                    if pd.isna(grade):
                        grade = 0
                    if float(f"{round(grade,2)}") == float(self.driver.find_element(By.ID, name).get_attribute("value")):
                        continue

                    set_grade(grade, name)

                    grade_element = self.driver.find_element(By.ID, name)
                    #Check if the value is the same
                    if grade_element.get_attribute("value") != f"{round(grade,2)}":
                        set_grade(grade, name)

                    
                except StaleElementReferenceException:
                    print("StaleElementReferenceException")
                    time.sleep(1)
                    set_grade(grade, name)
            try:
                next_bttn_element = self.driver.find_element(By.XPATH, '//a[@name="DERIVED_LAM_RIGHT_MOVE"]')
                print("found next button", next_bttn_element.get_attribute('innerHTML'))
                next_bttn_element.click()
            except NoSuchElementException:
                
                print("Grade Finished. Please check before submitting.")
                break

            print("Successfully imported all final grades.\n Please click on save")
        
    def close(self):
        self.driver.quit()
