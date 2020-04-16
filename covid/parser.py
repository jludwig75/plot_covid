from covid.dataset import CountryDataset, CovidDataPoint, COUNTRY_DATA_FILE_NAME
import xlrd
import requests
import json

_DATE_COL_NAME = 'dateRep'
_CASES_COL_NAME = 'cases'
_DEATHS_COL_NAME = 'deaths'
_COUNTRY_NAME_COL_NAME = 'countriesAndTerritories'
_COUNTRY_GEIOD_COL_NAME = 'geoId'
_POPULATION_COL_NAME = 'popData2018'

class CovidDataRowParser:
    def __init__(self):
        self._contry_datasets = {}

    @property
    def country_datasets(self):
        return self._contry_datasets

    def parse_row(self, row):
        cds = self._get_country_dataset(row[_COUNTRY_GEIOD_COL_NAME], row)
        if cds is None:
            return
        cds.add_datapoint(CovidDataPoint(cds, xlrd.xldate_as_datetime(row[_DATE_COL_NAME], 0), int(row[_CASES_COL_NAME]), int(row[_DEATHS_COL_NAME])))

    def _get_country_dataset(self, geoid, row_dict):
        if not geoid in self._contry_datasets:
            if not type(row_dict[_POPULATION_COL_NAME]) is float:
                # Skip countries for which there is no population data
                return None
            self._contry_datasets[geoid] = CountryDataset(geoid, row_dict[_COUNTRY_NAME_COL_NAME], int(row_dict[_POPULATION_COL_NAME]))
        return self._contry_datasets[geoid]

class CovidDatasetParser:
    def __init__(self, dataset_filename):
        self._dataset_filename = dataset_filename
        self._column_table = {}

    def _find_columns(self):
        for col in range(self._sheet.ncols):
            if self._sheet.cell_value(0, col) == _DATE_COL_NAME:
                self._column_table[_DATE_COL_NAME] = col
            elif self._sheet.cell_value(0, col) == _CASES_COL_NAME:
                self._column_table[_CASES_COL_NAME] = col
            elif self._sheet.cell_value(0, col) == _DEATHS_COL_NAME:
                self._column_table[_DEATHS_COL_NAME] = col
            elif self._sheet.cell_value(0, col) == _COUNTRY_NAME_COL_NAME:
                self._column_table[_COUNTRY_NAME_COL_NAME] = col
            elif self._sheet.cell_value(0, col) == _COUNTRY_GEIOD_COL_NAME:
                self._column_table[_COUNTRY_GEIOD_COL_NAME] = col
            elif self._sheet.cell_value(0, col) == _POPULATION_COL_NAME:
                self._column_table[_POPULATION_COL_NAME] = col
        if not _DATE_COL_NAME in self._column_table:
            raise Exception('Date column not found')
        if not _CASES_COL_NAME in self._column_table:
            raise Exception('Cases column not found')
        if not _DEATHS_COL_NAME in self._column_table:
            raise Exception('Deaths column not found')
        if not _COUNTRY_NAME_COL_NAME in self._column_table:
            raise Exception('Country name column not found')
        if not _COUNTRY_GEIOD_COL_NAME in self._column_table:
            raise Exception('Country geo code column not found')
        if not _POPULATION_COL_NAME in self._column_table:
            raise Exception('Population column not found')

    def _parse_rows(self):
        row_parser = CovidDataRowParser()
        for r in range(1, self._sheet.nrows):
            row = {}
            row[_DATE_COL_NAME] = self._sheet.cell_value(r, self._column_table[_DATE_COL_NAME])
            row[_CASES_COL_NAME] = self._sheet.cell_value(r, self._column_table[_CASES_COL_NAME])
            row[_DEATHS_COL_NAME] = self._sheet.cell_value(r, self._column_table[_DEATHS_COL_NAME])
            row[_COUNTRY_NAME_COL_NAME] = self._sheet.cell_value(r, self._column_table[_COUNTRY_NAME_COL_NAME])
            row[_COUNTRY_GEIOD_COL_NAME] = self._sheet.cell_value(r, self._column_table[_COUNTRY_GEIOD_COL_NAME])
            row[_POPULATION_COL_NAME] = self._sheet.cell_value(r, self._column_table[_POPULATION_COL_NAME])
            row_parser.parse_row(row)
        return row_parser.country_datasets

    def parse(self):
        loc = (self._dataset_filename)
        wb = xlrd.open_workbook(loc) 
        self._sheet = wb.sheet_by_index(0)
        self._find_columns()
        return self._parse_rows()

class CovidParser:
    _DATASET_FILENAME = 'dataset.xlsx'
    def __init__(self, dataset_url):
        self._dataset_url = dataset_url

    def _download_dataset(self):
        print('Downloading "%s"...' % self._dataset_url)
        with open(self._DATASET_FILENAME, 'wb') as file:
            r = requests.get(self._dataset_url, allow_redirects=True)
            file.write(r.content)

    def _parse_dataset(self):
        print('Parsing data...')
        parser = CovidDatasetParser(self._DATASET_FILENAME)
        self._country_datasets = parser.parse()

    def _save_data_files(self):
        print('saving data files...')
        for geoid, cds in self._country_datasets.items():
            # print('Saving data file for country %s' % geoid)
            cds.save_csv()
        country_data = {}
        for geoid, cds in self._country_datasets.items():
            country_data[geoid] = {'name': cds.country_name, 'population': cds.population}
        print('Saving country data to %s' % COUNTRY_DATA_FILE_NAME)
        with open(COUNTRY_DATA_FILE_NAME, 'wt') as file:
            file.write(json.dumps(country_data))

    def _plot_dataset(self):
        print('Plotting data...')
        for geoid, cds in self._country_datasets.items():
            # print('Plotting data file for country %s' % geoid)
            cds.dump()

    def run(self):
        self._download_dataset()
        self._parse_dataset()
        self._save_data_files()
        # self._plot_dataset()
