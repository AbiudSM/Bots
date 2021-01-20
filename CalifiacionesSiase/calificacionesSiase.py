from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.ui import Select
import pandas as pd
import os

try:
	with open('data.txt', 'r') as fname:
		data = list()
		for line in fname:
			splitLine = line.split(":")
			data.append(splitLine)
		
		matricula = data[0][1].strip()
		password = data[1][1].strip()

		fname.close()


	# path to chromedriver
	driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")

	os.system('cls')
	print("Cargando...")


	#driver.maximize_window()
	driver.set_window_position(-10000,0)


	# get siase url
	driver.get("https://www.uanl.mx/enlinea/")


	# Log in
	driver.switch_to.frame('loginbox')

	driver.find_element_by_xpath('//*[@id="cuenta"]').send_keys(matricula)

	driver.find_element_by_xpath('//*[@id="pass"]').send_keys(password)

	logIn = driver.find_element_by_xpath("/html/body/div/form/fieldset/div[4]/button")
	logIn.click()

	# Open Siase
	enterNexus = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td/a/img')
	openSiase = driver.find_element_by_link_text('FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA - INGENIERO EN TECNOLOGIA DE SOFTWARE')

	actions = ac(driver)
	actions.move_to_element(enterNexus).move_to_element(openSiase).click().perform()

	# Move to frame left
	driver.switch_to.frame('left')

	# Open grades
	openGrades = driver.find_element_by_link_text('Calificaciones')
	openGrades.click()

	# Move to frame center
	driver.switch_to.default_content()
	driver.switch_to.frame('center')

	# Open specific grades
	select = Select(driver.find_element_by_xpath('/html/body/form/table[1]/tbody/tr[1]/td[1]/select'))
	select.select_by_index('1')
	driver.find_element_by_xpath('/html/body/form/table[3]/tbody/tr[2]/td/input').click()

	# Get grades
	allGrades = driver.find_elements_by_css_selector('body > form > table > tbody > tr')
	numerGrades = len(allGrades) - 8

	grades = list() 
	subjects = list() 
	subjectstype = list()

	i = 2
	suma = 0
	divSuma = 0

	for _ in range(numerGrades):
		grade = driver.find_element_by_css_selector("body > form > table:nth-child(7) > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(6) > div > p > font > b")
		grades.append(grade.text)

		subject = driver.find_element_by_css_selector("body > form > table:nth-child(7) > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(2) > div > p > font > b")
		subjects.append(subject.text)

		subjectype = driver.find_element_by_css_selector("body > form > table:nth-child(7) > tbody > tr:nth-child(" + str(i) + ") > td:nth-child(3) > div > p > font > b")
		subjectstype.append(subjectype.text)

		if (grade != None) and (grade.text != " ") and (grade.text != "  "):
			suma = suma + int(grade.text)
			divSuma = divSuma + 1

		i = i + 1

	df = pd.DataFrame({'Tipo':subjectstype, 'Materia':subjects, 'Calificacion':grades}, index = list(range(1,numerGrades + 1)))

	os.system('cls')

	promedio = suma / divSuma
	print(df.to_string(index=False))
	print("\nPromedio: ",str(promedio))

	if promedio >= 97:
		print("\nProbablemente estes dentro del grupo los 100 de FIME :O")
	elif promedio >= 85:
		print("\nVas bien papu :D")
	elif promedio >= 75:
		print("\nPuedes mejorar :)")
	else:
		print("\nCambiate de carrera bro")
		
	driver.quit()

except Exception as e:
	print(e)
	print('\n\nPosible error: Agregar de manera correcta su matricula y contraseña al archivo "data.txt"')