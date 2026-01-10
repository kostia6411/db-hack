from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
import random


def get_schoolkid(full_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print("Ученик не найден")
        return
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников")
        return


def fix_marks(full_name):
    schoolkid = get_schoolkid(full_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(full_name):
    schoolkid = get_schoolkid(full_name)
    Chastisement.objects.filter(schoolkid=schoolkid).delete() 


def create_commendation(full_name, subject):
    schoolkid = get_schoolkid(full_name)
    try:
        lesson = Lesson.objects.filter(
            group_letter=schoolkid.group_letter, 
            year_of_study=schoolkid.year_of_study, 
            subject__title__contains=subject
        ).order_by("-date")[0]
    except Lesson.DoesNotExist:
        print("Урок не найден")
        return
    recommendation = [
        "Молодец!", 
        "Отлично!", 
        "Хорошо!", 
        "Гораздо лучше, чем я ожидал!", 
        "Ты меня приятно удивил!", 
        "Великолепно!", 
        "Прекрасно!", 
        "Ты меня очень обрадовал!", 
        "Именно этого я давно ждал от тебя!", 
        "Ты, как всегда, точен!", 
        "Очень хороший ответ!",
        "Талантливо!", 
        "Ты сегодня прыгнул выше головы!", 
        "Я поражен!", 
        "Уже существенно лучше!", 
        "Потрясающе!", 
        "Замечательно!", 
        "Прекрасное начало!", 
        "Так держать!"
    ]
    random_recommendation = random.choice(recommendation)
    Commendation.objects.create(
        text=random_recommendation, 
        created=lesson.date, 
        schoolkid=schoolkid, 
        teacher=lesson.teacher, 
        subject=lesson.subject
    )
