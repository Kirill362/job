from terminaltables import AsciiTable


def create_table(table_data, title):
    table_info = [["languages", "vacancies_found", "vacancies_processed", "average_salary"]]
    for vacancy in table_data:
        vacancy_info = table_data[vacancy]
        table_info.append([vacancy, vacancy_info["vacancies_found"], vacancy_info["vacancies_processed"], vacancy_info["average_salary"]])
    table = AsciiTable(table_info, title)
    return table.table


def predict_salary(from_salary, to_salary):
    if from_salary and to_salary:
        return (from_salary + to_salary) / 2
    elif not from_salary:
        return to_salary * 0.8
    elif not to_salary:
        return from_salary * 1.2