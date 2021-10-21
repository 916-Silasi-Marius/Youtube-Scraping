from datetime import date


class Date:
    def __init__(self, year, month, day):
        self.__year = year
        self.__month = month
        self.__day = day

    def print_date(self):
        print(self.__year, self.__month, self.__day)

    @property
    def get_year(self):
        return self.__year

    @property
    def get_month(self):
        return self.__month

    @property
    def get_day(self):
        return self.__day

    def get_days_gap(self, start):
        l_date = date(self.__year, self.__month, self.__day)
        f_date = date(start.get_year, start.get_month, start.get_day)
        delta = l_date - f_date
        return delta
