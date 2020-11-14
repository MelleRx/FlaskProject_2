from random import shuffle


def random_teachers(teachers):
    lst = list(range(1, len(teachers)))
    shuffle(lst)
    return lst


def free_time(teachers, id_t):
    result = {"Понедельник": [], "Вторник": [], "Среда": [], "Четверг": [],
              "Пятница": [], "Суббота": [], "Воскресенье": []}
    for day, time in teachers[id_t]["free"].items():
        for key, value in time.items():
            if day == "mon":
                if value:
                    result["Понедельник"].append(key)

            if day == "tue":
                if value:
                    result["Вторник"].append(key)

            if day == "wed":
                if value:
                    result["Среда"].append(key)

            if day == "thu":
                if value:
                    result["Четверг"].append(key)

            if day == "fri":
                if value:
                    result["Пятница"].append(key)

            if day == "sat":
                if value:
                    result["Суббота"].append(key)

            if day == "sun":
                if value:
                    result["Воскресенье"].append(key)
    return result
