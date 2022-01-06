from config import settings
import importlib

from python_starter.python_starter import *

DATA: str = "data"
DATA_FILTER_CONDITIONS: str = "data_filter_conditions"
MODEL_MODULE_NAME: str = "model_module_name"
MODEL_OUTPUT_DIRECTORY: str = "model_output_directory"
MODEL_OUTPUT_FILENAME: str = "model_output_filename"
OUTPUT: str = "output"


def main():
    set_error_folder(settings.error_directory)
    set_error_file_origin(os.path.basename(__file__).rstrip(".py"))
    set_error_task_origin("main")

    data_directory: str = settings.data_directory

    tasks = settings.tasks
    for task_name in tasks:
        task_data = tasks.get(task_name)
        if not task_data:
            continue

        markdown_header: str
        try:
            markdown_header = task_data.markdown_header
        except Exception:
            markdown_header = ""

        markdown: List[str] = [markdown_header]
        for model_name in task_data.models:
            model = task_data.get(model_name)
            model_module_name: str = model.model_module_name
            module = importlib.import_module(model_module_name)

            model_filter_conditions: list[str] = model.get(DATA_FILTER_CONDITIONS)
            data_filename: str = import_single_file(
                folder=data_directory,
                list_filename_filter_conditions=tuple(model_filter_conditions),
            )
            model = module.Model.parse_file(
                os.path.join(
                    data_directory,
                    data_filename,
                )
            )
            model_markdown = model.as_markdown()
            del model
            markdown.extend(model_markdown)

        output_folder: str = task_data.get(MODEL_OUTPUT_DIRECTORY)
        generate_sub_paths_for_folder(output_folder)

        output_filename = generate_filename(
            nt_filename=(task_data.get(MODEL_OUTPUT_FILENAME)),
            folder=output_folder,
        )
        with open(output_filename, "w") as f:
            f.writelines(markdown)


if __name__ == "__main__":
    main()
