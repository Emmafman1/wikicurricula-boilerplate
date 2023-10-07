import urllib

import sys

import calendar

import json

import datetime

from urllib.request import urlopen

import urllib.parse

import string

import json

from datetime import datetime

# Language subdomain for API calls
language = "en"

wikidata_id = 1

size = 1

first_edit = 1

notes = 1

images = 1

page_views = 1

incipit_size = 1

discussion_size = 1

# Discussion page prefix
discussion = "Discussion:"
discussion_url = urllib.parse.quote(discussion)

# At the moment, the warning count does not work for the Spanish Wikipedia
warnings_config = 0

commons_page = 1

commons_gallery = 1

wikisource = 1

wikiversity = 1

wikibooks = 1

featured = 1

# Featured article template
featured_template = "{{featured article"

quality = 1

# Good article template
good_article_template = "{{good article"

review = 1

bibliography = 1

coordinates = 1


def get_avg_page_views(article, start, end):
    total_views = 0

    try:
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{language}.wikipedia/all-access/user/{article}/daily/{start}/{end}"
        html = urlopen(url).read()

        html = str(html)
        html = html.replace('{"items":[', "")
        html = html.replace(']}', "")

        n = html.count("}")

        for i in range(n):
            txt = html[:html.find("}") + 1]
            total_views += int(txt[txt.find('"views":') + len('"views":'):-1])
            html = html.replace(txt, "", 1)

        start_date = datetime.strptime(start, "%Y%m%d")
        end_date = datetime.strptime(end, "%Y%m%d")
        days = (abs((end_date - start_date).days) + 1)
        result = str(int(round((total_views / days), 0)))

    except:
        result = "ERROR"

    return result


# Returns visits since the beginning of time, average daily visits since the beginning of time,
# average daily visits in the specified year
def visits(article):
    start_all_time = "20150701"

    start_prev_year = "20220101"
    end_prev_year = "20221231"

    start_current_year = "20230101"
    end_current_year = "20230831"

    date = []

    # Calculate result1, total page views since the beginning of time, and result2, average page views since the beginning of time
    d1 = datetime.strptime(start_all_time, "%Y%m%d")
    d2 = datetime.strptime(end_current_year, "%Y%m%d")
    days = (abs((d2 - d1).days) + 1)

    article = article.replace(" ", "_")
    total_views = 0

    try:
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{language}.wikipedia/all-access/user/{article}/daily/{start_all_time}/{end_current_year}"
        html = urlopen(url).read()

        ecc = 0

        if ecc == 0:
            html = str(html)
            html = html.replace('{"items":[', "")
            html = html.replace(']}', "")

            n = html.count("}")

            for i in range(n):
                txt = html[:html.find("}") + 1]
                total_views += int(txt[txt.find('"views":') + len('"views":'):-1])
                html = html.replace(txt, "", 1)

            result1 = str(total_views)
            result2 = str(int(round((total_views / days), 0)))

    except:
        result1 = "ERROR"
        result2 = "ERROR"

    # Calculate result3, average page views from the previous year
    result3 = get_avg_page_views(article, start_prev_year, end_prev_year)

    # Calculate result4, average page views from the current year
    result4 = get_avg_page_views(article, start_current_year, end_current_year)

    return str(result1), str(result2), str(result3), str(result4)


def name_to_q(item):
    return item.getID()


def count_notes(text):
    return str(text.count('</ref>'))


def calculate_size(text):
    return str(len(text))


def count_images(text):
    t = text.lower()
    img = str(
        t.count('.jpg') + t.count('.svg') + t.count('.jpeg') + t.count('.png') + t.count('.tiff') + t.count('.gif') +
        t.count('.tif') + t.count('.xcf'))
    return img


def get_first_edit(article):
    try:
        url = f"https://xtools.wmflabs.org/api/page/articleinfo/{language}.wikipedia.org/{article.replace(' ', '_')}"
        html = urlopen(url).read()
        html = str(html)
        html = html[html.find("created_at") + len("created_at") + 3:]
        html = html[:10]

    except:
        html = "ERROR"

    return html


