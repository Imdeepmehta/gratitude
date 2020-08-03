from requests_html import HTMLSession
import sys
import json


def pypi_url(module_name):
	"""
	This will return the search result of a module
	on pypi.org website.
	"""
	return f"https://pypi.org/project/{module_name}/"



def convertJson(json_data):
	# json_data = {}
	# json_data[module_name] = contri_data
	data = {
    "name": "Gratitude",
    "children": [
        
    	]
	}

	for module_name, module_data in json_data.items():
		username_s = []
		for i in module_data:
			username_s.append({"name": i[0]})

		data['children'].append({
			'name': module_name,
			'children': username_s
		})
	

	data = json.dumps(data)
	# # Save the data into json formate
	with open("data_file.json", "w") as outfile:
   		json.dump(data,outfile)
	print("done data")

	return data


	




def findDev(github_url,session):
	token = '564541d8154b3e221a1e4d0d2e24b75e0f3c004a'
	Flag = 1
	data = []

	
	for i in range(1):
		if Flag == 1:
			contributer_api_url = f"https://api.github.com/repos/{github_url[19:]}/contributors?per_page=100&page={i+1}"
			print(contributer_api_url)
			headers = {'Authorization': f'token {token}'}
			r = session.get(contributer_api_url)
			print("Response Code:", r.status_code)

			for dev in r.json():
				if dev['login'] != None:
					# print("Contributor Name =>",dev['login'])
					# print("Contributer Image => ",dev['avatar_url'])
					# print("Contributer Profile => ",dev['html_url'])
					data.append([dev['login'],dev['avatar_url'],dev['html_url']])
				else:
					Flag = 0
		else:
			break
	return data




def start(module_name):
	print("BOT: STARTING SESSION ... ["+module_name+"]")
	session = HTMLSession()
	r = session.get(pypi_url(module_name))
	li_s = r.html.find("div.sidebar-section ul.vertical-tabs__list li a[rel='nofollow']", first=False)

	for li in li_s:
		if "github." in li.attrs['href'] and "issues" not in li.attrs['href']:
			github_url = li.attrs['href']
			break

	print("BOT: FETCHING GITHUB URL => ",github_url)
	print(f"BOT: FETCHING CONTRIBUTER =>{github_url[19:]}")
	contri_data = findDev(github_url,session)

	return contri_data




# module_name = ["pandas","numpy","matplotlib"]

def main(module_name):
	json_data = {}


	for mod_name in module_name:
		print("BOT: Let's Find the contributors of => ",{mod_name})
		datas = start(mod_name)
		json_data[mod_name] = datas


	print("BOT: Let's clean data for you")
	final_data = convertJson(json_data)
	print(final_data)
	return final_data


