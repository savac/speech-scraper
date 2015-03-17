import urllib 
import re


def get_speech_html():
    '''Get html files only'''
    indexUrl="http://millercenter.org/president/speeches"
    baseUrl="http://millercenter.org/president"
    linkMatch='speeches/speech'
    outDir='../data'

    links = get_speech_links(indexUrl,linkMatch)
    for link in links:
        urllib.urlretrieve(baseUrl+'/'+link, outDir + '/' + link.replace('/', '_') + '.html')

def get_speech_links(indexUrl,linkMatch):
    '''Get a list of links'''
    # Get the index page
    htmlFile=urllib.urlopen(indexUrl)
    htmlText=htmlFile.read()
    
    # Get all links to transcripts
    # <a href="lbjohnson/speeches/speech-3523" class="transcript">Transcript</a>
    pattern=re.compile("<a href=""(.+?)"" class=""transcript"">")
    links=re.findall(pattern, htmlText)
    
    # Extra check
    #linksSpeech=[]
    #for link in linksTranscript:
    #    if linkMatch in link:
	#		linksSpeech.append(link.strip('"'))
    
    linksClean = []
    for link in links:
        linksClean.append(link.strip('"'))

    return linksClean

def parseHtml(textHtml):
    '''Given raw html return tuple with speaker, title, date, text'''

    # Get title and date
    try:
        pattern=re.compile("<h1 id=amprestitle>(.+?)</h1>")
        res=re.findall(pattern, textHtml)
        title=re.sub("\(.*?\)", "", res[0])
        pattern=re.compile("\((.+?)\)")
        res=re.findall(pattern, res[0])
        date=res[0]
    except IndexError:
        date='unknown'
        title='unknown'

    # Get speaker
    res=textHtml.split('<h2 style="margin: 0; padding: 0;">', 1)
    res=res[1].split('</h2>')
    try:
        speaker=res[0]
    except IndexError:
        speaker='unknown'

    # Get text
    res=textHtml.split('<div id=transcript class=indent>', 1)
    res=res[1].split('</div>')
    try:
        text=res[0]
        text=remove_tags(text)
    except IndexError:
        text='unknown'

    '''
    <h1 id=amprestitle>First Inaugural Address (January 20, 2001)</h1>
    <h2 style="margin: 0; padding: 0;">George W. Bush</h2>
    <aside>
    <div class=clearfix></div>
    <p id=description><p>George W. Bush delivers his inaugural address following his election to the first of his two Presidential terms.&nbsp; The President recognizes and thanks his 2000 Presidential Election opponent, Vice President Al Gore, who contested Bush&rsquo;s victory until a recount of Florida&rsquo;s votes took place, the critical state in the Electoral College tally.&nbsp; Bush also promises reductions in taxes, reforms in Social Security, Welfare and education, increases in defense, and intolerance of weapons of mass destruction.</p></p>
    <div id=word-cloud>
    <h2>Word Cloud</h2>
    <p>This is a chart of the words used most frequently in this speech. The larger the
    word, the more frequently that it was used.</p>
    <div id=tags><span style="font-size: 1.2em;">american</span> <span style="font-size: 0.7em;">called</span> <span style="font-size: 0.9em;">children</span> <span style="font-size: 2.1em;">citizens</span> <span style="font-size: 0.9em;">civility</span> <span style="font-size: 0.7em;">commitment</span> <span style="font-size: 1.2em;">common</span> <span style="font-size: 0.7em;">compassion</span> <span style="font-size: 1.8em;">country</span> <span style="font-size: 1.2em;">courage</span> <span style="font-size: 0.9em;">duty</span> <span style="font-size: 0.7em;">faith</span> <span style="font-size: 0.9em;">freedom</span> <span style="font-size: 0.7em;">justice</span> <span style="font-size: 0.9em;">live</span> <span style="font-size: 1.4em;">must</span> <span style="font-size: 1.6em;">nation</span> <span style="font-size: 0.7em;">nation39s</span> <span style="font-size: 4em;">our</span> <span style="font-size: 0.9em;">power</span> <span style="font-size: 0.9em;">promise</span> <span style="font-size: 0.9em;">public</span> <span style="font-size: 0.9em;">purpose</span> <span style="font-size: 0.7em;">sometimes</span> <span style="font-size: 1.6em;">story</span> <span style="font-size: 0.9em;">time</span> <span style="font-size: 4em;">will</span> <span style="font-size: 0.9em;">work</span> <span style="font-size: 1.2em;">you</span> <span style="font-size: 0.7em;">your</span>
    </div>	</div>
    </aside>
    <div id=transcript class=indent>
    <p>President Clinton, distinguished guests and my fellow citizens, the peaceful transfer of authority is rare in history, yet common in our country. With a simple oath, we affirm old traditions and make new beginnings.<br/>
    As I begin, I thank President Clinton for his service to our nation.<br/>
    '''

    return (speaker, title, date, text)

def remove_tags(text):
    '''TBD: This will fail if there are single < or > characters'''
    return re.sub("<.*?>", "", text)


if __name__ == '__main__':
    indexUrl="http://millercenter.org/president/speeches"
    baseUrl="http://millercenter.org/president"
    linkMatch='speeches/speech'
    outDir='../data'

    # tab separated file to hold the speaker, title, date etc.
    tsvOut = open(outDir + '/' + 'info.tsv','wb')

    links = get_speech_links(indexUrl,linkMatch)

    i=0
    for link in links:
        i+=1
        print '%d/%d' %(i, len(links))
        fileOut = outDir + '/' + link.replace('/', '_') + '.txt'
        htmlFile=urllib.urlopen(baseUrl+'/'+link)
        htmlText=htmlFile.read()

        (speaker, title, date, text)=parseHtml(htmlText)

        infoOut=fileOut+'\t'+speaker+'\t'+title+'\t'+date+'\n'
        tsvOut.write(infoOut)

        textOut=open(fileOut,'wb')
        textOut.write(text)