def count_warnings(t):
    t_tmp = t
    t = t.replace("\n", "")
    t = t.replace(" ", "")
    t = t.lower()

    tmp_to_check = t.count('{{c|') + t.count('{{c}}')
    tmp_synoptic = t.count('{{tmp|') + t.count('{{tmp}}')
    tmp_help = t.count('{{a|')
    tmp_correct = t.count('{{correct')
    tmp_curiosity = t.count('{{curiosity')
    tmp_divide = t.count('{{d|') + t.count('{{d}')
    tmp_sources = t.count('{{f|') + t.count('{{f}}')
    tmp_localism = t.count('{{l|') + t.count('{{l}}')
    tmp_pov = t.count('{{p|') + t.count('{{p}}')
    tmp_nn = t.count('{{nn|') + t.count('{{nn}}')
    tmp_recentism = t.count('{{recentism')
    tmp_manual_style = t.count('{{manual style')
    tmp_translation = t.count('{{t|') + t.count('{{t}}')
    tmp_wikify = t.count('{{w|') + t.count('{{w}}')
    tmp_stub = t.count('{{s|') + t.count('{{s}}')
    tmp_stub_section = t.count('{{stub section')
    tmp_copy_control = t.count('{{copy control')

    total_warnings = tmp_to_check + tmp_synoptic + tmp_help + tmp_correct + tmp_curiosity + tmp_divide + tmp_sources + tmp_localism + tmp_pov
    total_warnings = total_warnings + tmp_nn + tmp_recentism + tmp_manual_style + tmp_translation + tmp_wikify + tmp_stub + tmp_stub_section + tmp_copy_control

    tmp_no_sources = t.count('{{no source') + t.count('{{citation needed') + t.count('{{no source}}') + t.count('{{citation needed}}')
    tmp_to_clarify = t.count('{{clarify') + t.count('{{clarify}}')

    return str(total_warnings), str(tmp_no_sources), str(tmp_to_clarify)


def find_template(text):
    tmp = text[2:]
    tmp2 = text[2:]
    tmp = tmp[:tmp.find("}}") + 2]

    if "{{" in tmp:
        tmp3 = tmp[tmp.find("{{"):]
        tmp2 = tmp2.replace(tmp3, "$$$$$$$$$$$$$$")
        tmp2 = tmp2[:tmp2.find("}}") + 2]
        tmp2 = tmp2.replace("$$$$$$$$$$$$$$", tmp3)
        return tmp2

    return tmp


def calculate_incipit_length(text):
    incipit = text
    incipit = incipit[:incipit.find("\n==")]
    n_template = incipit.count('{{')
    incipit_clear = incipit
    fn = incipit.count("{{formatnum:")

    for i in range(fn):
        tmp = incipit[incipit.find("{{formatnum:"):]

        tmp = tmp[:tmp.find("}}") + 2]
        tmp2 = tmp.replace("{{formatnum:", "")
        tmp2 = tmp2.replace("}}", "")
        incipit = incipit.replace(tmp, tmp2)

    n_template = incipit.count("{{")

    for i in range(n_template):
        text = incipit[incipit.find("{{"):]
        template = find_template(text)
        text = text.replace("{{" + template, "")
        incipit = incipit.replace("{{" + template, "")

    incipit = incipit.replace("</ref>", "")
    n = incipit.count("<ref")

    for i in range(n):
        tmp = incipit[incipit.find("<ref"):]

        tmp = tmp[:tmp.find(">") + 1]
        incipit = incipit.replace(tmp, "")

    incipit = incipit.replace("[[", "")
    incipit = incipit.replace("]]", "")
    incipit = incipit.replace("|", "")
    incipit_length = len(incipit)

    return str(incipit_length)


def is_good_article(text):
    if good_article_template in text.lower():
        return "1"
    else:
        return "0"


def is_featured_article(text):
    if featured_template in text.lower():
        return "1"
    else:
        return "0"


