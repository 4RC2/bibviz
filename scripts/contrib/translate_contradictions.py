from googletrans import Translator
import bcolors
import copy
import html
import json
import shutil

DIRECTORY_DATA = "../../web/contents/data"
LOCALE_INPUT = "en"
LOCALE_OUTPUT = "hu"

translator = Translator()

with open(DIRECTORY_DATA + "/contra.json", "r") as file_input:
    data_input = json.load(file_input)
    data_output = copy.deepcopy(data_input)
    for source in data_input.items():
        i = -1
        for contradiction in source[1]["contradictions"]:
            i += 1
            description_input = html.unescape(contradiction["desc"])
            description_output = None
            while description_output is None:
                try:
                    description_output = translator.translate(description_input, dest=LOCALE_OUTPUT,
                                                              src=LOCALE_INPUT).text
                    data_output[source[0]]["contradictions"][i]["desc"] = html.escape(description_output)
                    print("{}_{:03}/{}: {}{}{} => {}{}{}".format(source[0],
                                                                 i + 1,
                                                                 len(source[1]["contradictions"]),
                                                                 bcolors.OK, description_input, bcolors.ENDC,
                                                                 bcolors.ERR, description_output, bcolors.ENDC))
                    j = 0
                    for answer_input in contradiction["refs"]:
                        j += 1
                        answer_output = None
                        while answer_output is None:
                            try:
                                answer_output = translator.translate(answer_input, dest=LOCALE_OUTPUT,
                                                                     src=LOCALE_INPUT).text
                                data_output[source[0]]["contradictions"][i]["refs"][html.escape(answer_output)] = \
                                    data_output[source[0]]["contradictions"][i]["refs"].pop(answer_input)
                                print("- {}/{}: {}{}{} => {}{}{}".format(j,
                                                                         len(contradiction["refs"]),
                                                                         bcolors.OK, answer_input, bcolors.ENDC,
                                                                         bcolors.ERR, answer_output, bcolors.ENDC))
                            except Exception:
                                pass
                except Exception:
                    pass
shutil.move("{}/{}.json".format(DIRECTORY_DATA, "contra"), "{}/{}.json.bak".format(DIRECTORY_DATA, "contra"))

with open("{}/{}.json".format(DIRECTORY_DATA, "contra"), "w", encoding="utf8") as file_output:
    json.dump(data_output, file_output, ensure_ascii=False, indent=2)
