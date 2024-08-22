from django.db import connection


def get_people_inside_today():
    with connection.cursor() as cursor:
        cursor.execute("SELECT count_people_inside_today();")
        result = cursor.fetchone()
    return result[0] if result else False


def get_persons_checkins_today():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_persons_checkins_today();")
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results
