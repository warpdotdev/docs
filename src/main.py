from config import settings
import importlib

from python_starter.python_starter import *

DATA: str = "data"
FILTER_CONDITIONS: str = "filter_conditions"
MODEL_MODULE_NAME: str = "model_module_name"
OUTPUT: str = "output"


def main():
    set_error_folder("../logs/")
    set_error_file_origin("main.py")
    set_error_task_origin("main")

    input_folder: str = settings.input_directory
    output_folder: str = settings.output_directory
    generate_sub_paths_for_folder(output_folder)

    models = settings.models
    markdown: List[str] = [
        "# Open Source License Dependencies",
        "\n\n",
        "These are the licenses of third-party libraries that Warp depends on.",
        "\n\n",
    ]
    for model_name in models:
        model_data = models.get(model_name)
        model_module_name: str = model_data.get(MODEL_MODULE_NAME)
        module = importlib.import_module(model_module_name)

        model_filter_conditions: list[str] = model_data.get(FILTER_CONDITIONS)
        data_filename: str = import_single_file(
            folder=input_folder,
            list_filename_filter_conditions=tuple(model_filter_conditions),
        )
        model = module.Model.parse_file(
            os.path.join(
                input_folder,
                data_filename,
            )
        )
        model_markdown = model.as_markdown()
        del model
        markdown.extend(model_markdown)

    output_filename = generate_filename(
        nt_filename=(settings.output_filename), folder=output_folder
    )
    with open(output_filename, "w") as f:
        f.writelines(markdown)

    if __name__ == "__main__":
        main()
