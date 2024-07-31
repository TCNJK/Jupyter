# read html
import os
from bs4 import BeautifulSoup

# Define the directory containing the HTML files
directory_path = "D:/Code/Python/Jupyter/notebook/quiz"

# Define the path for the output text file
output_file_path = os.path.join("D:/Code/Python/Jupyter/notebook", "all_questions_output.txt")

# Initialize the list to store formatted questions and answers
all_questions_with_options = []

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".html"):
        file_path = os.path.join(directory_path, filename)

        # Load the HTML content
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Locate all question blocks
        question_blocks = soup.find_all("div", class_="rc-FormPartsQuestion")

        for idx, block in enumerate(question_blocks, 1):
            # Extract the question text from the first content cell
            content_cells = block.find_all("div", class_="rc-FormPartsQuestion__contentCell")
            if len(content_cells) < 2:
                continue  # Skip if there's not enough data

            question_text = content_cells[0].get_text(" ", strip=True)

            # Extract options from the second content cell
            options_block = content_cells[1]
            option_elements = options_block.find_all("div", class_="rc-Option--isReadOnly")
            options_texts = []
            correct_answers = []

            for i, option_element in enumerate(option_elements):
                option_text = option_element.find("div", class_="rc-Option__input-text").get_text(" ", strip=True)
                input_element = option_element.find("input")
                
                if input_element and input_element.has_attr("checked"):
                    correct_answers.append(chr(65 + i))

                options_texts.append(option_text)

            # Remove the .html extension from the filename
            clean_filename = os.path.splitext(filename)[0]

            # Format the question and the correct answer(s)
            formatted_question = f"{clean_filename} Q{idx}: {question_text} " + " ".join(
                [f"\n{chr(65+i)}. {opt}" for i, opt in enumerate(options_texts)]
            )
            if correct_answers:
                formatted_question += f" Answer: {', '.join(correct_answers)}"
            else:
                formatted_question += " Answer: No answer found"
            
            all_questions_with_options.append(formatted_question)

# Write all formatted questions and answers to the text file
with open(output_file_path, "w", encoding="utf-8") as f:
    for question in all_questions_with_options:
        f.write(f"{question}\n\n\n")

print(f"All data has been written to {output_file_path}.")
