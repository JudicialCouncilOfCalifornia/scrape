from utils.gpt import Gpt, Regex

justicesAi = Gpt("dca-justices-pdf.csv")
justicesDataframe = justicesAi.get_df()

divisionRegex = Regex('(Division\ (?i)[One|Two|Three|Four|Five|Six|1|2|3|4|5|6]*)')
roleRegex = Regex('(?i)(Presiding|Associate)\ Justice')

for i in justicesDataframe.index:

    print('PROCESSING: ' + justicesDataframe['title'][i])

    if justicesAi.isnull(justicesDataframe['ocr'][i]):

        try:
            justicesDataframe.at[i, 'ocr'] = text = justicesAi.pdftotext(justicesDataframe['url'][i])
            print('--- ocr: ' + text[0:10])

        except Exception as err:
            print('--- FAILED: ' + justicesDataframe['title'][i])
            print(f"Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['body'][i]):

        try:
            prompt = "write a biography using all the info:\n\n"
            justicesDataframe.at[i, 'body'] = text = justicesAi.chatgpt(prompt + '"' + justicesDataframe['ocr'][i] + '"')
            print('--- body: ' + text[0:10])

        except Exception as err:
            print('--- FAILED: ' + justicesDataframe['title'][i])
            print(f"Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['date'][i]):

        try:
            prompt = "extract the justice appointment and resignation date in this format mm/dd/yyyy-mm/dd/yyyy:\n\n"
            justicesDataframe.at[i, 'date'] = text = justicesAi.chatgpt(prompt + justicesDataframe['body'][i])
            print('--- date: ' + text)

        except Exception as err:
            print('--- FAILED: ' + justicesDataframe['title'][i])
            print(f"Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['division'][i]):

        try:
            print('PROCESSING DIVISION: ' + justicesDataframe['title'][i])
            justicesDataframe.at[i, 'division'] = division = divisionRegex(justicesDataframe['body'][i])
            print('--- division' + division)

        except Exception as err:
            print('--- FAILED: ' + justicesDataframe['title'][i])
            print(f"Unexpected {err=}, {type(err)=}")
            pass

    if justicesAi.isnull(justicesDataframe['role'][i]):

        try:
            justicesDataframe.at[i, 'role'] = role = roleRegex(justicesDataframe['body'][i])
            print('--- role' + role)

        except Exception as err:
            print('FAILED: ' + justicesDataframe['title'][i])
            print(f"Unexpected {err=}, {type(err)=}")
            pass

justicesDataframe.to_csv("dca-justices-pdf.csv", index=False)