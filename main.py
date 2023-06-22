import inquirer
from inquirer.themes import GreenPassion
from termcolor import colored
from halo import Halo
from utils.api_utils import generate_essay
from utils.pdf_utils import save_essay_as_pdf
from rgbprint import gradient_print, Color

# Print the title
ascii_art = """\
 ██████╗ ██████╗ ████████╗    ███████╗███████╗███████╗ █████╗ ██╗   ██╗
██╔════╝ ██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝
██║  ███╗██████╔╝   ██║       █████╗  ███████╗███████╗███████║ ╚████╔╝ 
██║   ██║██╔═══╝    ██║       ██╔══╝  ╚════██║╚════██║██╔══██║  ╚██╔╝  
╚██████╔╝██║        ██║       ███████╗███████║███████║██║  ██║   ██║   
 ╚═════╝ ╚═╝        ╚═╝       ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   
"""

goodbye = """
 ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗
██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝
██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  
██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  
╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗
 ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝
"""

from rgbprint import gradient_print, Color
gradient_print(
    ascii_art,
    start_color=Color.light_green, 
    end_color=Color.dark_green
)

gradient_print(
    "Version Alpha 0.1.0\nBy: Kalmix",
    start_color=Color.light_green, 
    end_color=Color.dark_green
)


def prompt_essay_topic():
    prompt = input(colored("[📜] Enter the essay topic (Only the topic, e.g., Quantum Physics): ", "green"))
    return prompt


def select_model():
    model_choices = [
        inquirer.List(
            'model',
            message="Select a model [🤖]",
            choices=[
                'Text Davinci 003',
                'GPT-4',
                'GPT-3.5 Turbo'
            ],
        ),
    ]

    model_choice = inquirer.prompt(model_choices, theme=GreenPassion())['model']

    model_map = {
        'Text Davinci 003': 'text-davinci-003',
        'GPT-4': 'gpt-4',
        'GPT-3.5 Turbo': 'gpt-3.5-turbo'
    }

    model = model_map.get(model_choice)
    if not model:
        print("Invalid model choice.")
        exit()

    return model


def main():
    while True:
        prompt = prompt_essay_topic()
        model = select_model()

        # Generate the essay
        with Halo(text='Generating your essay [📜]', spinner='dots2', text_color="green"):
            essay = generate_essay(prompt, model)

        if essay:
            print(colored("[📜] Generated Essay:", "green"))
            print(essay)

            # Choose whether to export to PDF
            export_choices = [
                inquirer.List(
                    'export',
                    message="Export to PDF? [📖]",
                    choices=[
                        'Yes',
                        'No'
                    ],
                ),
            ]

            export_choice = inquirer.prompt(export_choices, theme=GreenPassion())['export']

            if export_choice == "Yes":
                output_path = save_essay_as_pdf(essay, essay.splitlines()[0])
                print(colored("[✅] PDF saved successfully (Ctrl + Click to go to Path):", "green"), output_path)
            else:
                print(colored("[❌] PDF not exported.", "red"))

        # Ask if the user wants to do another generation
        repeat_choices = [
            inquirer.List(
                'repeat',
                message="Do you want to generate another essay? [🔁]",
                choices=[
                    'Yes',
                    'No'
                ], 
            ),
        ]

        repeat_choice = inquirer.prompt(repeat_choices, theme=GreenPassion())['repeat']

        if repeat_choice == 'No':
            gradient_print(
                goodbye,
                start_color=Color.light_green, 
                end_color=Color.dark_green
            )
            break



if __name__ == '__main__':
    main()
