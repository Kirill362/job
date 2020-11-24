from hh_functions import create_hh_table
from sj_functions import create_sj_table
from general_functions import creating_table

LANGUAGES = ["JavaScript", "Java", "Python", "Ruby", "PHP", "C++", "CSS", "C#"]


def main():
    hh_answer = create_hh_table(LANGUAGES)
    sj_answer = create_sj_table(LANGUAGES)
    print(creating_table(hh_answer, "HeadHunter Moscow"))
    print(creating_table(sj_answer, "SuperJob Moscow"))


if __name__ == '__main__':
    main()
