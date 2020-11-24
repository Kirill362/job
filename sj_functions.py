import requests
from dotenv import load_dotenv
import os
from general_functions import predict_salary


def predict_rub_salary_sj(vacancy):
    if vacancy["currency"] == "rub" and vacancy["payment_from"] != 0 and vacancy["payment_to"] != 0:
        return predict_salary(vacancy["payment_from"], vacancy["payment_to"])


def create_sj_table(languages):
    load_dotenv()
    headers = {"X-Api-App-Id": os.environ['X-API-APP-ID']}
    sj_answer = {}
    vacancies_per_page = 20
    for lang in languages:
        sum_salary = 0
        sj_vacancies_processed = 0
        payload = {"town": 4,
                   "catalogues": 48,
                   "keyword": lang}
        hh_url = "https://api.superjob.ru/2.0/vacancies/"
        response = requests.get(hh_url, params=payload, headers=headers)
        response.raise_for_status()
        sj_dict = response.json()
        for page in range((sj_dict["total"] // vacancies_per_page) + 1):
            payload = {"town": 4,
                       "catalogues": 48,
                       "keyword": lang,
                       "page": page}
            response = requests.get(hh_url, params=payload, headers=headers)
            response.raise_for_status()
            sj_dict = response.json()
            for vacancy in sj_dict["objects"]:
                salary = predict_rub_salary_sj(vacancy)
                if salary:
                    sum_salary += salary
                    sj_vacancies_processed += 1
        if sj_vacancies_processed != 0:
            average_salary = int(sum_salary / sj_vacancies_processed)
        else:
            average_salary = None
        sj_answer[lang] = {"vacancies_found": sj_dict["total"],
                           "vacancies_processed": sj_vacancies_processed,
                           "average_salary": average_salary}
    return sj_answer