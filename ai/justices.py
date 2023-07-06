from utils.gpt import Gpt

justicesAi = Gpt("dca-justices.csv")
justicesDataframe = justicesAi.get_df()

for i in justicesDataframe.index:

    if justicesAi.isnull(justicesDataframe['date'][i]):

        try:
            print('PROCESSING: ' + justicesDataframe['url'][i])
            text = justicesDataframe['text'][i]

            if text:
                print('-- Extracting Date Range')
                prompt = "Extract the appointed date and resigned date from this text in this format mm/dd/yyyy-mm/dd/yyyy:\n\n"
                answer = justicesAi.chatgpt(prompt + text)
                justicesDataframe.at[i, 'date'] = answer if "Response Error" not in answer else None
                print(answer)

        except Exception as err:
            print('FAILED: ' + justicesDataframe['url'][i])
            print(f"Unexpected {err=}, {type(err)=}")
            pass

justicesDataframe.to_csv("dca-justices.csv", index=False)