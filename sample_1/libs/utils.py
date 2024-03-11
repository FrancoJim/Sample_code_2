import logging

import pandas as pd
import requests

logging.basicConfig(level=logging.INFO)


def add(x, y):
    """
    Add two numbers together (for Testing purposes only)
    :param x: First number
    :param y: Second number
    :return: The sum of the two numbers
    """
    return x + y


class BEA_Wrapper:
    api_base = "http://apps.bea.gov/api/data"

    def __init__(self, api_key):
        self.api_key = api_key

    def list_datasets(self):
        """
        List all available datasets from the Bureau of Economic Analysis (BEA) API.
        :return: A pandas DataFrame containing the list of datasets.
        """
        url = f"{self.api_base}?&UserID={self.api_key}&method=GETDATASETLIST&ResultFormat=JSON"
        data = requests.get(url).json()
        return pd.DataFrame(data["BEAAPI"]["Results"]["Dataset"])

    def fetch_gdp_by_industry(self, year="2023"):
        """
        Fetch the Gross Domestic Product (GDP) by Industry dataset from the Bureau of Economic Analysis (BEA) API.
        :param year: The year(s) to fetch data for. Default is "2023".
        :return: A pandas DataFrame containing the data.
        """
        url = f"{self.api_base}?&amp;UserID={self.api_key}&amp;method=GetData&amp;DataSetName=GDPbyIndustry&amp;Year={year}&amp;Industry=ALL&amp;tableID=1&amp;Frequency=A&amp;ResultFormat=json"
        data = requests.get(url).json()
        return data
