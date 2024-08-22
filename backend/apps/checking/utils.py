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


def get_calculate_hours(id, start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT calculate_hours(%s, %s, %s);", [id, start_date, end_date])
        result = cursor.fetchone()
    return result[0] if result else False


def get_persons_report_range(id, start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("SELECT get_checking_reports_range(%s, %s, %s);", [id, start_date, end_date])
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results
