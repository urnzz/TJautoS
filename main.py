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
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listagemDeProcessos"]')))
                t=driver.find_element(By.XPATH, '//*[@id="listagemDeProcessos"]')
                lists = t.find_elements(By.TAG_NAME, "ul")
                for list in lists:
                    rows = list.find_elements(By.TAG_NAME, 'li')
                    n=-1
                    enc=False
                    for row in rows:
                        n+=1
                        if "Cumprimento de sentença" in str(row.find_element(By.CLASS_NAME, "classeProcesso").text):
                            if '2019' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text) or '2020' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text) or '2021' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text) or '2022' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text):
                                print('encontrado quinquenio')
                                o.write(cpf.strip()+", QUINQUENIO:"+row.find_element(By.CLASS_NAME, "linkProcesso").text+"\n")
                                enc=True
                            elif '2011' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text):
                                print('encontrado sexta-parte')
                                o.write(cpf.strip()+", SEXTA-PARTE:"+row.find_element(By.CLASS_NAME, "linkProcesso").text+"\n")
                                enc=True
                            elif '2005' in str(row.find_element(By.CLASS_NAME, "linkProcesso").text):
                                print('encontrado quinquenio')
                                o.write(cpf.strip()+", QUINQUENIO:"+row.find_element(By.CLASS_NAME, "linkProcesso").text+"\n")
                                enc=True
                            elif n == len(rows) and enc==False:
                                o.write(cpf.strip()+",sem processo\n")
                                print("sem processo") 
                        else:
                            if n == len(rows) and enc==False:
                                o.write(cpf.strip()+",sem processo\n")
                                print("sem processo") 
            except:
                o.write(cpf.strip()+",so 1 proc\n")
                print("so 1 proc") 
        except:
            o.write(cpf.strip()+",erro\n")
            print('erro encontrado, pulando cpf: '+cpf)
            pass

if __name__ == '__main__':
    main()