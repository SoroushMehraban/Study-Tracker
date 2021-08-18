import datetime
import pickle
import os
from colorama import Fore, Style


def get_input():
    instructions = f"""\n{Fore.CYAN}Choose a number from below:{Style.RESET_ALL}
{Fore.GREEN}1){Style.RESET_ALL} Add a new study
{Fore.GREEN}2){Style.RESET_ALL} Show review items
{Fore.GREEN}3){Style.RESET_ALL} Update a review item
{Fore.GREEN}4){Style.RESET_ALL} Show all
{Fore.GREEN}5){Style.RESET_ALL} EXIT
{Fore.YELLOW}>{Style.RESET_ALL} """
    while True:
        try:
            input_number = int(input(instructions))
            if input_number > 5 or input_number < 1:
                print(f"\n{Fore.RED}Value should be from 1 to 5{Style.RESET_ALL}\n")
                continue
            return input_number
        except ValueError:
            print(f"\n{Fore.RED}Entered value should be a number{Style.RESET_ALL}\n")


def add_new_study():
    study_name = input(f"{Fore.CYAN}Enter the name of the study{Style.RESET_ALL}\n> ")
    if not (study_name in stored_studies):
        stored_studies[study_name] = {
            'number_of_studies': 1,
            'date': datetime.date.today()
        }
        save_stored_studies()
        print(f"{Fore.GREEN}SAVED SUCCESSFULLY{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}ALREADY EXISTS!{Style.RESET_ALL}")


def show_review_items():
    today_time = datetime.date.today()

    shown_dict = {}
    for index, study_name in enumerate(stored_studies):
        time_delta = datetime.timedelta(days=stored_studies[study_name]['number_of_studies'])
        if today_time - stored_studies[study_name]['date'] >= time_delta:
            print(f"{Fore.GREEN}{index}. {Fore.YELLOW}{study_name}{Style.RESET_ALL}")
            shown_dict[index] = study_name
            shown_any = True

    if len(shown_dict) == 0:
        print(f"{Fore.RED}Nothing to review{Style.RESET_ALL}")
    return shown_dict


def update_review_item():
    shown_dict = show_review_items()

    user_input = input(f"{Fore.CYAN}Enter study name or a number from above:\n{Fore.YELLOW}>{Style.RESET_ALL} ")
    try:
        study_index = int(user_input)
        try:
            study_name = shown_dict[study_index]
        except KeyError:
            print(f"{Fore.RED} number should be from one of the shown items\n")
            return update_review_item()
    except ValueError:
        study_name = user_input

    if study_name in stored_studies:
        stored_studies[study_name]['number_of_studies'] += 1
        stored_studies[study_name]['date'] = datetime.date.today()
        save_stored_studies()
        print(f"{Fore.GREEN}UPDATED SUCCESSFULLY{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}DOES NOT EXIST!{Style.RESET_ALL}")


def load_stored_studies():
    if os.path.exists('studies.bin'):
        with open('studies.bin', 'rb') as f:
            return pickle.load(f)
    else:
        with open('studies.bin', 'wb') as f:
            pickle.dump({}, f)
        return load_stored_studies()


def save_stored_studies():
    with open('studies.bin', 'wb') as f:
        pickle.dump(stored_studies, f)


def show_all():
    today_time = datetime.date.today()
    for study_name in stored_studies:
        review_date = stored_studies[study_name]['date'] \
                      + datetime.timedelta(days=stored_studies[study_name]['number_of_studies'])
        days_from_today = (review_date - today_time).days

        if days_from_today > 0:
            print(
                f"{Fore.YELLOW}{study_name}:{Fore.GREEN} Should be reviewed after {days_from_today} day{'s' if days_from_today > 1 else ''}{Style.RESET_ALL}")
        elif days_from_today < 0:
            print(
                f"{Fore.YELLOW}{study_name}:{Fore.RED} {days_from_today * -1} day{'s' if days_from_today < -1 else ''}"
                f" passed from the review{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}{study_name}:{Fore.MAGENTA} Should be reviewed today{Style.RESET_ALL}")


if __name__ == '__main__':
    stored_studies = load_stored_studies()

    while True:
        given_order_number = get_input()
        if given_order_number == 1:
            add_new_study()
        elif given_order_number == 2:
            show_review_items()
        elif given_order_number == 3:
            update_review_item()
        elif given_order_number == 4:
            show_all()
        elif given_order_number == 5:
            exit()
