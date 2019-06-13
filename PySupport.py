#iSupport Entry Automation - PySupport v1.2
#Written by Amogh Kulkarni on 6/12/19
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet
import getpass
path_prefix = 'C:\\Users\\akulkar5\\OneDrive - University of Toledo\\Desktop\\'
path_to_tag_file = path_prefix + 'tags.txt'
path_to_mac_file = path_prefix + 'macs.txt'
#decrypt pw
encrypted = "gAAAAABdAmOvcj0Y4RBDyqRoIRjr9aYmgUfZx2Q9lpZ_H_UenJ1_0CmA5Cqu_CY0ZSsyAsuLbjlLQ51RWO0rm5CADRmVzDGgNA=="
key = "rhvxGus7Id4wKVtcCRp-7w5BbVlSLS3aOUj_bldL" + getpass.getpass("Key suffix: ")
encoding = "utf-8"
cipher = Fernet(bytes(key, encoding))
to_decrypt = bytes(encrypted, encoding)
#get data(Tags and MACs) from their respective files
with open(path_to_tag_file) as tag_file:
    tags = tag_file.read().splitlines()
with open(path_to_mac_file) as mac_file:
    macs = mac_file.read().splitlines()
serial_mac_map = dict(zip(tags, macs))
print(serial_mac_map)
#login to isupport
user = "akulkar5"
driver = webdriver.Firefox()
print("Logging in...")
driver.get("https://ittech.utoledo.edu")
#wait(driver, 5).until(EC.alert_is_present())
alert = driver.switch_to_alert()
alert.send_keys(user + Keys.TAB + (cipher.decrypt(to_decrypt)).decode(encoding))
alert.accept()
#make asset
print("Creating asset...")
driver.get("https://ittech.utoledo.edu/Rep/Asset/Asset.aspx?AssetTypeID=2")
#asset fields
campus_input = "Health"
room_input = "0055"
dept_input = "IT Personnel("
modified_input = "AKULKAR5"
entry_tech_input = "AKULKAR5"
#date fields
date_created_input = "06/13/2019 12:00:00 AM"
date_modified_input = "06/13/2019 12:00:00 AM"
#loop from here
for serial in serial_mac_map:
    name_input = "UT" + serial
    tag_input = name_input
    serial_number = driver.find_element_by_id("uxTextBox_SerialNumber")
    name = driver.find_element_by_id("uxTextBox_Name")
    tag_number = driver.find_element_by_id("uxTextBox_TagNumber")
    campus = driver.find_element_by_id("uxTabsSection_uxCustomField_46")
    room = driver.find_element_by_id("uxTabsSection_uxCustomField_29")
    department = driver.find_element_by_id("uxTabsSection_uxCustomField_53")
    user_type_radiobtn = driver.find_element_by_xpath(".//input[@type='radio' and @value='Department']")
    multi_user_radiobtn = driver.find_element_by_xpath(".//input[@type='radio' and @value='YES']")
    modified = driver.find_element_by_id("uxTabsSection_uxCustomField_51")
    entry_tech = driver.find_element_by_id("uxTabsSection_uxCustomField_49")
    mac_wired = driver.find_element_by_id("uxTabsSection_uxCustomField_32")
    date_created = driver.find_element_by_id("uxTabsSection_uxCustomField_50")
    date_modified = driver.find_element_by_id("uxTabsSection_uxCustomField_52")
    #dropdowns
    building_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_27"))
    building_dropdown.select_by_visible_text('DOWLING HALL IDA MARIE')
    floor_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_28"))
    floor_dropdown.select_by_visible_text('Basement')
    dept_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_53"))
    dept_dropdown.select_by_visible_text('IT Personnel (105780)')
    purchase_type_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_116"))
    purchase_type_dropdown.select_by_visible_text('Department')
    mac_wired_input = serial_mac_map[serial]
    status_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_47"))
    status_dropdown.select_by_visible_text('Hold')
    manufacturer_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_54"))
    manufacturer_dropdown.select_by_visible_text('Dell')
    model_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_55"))
    model_dropdown.select_by_visible_text('Optiplex')
    model_type_dropdown = Select(driver.find_element_by_id("uxTabsSection_uxCustomField_56"))
    model_type_dropdown.select_by_visible_text('7460')
    #radio buttons
    driver.execute_script("arguments[0].click();", user_type_radiobtn)
    driver.execute_script("arguments[0].click();", multi_user_radiobtn)
    #fill input fields
    field_input_map = {date_created: date_created_input, serial_number: serial, name: name_input, tag_number: tag_input,
    mac_wired: mac_wired_input, date_modified: date_modified_input, campus: campus_input, room: room_input,
    modified: modified_input, entry_tech: entry_tech_input}
    print("Auto filling fields...")
    for field in field_input_map:
        field.send_keys(field_input_map[field] + Keys.ENTER)
    #new tab
    driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
    ## TODO: if not the last element in the dict
    print("Creating asset...")
    driver.get("https://ittech.utoledo.edu/Rep/Asset/Asset.aspx?AssetTypeID=2")
driver.close()
