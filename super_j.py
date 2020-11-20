import requests
from terminaltables import AsciiTable



def creating_table(info, title):
    table_info = [["languages", "vacancies_found", "vacancies_processed", "average_salary"]]
    for vacancie in info:
        table_info.append([vacancie, info[vacancie]["vacancies_found"], info[vacancie]["vacancies_processed"], info[vacancie]["average_salary"]])
    table = AsciiTable(table_info, title)
    return table.table


def predict_salary(from_salary, to_salary):
    if from_salary and to_salary:
        return (from_salary + to_salary) / 2
    elif not from_salary:
        return to_salary * 0.8
    elif not to_salary:
        return from_salary * 1.2


def predict_rub_salary_sj(vacancie):
    if vacancie["currency"] == "rub" and vacancie["payment_from"] != 0 and vacancie["payment_to"] != 0:
        return predict_salary(vacancie["payment_from"], vacancie["payment_to"])


headers = {"X-Api-App-Id": "v3.h.3969469.05b92e1fe4e00b35711d249709174f06dc4bde24.fd893b9db5354288d7028c8be578ecd46699f697"}
answer = {}
languages = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "CSS", "C#"]
for lang in languages:
    sum_salary = 0
    vacancies_processed = 0
    payload = {"town": 4,
               "catalogues": 48,
               "keyword": lang}
    hh_url = "https://api.superjob.ru/2.0/vacancies/"
    response = requests.get(hh_url, params=payload, headers=headers)
    response.raise_for_status()
    for page in range(response.json()["total"] // 20 + 1):
        payload = {"town": 4,
                   "catalogues": 48,
                   "keyword": lang,
                   "page": page}
        response = requests.get(hh_url, params=payload, headers=headers)
        response.raise_for_status()
        for vacancie in response.json()["objects"]:
            salary = predict_rub_salary_sj(vacancie)
            if salary:
                sum_salary += salary
                vacancies_processed += 1
    if vacancies_processed != 0:
        average_salary = int(sum_salary / vacancies_processed)
    else:
        average_salary = None
    answer[lang] = {"vacancies_found": response.json()["total"],
                   "vacancies_processed": vacancies_processed,
                   "average_salary": average_salary}
print(creating_table(answer, "SuperJob Moscow"))