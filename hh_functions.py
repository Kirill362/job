import requests
from general_functions import predict_salary


def predict_rub_salary_hh(vacancy):
    if vacancy["salary"]:
        if vacancy["salary"]["currency"] == "RUR":
            return predict_salary(vacancy["salary"]["from"], vacancy["salary"]["to"])


def create_hh_table(languages):
    hh_answer = {}
    for lang in languages:
        average_salary = 0
        hh_vacancies_processed = 0
        payload = {"text": f"Программист {lang}",
                   "area": 1,
                   "per_page": 50}
        hh_url = "https://api.hh.ru/vacancies"
        response = requests.get(hh_url, params=payload)
        response.raise_for_status()
        hh_api_answer = response.json()
        for page in range(hh_api_answer["pages"]):
            payload = {"text": f"Программист {lang}",
                       "area": 1,
                       "per_page": 50,
                       "page": page}
            response = requests.get(hh_url, params=payload)
            response.raise_for_status()
            hh_api_answer = response.json()
            for vacancy in hh_api_answer["items"]:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    average_salary += salary
                    hh_vacancies_processed += 1
        hh_answer[lang] = {"vacancies_found": hh_api_answer["found"],
                       "vacancies_processed": hh_vacancies_processed,
                       "average_salary": int(average_salary / hh_vacancies_processed)}
    return hh_answer