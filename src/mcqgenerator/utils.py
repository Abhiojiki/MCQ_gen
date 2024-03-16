import os
import PyPDF2
import json
import traceback
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception(
        "unsupported file format only pdf and text file suppoted"
        )
def get_table_data(quiz_str):
    try:
        print(quiz_str)
        # Convert the quiz from a str to dict
        start_idx = quiz_str.find('{"1":')

# Extract the JSON part from the string
        json_part = quiz_str[start_idx:]
        print(json_part)
        quiz_dict = json.loads(json_part)

        quiz_table_data = []

        # Iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                f" {option} -> {option_value}" for option, option_value in value["options"].items()
            )
            correct = value["correct"]

            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        # Handle any exceptions that occur during the process
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
        