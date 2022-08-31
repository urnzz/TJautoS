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
            print("pesquisando no TJ "+cpf.strip())
            url='https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=DOCPARTE&dadosConsulta.valorConsulta={}&cdForo=-1'
            driver.get(url.format(cpf))
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listagemDeProcessos"]')))
                t=driver.find_element(By.XPATH, '//*[@id="listagemDeProcessos"]')
                lists = t.find_elements(By.TAG_NAME, "ul")
                numQ=''
                numS=''
                for list in lists:
                    rows = list.find_elements(By.TAG_NAME, 'li')
                    n=-1
                    enc=False
                    numQ=''
                    numS=''
                    for row in rows:
                        n+=1
                        if "Cumprimento de sentença" in str(row.find_element(By.CLASS_NAME, "classeProcesso").text):
                            if '2019' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text) or '2020' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text) or '2021' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text) or '2022' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text):
                                print('encontrado quinquenio')
                                enc=True
                                numQ=row.find_element(By.CLASS_NAME, "linkProcesso").text
                            elif '2011' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text):
                                print('encontrado sexta-parte')
                                enc=True
                                numS=row.find_element(By.CLASS_NAME, "linkProcesso").text
                            elif '2005' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text):
                                print('encontrado quinquenio')
                                enc=True
                                numQ=row.find_element(By.CLASS_NAME, "linkProcesso").text
                            elif n == len(rows) and enc==False:
                                print("sem processo") 
                        else:
                            if n == len(rows) and enc==False:
                                print("sem processo") 
                o.write(cpf.strip()+','+numQ+','+numS+'\n')
            except:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/span[1]')))
                num = list.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/span[1]').text
                numQ=''
                numS=''
                enc=False
                if '2005' in num:
                    print('encontrado quinquenio')
                    enc=True
                    numS=num
                elif '2011' in num:
                    print('encontrado sexta-parte')
                    enc=True
                    numS=num
                elif '2019' in num or '2020' in num or '2021' in num or '2022' in num:
                    print('encontrado quinquenio')
                    enc=True
                    numQ=num
                else:
                    print("sem processo")
                if enc==True:
                    o.write(cpf.strip()+','+numQ+','+numS+'\n')
        except:
            o.write(cpf.strip()+",erro\n")
            print('erro encontrado, pulando cpf: '+cpf)
            pass

if __name__ == '__main__':
    main()