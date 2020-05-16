import pandas as pd
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
df = pd.read_excel(r'dictonary.xlsx')


@app.route('/')
def render_main():
    asai = ["நேர்", "நிரை", "நேர்பு", "நிரைபு", "நேர்/நேர்", "நிரை/நேர்", "நிரை/நிரை", "நேர்/நிரை",
            "நேர்/நேர்/நேர்", "நிரை/நேர்/நேர்", "நேர்/நிரை/நேர்", "நிரை/நிரை/நேர்", "நேர்/நேர்/நிரை",
            "நிரை/நேர்/நிரை", "நிரை/நிரை/நிரை", "நேர்/நிரை/நிரை", "நேர்/நேர்/நேர்/நேர்",
            "நிரை/நேர்/நேர்/நேர்", "நிரை/நிரை/நேர்/நேர்", "நேர்/நிரை/நேர்/நேர்", "நேர்/நேர்/நிரை/நேர்",
            "நிரை/நேர்/நிரை/நேர்", "நிரை/நிரை/நிரை/நேர்", "நேர்/நிரை/நிரை/நேர்", "நேர்/நேர்/நேர்/நிரை",
            "நிரை/நேர்/நேர்/நிரை", "நிரை/நிரை/நேர்/நிரை", "நேர்/நிரை/நேர்/நிரை", "நேர்/நேர்/நிரை/நிரை",
            "நிரை/நேர்/நிரை/நிரை", "நிரை/நிரை/நிரை/நிரை", "நேர்/நிரை/நிரை/நிரை"]

    seer = ["நாள்", "மலர்", "காசு", "பிறப்பு", "தேமா", "புளிமா", "கருவிளம்", "கூவிளம்", "தேமாங்காய்", "புளிமாங்காய்",
            "கருவிளங்காய்", "கூவிளங்காய்", "தேமாங்கனி", "புளிமாங்கனி", "கருவிளங்கனி", "கூவிளங்கனி", "தேமாந்தண்பூ",
            "புளிமாந்தண்பூ", "கருவிளந்தண்பூ", "கூவிளந்தண்பூ", "தேமாநறும்பூ", "புளிமாநறும்பூ", "கருவிளநறும்பூ",
            "கூவிளநறும்பூ", "தேமாந்தண்ணிழல்", "புளிமாந்தண்ணிழல்", "கருவிளந்தண்ணிழல்", "கூவிளந்தண்ணிழல்", "தேமாநறுநிழல்",
            "புளிமாநறுநிழல்", "கருவிளநறுநிழல்", "கூவிளநறுநிழல்"]

    wordSearchType = {"startwith": "Word start with", "endwith": "Word end with", "contains": "Word contains",
                      "containsAny": "Word contains any", "containsAll": "Word contains all"}

    return render_template("index.html", seer=seer, asai=asai, wordSearchType=wordSearchType)
    # return render_template("index.html")


def process(word, meaning, asai, seer, wordSearchTypeKey):
    global df
    try:
        tdf = df[:]
        if seer is not None and seer not in [' ', '']:
            if seer in ['காசு', 'பிறப்பு']:
                tdf = tdf[tdf.seerpu == seer]
            else:
                tdf = tdf[tdf.seer == seer]
        if asai is not None and asai not in [' ', '']:
            if asai in ['நேர்பு', 'நிரைபு']:
                tdf = tdf[tdf.asaipu == asai]
            else:
                tdf = tdf[tdf.asai == asai]

        if word is not None and word not in [' ', '']:
            if len(word) == len(word.translate({ord(c): "" for c in """!@#$%^&*()[]{};:,./<>?\|`~-=_+"'"""})):
                tWord = word.strip()
                tWord = tWord.translate ({ord(c): "" for c in """!@#$%^&*()[]{};:,./<>?\|`~-=_+"'"""})

                if wordSearchTypeKey == 'startwith':
                    tWord = '^'+tWord
                elif wordSearchTypeKey == 'endwith':
                    tWord = tWord+'$'
                elif wordSearchTypeKey in ['contains', ' ']:
                    tWord = tWord
                elif wordSearchTypeKey == 'containsAny':
                    tWord = tWord.replace(' ', '|')
                elif wordSearchTypeKey == 'containsAll':
                    #from itertools import permutations
                    #wordList = list(permutations(tword, tword.count(' ')+1))
                    #tword = '|'.join(['(.*?)'.join(w) + '.' for w in wordList])
                    tWord = tWord.replace(' ', '(.*?)')
                else:
                    tWord = '---'
            else:
                tWord = '---'
            # print(tWord)
            tdf = tdf[tdf.word.str.contains(tWord, regex=True)]

        # if word is not None and word not in [' ', '']:
        #     try:
        #         word = word.rstrip('.')
        #         if word[0] == '.':
        #             word = word + '.'
        #             tdf = tdf[tdf.word.str.contains(word, regex=True)]
        #         else:
        #             tdf = tdf[tdf.word.str.startswith(word)]
        #     except:
        #         tdf = tdf[tdf.word == False]

        if meaning is not None and meaning not in [' ', '']:
            try:
                tMeaning = meaning.translate({ord(c): "" for c in """!@#$%^&*()[]{};:,./<>?\|`~-=_+"'"""})
                if len(meaning) == len(tMeaning):
                    tMeaning = tMeaning.strip('.')
                    tMeaning = '.' + tMeaning + '.'
                    tdf = tdf[tdf.meaning.str.contains(tMeaning, regex=True)]
                else:
                    tdf = tdf[tdf.tMeaning == False]
            except:
                tdf = tdf[tdf.tMeaning == False]

        displayCount = str(len(tdf))
        availabeCount = displayCount
        maxLimit = 1000
        if len(tdf) > maxLimit:
            tdf.reset_index(inplace=True, drop=True)
            displayCount = str(maxLimit)
            tdf = tdf[:maxLimit]
        status = 'Showing ' + displayCount + ' from ' + availabeCount

        if asai in ['நேர்பு', 'நிரைபு'] or seer in ['காசு', 'பிறப்பு']:
            result = tdf[['word', 'meaning', 'asaipu', 'seerpu']].to_json(orient='records', force_ascii=False)
            result.columns = ['word', 'meaning', 'asai', 'seer']
        else:
            result = tdf[['word', 'meaning', 'asai', 'seer']].to_json(orient='records', force_ascii=False)
        tdf = None
    except:
        result = [{'word': ' ', 'meaning': ' ', 'asai': ' ', 'seer': ' '}]
        status = ' '
    return result, status


@app.route('/process', methods=['GET', 'POST'])
def startProcess():
    print('-----------------------------------------------------------------------------')
    word = request.form['word']
    meaning = request.form['meaning']
    asai = request.form['asai']
    seer = request.form['seer']
    wordSearchTypeKey = request.form['wordSearchTypeKey']
    try:
        status = ' '
        # result = [{'word': ' ', 'meaning': ' ', 'asai': ' ', 'seer': ' '}]
        # print("word : " + word)
        # print("meaning : " + meaning)
        # print("asai : " + asai)
        # print("seer : " + seer)
        result, status = process(word, meaning, asai, seer, wordSearchTypeKey)
    except:
        result = [{'word': ' ', 'meaning': ' ', 'asai': ' ', 'seer': ' '}]
        status = ' '
    return jsonify({'result': result, 'status': status})


port = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run()
