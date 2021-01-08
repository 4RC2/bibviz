from googletrans import Translator
import bcolors
import html
import json
import shutil

DIRECTORY_LOCALES = "../../web/locales"
LOCALE_INPUT = "en"
LOCALE_OUTPUT = "hu"

translator = Translator()
data_output = {}

with open("{}/{}.json".format(DIRECTORY_LOCALES, LOCALE_INPUT), "r") as file_input:
    data_input = json.load(file_input)
    i = 0
    for k, v in dict(data_input).items():
        i += 1
        text_input = html.unescape(v)
        while k not in data_output.keys():
            try:
                text_output = translator.translate(text_input, dest=LOCALE_OUTPUT, src=LOCALE_INPUT).text
                text_output = text_output.replace("{{", "{{ ").replace("}}", " }}")
                data_output[k] = html.escape(text_output)
            except Exception:
                pass
        print("{:03}/{}: {}{}{} => {}{}{}".format(i,
                                                  len(data_input),
                                                  bcolors.OK, text_input, bcolors.ENDC,
                                                  bcolors.ERR, text_output, bcolors.ENDC))
shutil.move("{}/{}.json".format(DIRECTORY_LOCALES, LOCALE_INPUT),
            "{}/{}.json.bak".format(DIRECTORY_LOCALES, LOCALE_INPUT))

with open("{}/{}.json".format(DIRECTORY_LOCALES, LOCALE_INPUT), "w", encoding="utf8") as file_output:
    json.dump(data_output, file_output, ensure_ascii=False, indent=2)
