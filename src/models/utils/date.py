from datetime import datetime, timedelta

class DateGeneration2Days:
    @staticmethod
    def start_date():
        current_date = datetime.now()
        start_date = current_date - timedelta(days=2)
        return start_date

    @staticmethod
    def end_date():
        current_date = datetime.now()
        end_date = current_date + timedelta(days=2)
        return end_date