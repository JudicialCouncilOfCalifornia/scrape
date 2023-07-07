from utils.gpt import Gpt, Regex

justicesAi = Gpt("dca-justices-pdf.csv")
justicesDataframe = justicesAi.get_df()

divisionRegex = Regex('(Division\ (?i)[One|Two|Three|Four|Five|Six|1|2|3|4|5|6]*)')
roleRegex = Regex('(?i)(Presiding|Associate)\ Justice')

for i in justicesDataframe.index:

    print("\nPROCESSING: " + justicesDataframe['title'][i])

    if justicesAi.isnull(justicesDataframe['ocr'][i]):

        try:
            justicesDataframe.at[i, 'ocr'] = text = justicesAi.pdftotext(justicesDataframe['url'][i])
            print('--- ocr:', text[0:20] + '...')

        except Exception as err:
            print('--- oct FAILED: ' + justicesDataframe['title'][i])
            print(f"--- Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['body'][i]) and justicesDataframe['ocr'][i]:

        try:
            prompt = "summarize this justice profile:\n\n"
            justicesDataframe.at[i, 'body'] = text = justicesAi.chatgpt(prompt + '"' + justicesAi.reducewords(justicesDataframe['ocr'][i], 2000) + '"')
            print('--- body:', text[0:20] + '...')

        except Exception as err:
            print('--- body FAILED:' + justicesDataframe['title'][i])
            print(f"--- Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['date'][i]) and justicesDataframe['ocr'][i]:

        try:
            prompt = "extract the justice appointment and resignation date in this format mm/dd/yyyy-mm/dd/yyyy:\n\n"
            justicesDataframe.at[i, 'date'] = text = justicesAi.chatgpt(prompt + '"' + justicesAi.reducewords(justicesDataframe['ocr'][i], 2000) + '"')
            print('--- date:', text)

        except Exception as err:
            print('--- date FAILED: ' + justicesDataframe['title'][i])
            print(f"--- Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['division'][i]) and justicesDataframe['ocr'][i]:

        try:
            justicesDataframe.at[i, 'division'] = division = divisionRegex(justicesDataframe['ocr'][i])
            print('--- division:', division)

        except Exception as err:
            print('--- division FAILED: ' + justicesDataframe['title'][i])
            print(f"--- Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['role'][i]) and justicesDataframe['ocr'][i]:

        try:
            justicesDataframe.at[i, 'role'] = role = roleRegex(justicesDataframe['ocr'][i])
            print('--- role:', role)

        except Exception as err:
            print('--- role FAILED: ' + justicesDataframe['title'][i])
            print(f"--- Unexpected {err=}, {type(err)=}")
            pass

justicesDataframe.to_csv("dca-justices-pdf.csv", index=False)