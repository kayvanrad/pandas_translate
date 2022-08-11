import pandas as pd
import requests
import json

class PandasTranslate:
    def __init__(self, server='http://localhost:5000'):
        self.server=server
    
    def auto_detect(self, txt: str) -> str:
        '''
        detect input text language

        parameters
        ----------
        txt: str
            input text

        returns
        -------
        str
            detected language        
        '''
        res = requests.post(
            '{}/detect'.format(self.server),
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    'q': txt
                }
            )
        )
        return res.json()[0]['language']

    def translate(self, txt: str, target: str, source: str = None) -> str:
        '''
        translate input text

        parameters
        ----------
        txt: str
            input text
        target: str
            target language
        source: str, default = None
            source language, if None automatically detected from input
            text

        returns
        -------
        str
            translated text        
        '''
        if source is None:
            source = self.auto_detect(txt)

        res = requests.post(
            '{}/translate'.format(self.server),
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    'q': txt,
                    'source': source,
                    'target': target
                }
            )
        )

        return res.json()['translatedText']

    def translate_header(
        self, df: pd.DataFrame, target: str, source: str = None,
        copy: bool = False
    ) -> pd.DataFrame:
        '''
        translate dataframe header (column names)

        parameters
        ----------
        df: pandas df
            input data df
        target: str
            target language
        source: str, default = None
            source language, if None automatically detected from input
            text
        copy: bool, default = False
            whether to make a copy of the input df

        returns
        -------
        pandas df
            df with translated header (column names)
        '''
        if copy:
            df = df.copy()
        df.columns = [
            self.translate(x, target=target, source=source) for x in df.columns
        ]
        return df

    def translate_entries(
        self, df: pd.DataFrame, cols: list, target: str, source: str = None,
        copy: bool = False
    ) -> pd.DataFrame:
        '''
        translate entries in dataframe

        parameters
        ----------
        df: pandas df
            input data df
        cols: list
            list of columns to be translated
        target: str
            target language
        source: str, default = None
            source language, if None automatically detected from input text
        copy: bool, default = False
            whether to make a copy of the input df

        returns
        -------
        pandas df
            df with translated entries
        '''    
        if copy:
            df = df.copy()
        for c in cols:
            df[c] = df[c].apply(
                lambda x: self.translate(x, target=target, source=source)
            )
        return df