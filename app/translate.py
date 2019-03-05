import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language='en', dest_language='es'):
    """Function to use the MS Azure Test Translate API
    
    Arguments:
        text {string} -- text to translate
        source_language {string} -- source language
        dest_language {[type]} -- new translation language
        NOTE: languages must be a valid language, e.g. 'en' or 'es' etc.
    
    Returns:
        [json] -- returns json in utf-8 format with transated text
    """

    if 'MS_TRANSLATE_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATE_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATE_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))
