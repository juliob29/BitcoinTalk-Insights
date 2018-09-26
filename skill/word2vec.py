"""
Logic for training word2vec model.
"""
import os
import spacy
import gensim
import requests

from tqdm import tqdm
from isoweek import Week
from sanic.log import logger
from datetime import datetime, timedelta
from skill.bitcointalk import BitcoinTalk


class Model:
    """
    This class sets up the Word2Vec model on the BitcoinTalk data. It cleans 
    the data by creating sentences and removing stop words, creates the corpus, 
    and then runs this data in a Word2Vec model with 4000 epochs.
    """

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.last_week = BitcoinTalk().last_week()

    def __create_sentences(self, document):
        """
        This function creates sentences using the spacy library.

        Parameters
        ----------
        document: str 
            Any large string will be split into sentences. 

        Returns
        -------
        list
            List with split sentences.
        """
        doc = self.nlp(document)
        return [sentence.text for sentence in doc.sents]

    def __remove_stop_words(self,
                            document,
                            minimum_token_length=3,
                            minimum_sentence_length=3):
        """
        Removes stop words from an input document.
        This method also removes tokens (i.e. words)
        that contain a single character.
        
        Parameters
        ----------
        document: str
            Text string representing a document.
        
        minimum_token_length: int, default 3
            Minimum token length for a token
            to be included.
        
        minimum_sentence_length: int, default 2
            Minimum tokens (i.e. words) that a 
            sentence must have.
        
        Returns
        -------
        str
            String without stop words. Words are separated
            by a space (i.e. ' ').
        """
        doc = self.nlp(document)
        results = [
            token.text.strip() for token in doc
            if not token.is_stop and len(token.text) > minimum_token_length
        ]

        if len(results) < minimum_sentence_length:
            return None
        else:
            return results

    def _corpus_create(self, documents):
        """
        This function creates a corpus that is cleaned from the PostgreSQL 
        database. It removes all stop words and shorter sentences, and 
        appends to a variable in the format needed for Word2Vec to train.

        Parameters
        ----------
        documents: list
            List of documents extracted from Bitcointalk().last_week()

        Returns
        -------
        results: list
            Contains a corpus that can be directed used to 
            train Word2Vec model. A corpus is a list of sentences.
            And a sentence is a list of words (str). Example:

                [
                    ['bitcoin', 'prices', 'soar'],
                    ['ethereum', 'prices', 'slow', 'down']
                ]
        """
        logger.info("Cleaning Corpus...")

        results = []
        for document in documents:
            sentences = self.__create_sentences(
                document['content_no_quote_no_html'])
            for sentence in sentences:
                sentences_no_stop_words = self.__remove_stop_words(
                    sentence,
                    minimum_token_length=2,
                    minimum_sentence_length=3)
            if sentences_no_stop_words:
                results.append(sentences_no_stop_words)
        lower_case = []
        for result in results:
            mapped = map(str.lower, result)
            lower_case.append(list(mapped))

        logger.info("Corpus Cleaned!")
        return lower_case

    def train(self,
              data_last_week=True,
              epochs=4000,
              directory=os.getenv('MODELS_PATH'), 
              **kwargs):
        """
        This functions trains a Word2Vec model on the last week data from BitcoinTalk.
        This training should be run everyweek on a new dataset. It will save
        its results to models directory under the name of the current week. 

        Parameters
        ----------
        epochs: int, default 4000
            Number of epochs to train model for.
        
        directory: str, default 'models'
            Directory to store trained models.

        Returns
        -------
        model: gensim.models.Word2Vec
            Trained Gensim Word2Vec model.
        """
        if data_last_week:
            data = self.last_week
        else:
            data = BitcoinTalk().all()

        last_week = str(Week.thisweek() - 1)

        print("Training pipeline beginning!!")
        logger.info(f'Getting last weeks data ({last_week})')
        cleaned_data = self._corpus_create(data)

        logger.info('Training Model.')
        model = gensim.models.Word2Vec(cleaned_data, iter=epochs, **kwargs)
        logger.info('Model trained!')

        logger.info('Saving model to directory models.')
        model.save(f'{directory}/{last_week}.model')
        logger.info('Done!')
        print("Done training!!")

        
        return model


if __name__ == '__main__':
    Model().train()
