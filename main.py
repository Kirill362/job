import requests
from terminaltables import AsciiTable

LANGUAGES = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "CSS", "C#"]
HEADERS = {"X-Api-App-Id": "v3.h.3969469.05b92e1fe4e00b35711d249709174f06dc4bde24.fd893b9db5354288d7028c8be578ecd46699f697"}


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


def predict_rub_salary_hh(vacancie):
    if vacancie["salary"]:
        if vacancie["salary"]["currency"] == "RUR":
            return predict_salary(vacancie["salary"]["from"], vacancie["salary"]["to"])


def predict_rub_salary_sj(vacancie):
    if vacancie["currency"] == "rub" and vacancie["payment_from"] != 0 and vacancie["payment_to"] != 0:
        return predict_salary(vacancie["payment_from"], vacancie["payment_to"])


def main():
    hh_answer = {}
    sj_answer = {}
    for lang in LANGUAGES:
        average_salary = 0
        hh_vacancies_processed = 0
        payload = {"text": f"Программист {lang}",
                   "area": 1,
                   "per_page": 50}
        hh_url = "https://api.hh.ru/vacancies"
        response = requests.get(hh_url, params=payload)
        response.raise_for_status()
        for page in range(response.json()["pages"]):
            payload = {"text": f"Программист {lang}",
                       "area": 1,
                       "per_page": 50,
                       "page": page}
            response = requests.get(hh_url, params=payload)
            response.raise_for_status()
            for vacancie in response.json()["items"]:
                salary = predict_rub_salary_hh(vacancie)
                if salary:
                    average_salary += salary
                    hh_vacancies_processed += 1
        hh_answer[lang] = {"vacancies_found": response.json()["found"],
                       "vacancies_processed": hh_vacancies_processed,
                       "average_salary": int(average_salary / hh_vacancies_processed)}
        sum_salary = 0
        sj_vacancies_processed = 0
        payload = {"town": 4,
                   "catalogues": 48,
                   "keyword": lang}
        hh_url = "https://api.superjob.ru/2.0/vacancies/"
        response = requests.get(hh_url, params=payload, headers=HEADERS)
        response.raise_for_status()
        for page in range(response.json()["total"] // 20 + 1):
            payload = {"town": 4,
                       "catalogues": 48,
                       "keyword": lang,
                       "page": page}
            response = requests.get(hh_url, params=payload, headers=HEADERS)
            response.raise_for_status()
            for vacancie in response.json()["objects"]:
                salary = predict_rub_salary_sj(vacancie)
                if salary:
                    sum_salary += salary
                    sj_vacancies_processed += 1
        if sj_vacancies_processed != 0:
            average_salary = int(sum_salary / sj_vacancies_processed)
        else:
            average_salary = None
        sj_answer[lang] = {"vacancies_found": response.json()["total"],
                       "vacancies_processed": sj_vacancies_processed,
                       "average_salary": average_salary}
    print(creating_table(hh_answer, "HeadHunter Moscow"))
    print(creating_table(sj_answer, "SuperJob Moscow"))


if __name__ == '__main__':
  main()
