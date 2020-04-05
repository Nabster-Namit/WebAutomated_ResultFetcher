from selenium import webdriver
from captcha_solver import CaptchaSolver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from pandas import Series, DataFrame
from io import BytesIO
import pytesseract
from PIL import Image
import numpy as np

def main():

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    Result_CSV = pd.read_csv(r'C:\Users\namit\Desktop\Result.csv')
    Class_dataFrame = DataFrame(Result_CSV)

    # DataFrame for class result list
    # for i in range (0,100):
    #     name_text = i
    #     enroll_text = i
    #     sgpa_text = i
    #     cgpa_text = i
    #     Result = Series(name_text,enroll_text,sgpa_text,cgpa_text)
    #     Class_dataFrame = DataFrame(Result, columns=['Name','Enrollment','SGPA','CGPA'])
    #     Class_dataFrame = DataFrame(np.arrange(400).reshape(100,4),index=[],columns=['Name','Enrollment','SGPA','CGPA'])
    #     Class_dataFrame = DataFrame({'Name':[name_text],'Enrollment':[eroll_text],'SGPA':[sgpa_text],'CGPA':[cgpa_text]})


    ## getting to result page
    driver = webdriver.Chrome()
    driver.get("http://result.rgpv.ac.in/result/ProgramSelect.aspx")
    prog_select = driver.find_element_by_xpath('//*[@id="radlstProgram_1"]')
    prog_select.click()
    time.sleep(2)


    x = Class_dataFrame['Enrollment'].max()
    x = '%003d' %x
    i = int(x[-3:])

    # captcha_id = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_pnlCaptcha"]/table/tbody/tr[1]/td/div/img')
    # solver = CaptchaSolver('browser')
    # raw_data = open('captcha.png', 'rb').read()
    # print(solver.solve_captcha(raw_data))

    ##loop for results
    while i < 100:
        Result_CSV = pd.read_csv(r'C:\Users\namit\Desktop\Result.csv')
        Class_dataFrame = DataFrame(Result_CSV)
        x = Class_dataFrame['Enrollment'].max()
        x = '%003d' % x
        i = int(x[-3:]) + 1
        enrollment_id = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtrollno"]')
        sem_id = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_drpSemester"]')
        get_result = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnviewresult"]')
        captcha_id = driver.find_element_by_xpath(
            '//*[@id="ctl00_ContentPlaceHolder1_pnlCaptcha"]/table/tbody/tr[1]/td/div/img')
        captcha_text_id = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_TextBox1"]')
        location = {'x': 300, 'y': 352}
        size = {'width': 700, 'height': 75}
        # locationRR = captcha_id.location
        # sizeRR = captcha_id.size
        # print (locationRR)
        # print(sizeRR)
        captcha_screenshot = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(captcha_screenshot))  # uses PIL library to open image in memory

        im.save('captcha_original.png')
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        select = Select(sem_id)
        select.select_by_visible_text('3')
        enrollment = '0103EC181' + '%003d' % int(i)
        enrollment_id.send_keys(enrollment)

        captcha = im.crop((left, top, right, bottom))  # defines crop points
        captcha.save('captcha.png')  # saves new cropped image
        img = Image.open(r"C:\Users\namit\PycharmProjects\LearningPython\captcha.png")
        # print(img)
        text = pytesseract.image_to_string(img).upper()
        filteredChars = ''.join((filter(lambda x: x in ['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'], text)))
        # print(text.upper())

        captcha_text_id.send_keys(filteredChars.upper())
        time.sleep(3)
        get_result.click()
        time.sleep(5)
        if 'EC' == driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblBranchGrading"]').text :
            enroll_text = '%00d' % int(i)
            #enroll_text = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_pnlGrading"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[4]').text
            name_text = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblNameGrading"]').text
            sgpa_text = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblSGPA"]').text
            cgpa_text = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblcgpa"]').text
            Result_Series = [name_text, enroll_text, sgpa_text, cgpa_text]
            # Class_dataFrame = DataFrame(Result_Series, columns=['Name', 'Enrollment', 'SGPA', 'CGPA'])
            Class_dataFrame.loc[i] = Result_Series
            Class_dataFrame.to_csv(r'C:\Users\namit\Desktop\Result.csv', index=False)
            # Result_Series = ([name_text,enroll_text,sgpa_text,cgpa_text],index = ['Name','Enrollment','SGPA','CGPA'])
            backButton = driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div/div[2]/table/tbody/tr[2]/td/a')
            backButton.click()
            prog_select = driver.find_element_by_xpath('//*[@id="radlstProgram_1"]')
            prog_select.click()
            time.sleep(2)
        else :
            main()
main()



