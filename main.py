import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    f = open("cpfs.txt", "r")
    cpfs = f.readlines()
    o = open('output.txt', 'w+')
    options = uc.ChromeOptions()
    options.headless=True
    driver = uc.Chrome(options=options)
    for cpf in cpfs:
        try:
            print("pesquisando no PJE "+cpf.strip())
            driver.get("https://www.google.com/search?client=firefox-b-d&q=consulta+pje")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")))
            gs = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/a/h3")
            gs.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')))
            cpfC = driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')
            cpfC.click()
            cpfC.clear()
            cpfC.send_keys(cpf.strip())
            driver.find_element(By.XPATH, '//*[@id="fPP:searchProcessos"]').click()
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody/tr')))
                t=driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/form/div[2]/div/table/tbody')
                rows = t.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    if "teto" in str(row.find_element(By.CLASS_NAME, "btn-block").text):
                        print('encontrado')
                        o.write(cpf.strip()+","+row.find_element(By.CLASS_NAME, "btn-block").text+"\n")
                        break
                    else:
                        if "Teto" in str(row.find_element(By.CLASS_NAME, "btn-block").text):
                            print('encontrado')
                            o.write(cpf.strip()+","+row.find_element(By.CLASS_NAME, "btn-block").text+"\n")
                            break
                        else:
                            raise Exception('') 
            except:
                o.write(cpf.strip()+",\n")
                print("sem processo de teto") 
        except:
            o.write(cpf.strip()+",erro\n")
            print('erro encontrado, pulando cpf: '+cpf)
            pass

if __name__ == '__main__':
    main()