def analysis():
    f = open('query.csv', "r")
    vox = f.readlines()

    # Clear the contents of the file before starting
    results = open('results.txt', "w")
    results.truncate(0)
    results.close()

    for voce in vox:
        results = open('results.txt', 'a')  # open the file in append mode
        voce = voce[:-1]
        voce = voce.replace(" ", "_")
        result = ""

        wikitext = ""

        voce2 = urllib.parse.quote(voce)
        voce = voce.replace(" ", "_")

        try:
            url = f"https://{language}.wikipedia.org/w/api.php?action=parse&page={voce2}&prop=wikitext&formatversion=2&format=json"
            json_url = urlopen(url)
            data = json.loads(json_url.read())
            wikitext = data["parse"]["wikitext"]

            if "#REDIRECT" in wikitext:
                voce2 = wikitext[wikitext.find("[[") + 2:]
                voce2 = voce2[:voce2.find("]]")]
                voce = voce2
                voce2 = voce2.replace("_", " ")

        except:
            pass

        try:
            voce2 = urllib.parse.quote(voce)
            voce = voce.replace(" ", "_")

            url = f"https://{language}.wikipedia.org/w/api.php?action=query&titles={voce2}&prop=pageprops&format=json&formatversion=2"
            json_url = urlopen(url)
            data = json.loads(json_url.read())
            wikidata_id = data["query"]["pages"][0]["pageprops"]["wikibase_item"]
            url = f"https://www.wikidata.org/wiki/Special:EntityData/{wikidata_id}.json"
            json_url = urlopen(url)
            wikidata = json.loads(json_url.read())
            url = f"https://{language}.wikipedia.org/w/api.php?action=parse&page={voce2}&prop=wikitext&formatversion=2&format=json"
            json_url = urlopen(url)
            data = json.loads(json_url.read())
            wikitext = data["parse"]["wikitext"]

            try:
                url = f"https://{language}.wikipedia.org/w/api.php?action=parse&page={discussion_url}{voce2}&prop=wikitext&formatversion=2&format=json"
                json_url = urlopen(url)
                data = json.loads(json_url.read())
                wikitext_discussion = data["parse"]["wikitext"]
            except:
                wikitext_discussion = ""

            result = result + voce + "\t"
            result = result + wikidata_id + "\t"

        except:
            result = result + voce + "\t" + "Nonexistent Entry"

        else:
            if first_edit:
                result = result + get_first_edit(voce2) + "\t"

            if size:
                result = result + calculate_size(wikitext) + "\t"

            if images:
                result = result + count_images(wikitext) + "\t"

            if notes:
                result = result + count_notes(wikitext) + "\t"

            if warnings_config:
                for i in count_warnings(wikitext):
                    print("some warnings")
                    result = result + i + "\t"

            if dimensioneDiscussione:
                result = result + calculate_size(wikitext_discussion) + "\t"

            if dimensioneIncipit:
                result = result + calculate_incipit_length(wikitext) + "\t"

            if visits:
                for i in visits(voce2):
                    result = result + i + "\t"

            if review:
                result = result + is_good_article(wikitext) + "\t"

            if featured:
                result = result + is_featured_article(wikitext) + "\t"

            if commons_gallery:
                try:
                    result = result + wikidata["entities"][wikidata_id]["claims"]["P373"][0]["mainsnak"]["datavalue"][
                        "value"] + "\t"
                except:
                    result = result + "" + "\t"

            if commons_page:
                try:
                    result = result + wikidata["entities"][wikidata_id]["claims"]["P935"][0]["mainsnak"]["datavalue"][
                        "value"] + "\t"
                except:
                    result = result + "" + "\t"

            if wikisource:
                try:
                    result = result + wikidata["entities"][wikidata_id]["sitelinks"]["itwikisource"]["title"] + "\t"
                except:
                    result = result + "\t"

            if coordinates:
                try:
                    result = result + wikidata["entities"][wikidata_id]["claims"]["P625"][0]["mainsnak"]["datavalue"][
                        "value"]["latitude"] + "\t"
                    result = result + wikidata["entities"][wikidata_id]["claims"]["P625"][0]["mainsnak"]["datavalue"][
                        "value"]["longitude"] + "\t"
                except:
                    result = result + "\t" + "\t"

        results.write(result + "\n")  # add a newline after each result
        results.close()  # close the file
        print(result)


def main():
    analysis()


if __name__ == "__main__":
    main()