df = pd.read_excel('dictonary.xlsx')
df
dy = pd.DataFrame(list(zip(wordList, meaningList)), 
               columns =['word', 'meaning']) 
dy 
from seerPiri import *
def asai(val):
    try:
        a, s = process(val + ' று')
        return ' '.join(a[:-1])
    except:
        return ' '

def seer(val):
    try:
        a, s = process(val + ' று')
        return ''.join(s[:-2]).replace('/ ', ' ')
    except:
        return ' '
dy['asai'] = dy['word'].apply(asai)
dy['seer'] = dy['word'].apply(seer)
dy['asai'] = dy['asai'].str.strip()
dy['seer'] = dy['seer'].str.strip()
dy['seer'] = dy['seer'].str.replace('-1','')    
dy['seerpu'] = ' '
for i in dy[((dy.word.str.contains('.உ$|.ு$', regex=True)) & (dy.seer == 'நிரை/நேர்'))].index:
    dy.loc[i].seerpu = 'நிரைபு'
for i in dy[((dy.word.str.contains('.உ$|.ு$', regex=True)) & (dy.seer == 'நேர்/நேர்'))].index:
    dy.loc[i].seerpu = 'நேர்பு'

dz = pd.concat([df, dy[~(dy.word.isin(df.word))]], ignore_index=True)

dz[dz.word.str.contains(' ')].asai = ' '
dz[dz.word.str.contains(' ')].seer = ' '
dz[dz.word.str.contains(' ')].seerpu = ' '

dz.to_excel('dictionary_v2.xlsx', index=False, encoding = 'UTF-8')