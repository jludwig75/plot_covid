import json
from datetime import datetime

COUNTRY_DATA_FILE_NAME = 'country_data.json'

def date_string(dt):
    return '%04u-%02u-%02u' % (dt.year, dt.month, dt.day)

def _load_country_data():
    with open(COUNTRY_DATA_FILE_NAME, 'rt') as file:
        return json.loads(file.read())

def _geoid_csv_file_name(geoid):
    return geoid.lower() + '.csv'

class CountryDataset:
    def __init__(self, geoid, country_name, population):
        self._geoid = geoid
        self._country_name = country_name
        self._population = population
        self._datapoints = []

    def add_datapoint(self, datapoint):
        self._datapoints.append(datapoint)
        self._datapoints.sort(key=lambda r: r.date)
        cummulative_cases = 0
        cummulative_deaths = 0
        for dp in self._datapoints:
            cummulative_cases = dp.accumulate_cases(cummulative_cases)
            cummulative_deaths = dp.accumulate_deaths(cummulative_deaths)
    def save_csv(self):
        file_name = _geoid_csv_file_name(self._geoid)
        with open(file_name, 'wt') as file:
            file.write('date,new_cases,new_deaths,new_cases_per_1m,new_deaths_per_1m,cum_cases,cum_deaths,cum_cases_per_1m,cum_deaths_per_1m\n')
            for dp in self._datapoints:
                file.write('%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n' % (date_string(dp.date), dp.new_cases, dp.new_deaths, dp.new_cases_per_1m, dp.new_deaths_per_1m, dp.cummulative_cases, dp.cummulative_deaths, dp.cummulative_cases_per_1m, dp.cummulative_deaths_per_1m))

    @property
    def geoid(self):
        return self._geoid
    @property
    def country_name(self):
        return self._country_name
    @property
    def population(self):
        return self._population
    @property
    def datapoints(self):
        return self._datapoints
    def dump(self):
        print('%s: %s, %u' % (self._geoid, self._country_name, self._population))
        for dp in self._datapoints:
            dp.dump()

class CovidDataPoint:
    def __init__(self, country_dataset, date, new_cases, new_deaths):
        self._country_dataset = country_dataset
        self._date = date
        self._new_cases = new_cases
        self._new_deaths = new_deaths
    def accumulate_cases(self, prior_case_count):
        self._cummulative_cases = self._new_cases + prior_case_count
        return self._cummulative_cases
    def accumulate_deaths(self, prior_death_count):
        self._cummulative_deaths = self._new_deaths + prior_death_count
        return self._cummulative_deaths
    @property
    def country_dataset(self):
        return self._country_dataset
    @property
    def date(self):
        return self._date
    @property
    def new_cases(self):
        return self._new_cases
    @property
    def new_deaths(self):
        return self._new_deaths
    @property
    def new_cases_per_1m(self):
        return self._convert_to_per_1m(self._new_cases)
    @property
    def new_deaths_per_1m(self):
        return self._convert_to_per_1m(self._new_deaths)
    @property
    def cummulative_cases(self):
        return self._cummulative_cases
    @property
    def cummulative_deaths(self):
        return self._cummulative_deaths
    @property
    def cummulative_cases_per_1m(self):
        return self._convert_to_per_1m(self._cummulative_cases)
    @property
    def cummulative_deaths_per_1m(self):
        return self._convert_to_per_1m(self._cummulative_deaths)
    def _convert_to_per_1m(self, value):
        if self._country_dataset.population == 0:
            return None
        return (value * 1000000) / self._country_dataset.population
    def dump(self):
        print('%s: %.3f, %.3f, %.3f, %.3f' % (self.date, self.new_cases_per_1m, self.new_deaths_per_1m, self.cummulative_cases_per_1m, self.cummulative_deaths_per_1m))

def load_dataset(geoid):
    country_data = _load_country_data()
    file_name = _geoid_csv_file_name(geoid)
    cds = CountryDataset(geoid, country_data[geoid]['name'], int(country_data[geoid]['population']))
    with open(file_name, 'rt') as file:
        lines = file.readlines()
        field_names = lines[0].split(',')
        assert field_names[0] == 'date'
        assert field_names[1] == 'new_cases'
        assert field_names[2] == 'new_deaths'
        for i in range(1, len(lines)):
            parts = lines[i].split(',')
            date_parts = parts[0].split('-')
            cds.add_datapoint(CovidDataPoint(cds, datetime(year=int(date_parts[0]), month=int(date_parts[1]), day=int(date_parts[2])), float(parts[1]), float(parts[2])))
    return cds
