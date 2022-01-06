import os
from collections import namedtuple
from datetime import datetime
from itertools import accumulate
from re import compile
from re import match
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import Iterator
from typing import List
from typing import NamedTuple
from typing import Pattern
from typing import Tuple

# GLOBAL VARIABLES
ERROR_FOLDER: str = ""
ERROR_LIST: List[str] = []
ERROR_FILE_ORIGIN: str = ""
ERROR_TASK_ORIGIN: str = ""
PARTITION_GROUP: int = 1
PARTITION_TOTAL: int = 1

NT_filename_errors = namedtuple(
    "NT_filename_errors",
    [
        "error_file_origin",
        "error_task_origin",
        "extension",
    ],
)


def cast(
    cast_object: Any,
    cast_type: str,
) -> Any:
    if cast_type == "str":
        return str(cast_object)
    elif cast_type == "int":
        return int(cast_object)
    elif cast_type == "float":
        return float(cast_object)
    elif cast_type == "bool":
        return bool(cast_object)
    else:
        log_error(
            error=f"Cast Type: {cast_type} not found. Returning original argument: {cast_object}"
        )
        return cast_object


def filter_list_strings(
    list_strings: Iterable[str],
    list_string_filter_conditions: Tuple[str, ...] = (),
) -> Iterable[str]:
    if len(list_string_filter_conditions) > 0:
        list_strings = filter(
            lambda x: all(
                str(condition) in x for condition in list_string_filter_conditions
            ),
            list_strings,
        )

    return list_strings


def flatten_list(
    list_of_lists: List[List[Any]],
) -> List[Any]:
    item: Any
    sublist: List[Any]
    flat_list: List[Any] = [item for sublist in list_of_lists for item in sublist]

    return flat_list


def generate_filename(
    nt_filename: tuple,
    delimiter: str = "",
    folder: str = "",
) -> str:
    filename_extension: str
    filename_without_extension: Tuple[str, ...]
    try:
        filename_extension = nt_filename.extension
        filename_without_extension = tuple(
            x for x in nt_filename if x != filename_extension
        )

    except AttributeError as err:
        log_error(error=str(err))
        filename_extension = ""
        filename_without_extension: Tuple[str, ...] = nt_filename

    output: str = delimiter.join(filename_without_extension)
    if folder:
        output = folder + output
    if filename_extension:
        output = output + filename_extension

    return output


def generate_sub_paths_for_folder(
    folder: str,
) -> None:
    directories: List[str] = folder.split("/")
    recursive_sub_directories: Iterator[str] = accumulate(
        directories, lambda x, y: "/".join([x, y])
    )
    sub_directory: str
    for sub_directory in recursive_sub_directories:
        if not os.path.isdir(sub_directory):
            os.mkdir(sub_directory)


def is_single_item(
    list_items: List[Any],
) -> bool:
    match len(list_items):
        case 0:
            log_error(error="is_single_item-list_empty")
            return False
        case 1:
            return True
        case _:
            log_error(error="is_single_item-list_length_greater_than_1")
            return False


def import_paths_from_folder(
    folder: str,
    list_paths_filter_conditions: Tuple[str, ...] = (),
    check_paths: bool = False,
    include_files: bool = True,
    include_folders: bool = False,
    ignore_hidden: bool = True,
) -> Generator[str, None, List[str]]:
    if os.path.exists(folder):
        list_function_checks_all_true: List[Callable] = []
        list_function_checks_any_true: List[Callable] = []

        if check_paths:
            if ignore_hidden:
                pattern_to_ignore: Pattern[str] = compile(r"^\.[A-Za-z]")
                is_not_hidden_file_function: Callable[[str], bool] = lambda x: not bool(
                    match(pattern_to_ignore, x)
                )
                list_function_checks_all_true.append(is_not_hidden_file_function)
            if include_files:
                is_file_function: Callable[[str], bool] = lambda x: os.path.isfile(
                    f"{folder}{x}"
                )
                list_function_checks_any_true.append(is_file_function)
            if include_folders:
                is_folder_function: Callable[[str], bool] = lambda x: os.path.isdir(
                    f"{folder}{x}"
                )
                list_function_checks_any_true.append(is_folder_function)
        if len(list_paths_filter_conditions) > 0:
            filter_all_conditions_function: Callable[[str], bool] = lambda x: all(
                str(condition).lower() in str(x).lower()
                for condition in list_paths_filter_conditions
            )
            list_function_checks_all_true.append(filter_all_conditions_function)

        path: str
        for path in os.listdir(folder):
            bool_all_true_check: bool = True
            if len(list_function_checks_all_true) > 0:
                bool_all_true_check = all(
                    [
                        function_check(path)
                        for function_check in list_function_checks_all_true
                    ]
                )
            bool_any_true_check: bool = True
            if len(list_function_checks_any_true) > 0:
                bool_any_true_check = any(
                    [
                        function_check(path)
                        for function_check in list_function_checks_any_true
                    ]
                )
            if bool_all_true_check and bool_any_true_check:
                yield path
    else:
        generate_sub_paths_for_folder(
            folder=folder,
        )
        return []


def import_single_file(
    folder: str,
    list_filename_filter_conditions: Tuple[str, ...],
) -> str:
    filename: str
    list_rest: List[str]
    list_filenames: List[str] = list(
        import_paths_from_folder(
            folder=folder,
            list_paths_filter_conditions=list_filename_filter_conditions,
        )
    )
    single_file: bool = is_single_item(list_filenames)
    if not single_file:
        log_error(
            error=f"parse_filename-" f"{'_'.join(list_filename_filter_conditions)}"
        )
        return ""
    else:
        first_file: str
        rest_of_files: List[str]
        first_file, *rest_of_files = list_filenames
        return first_file


def partial_named_tuple_generator(
    named_tuple_template,
    data: dict,
) -> Callable:
    fields_to_keep: dict = {k: v for (k, v) in data.items()}

    return lambda params: named_tuple_template(**(params | fields_to_keep))


def set_error_folder(
    error_folder: str,
) -> None:
    global ERROR_FOLDER
    ERROR_FOLDER = error_folder
    print(f"error_folder : {error_folder}")


def set_error_file_origin(
    file_origin: str,
) -> None:
    global ERROR_FILE_ORIGIN
    ERROR_FILE_ORIGIN = file_origin
    print(f"file_origin : {file_origin}")


def set_error_task_origin(
    task_origin: str,
) -> None:
    global ERROR_TASK_ORIGIN
    ERROR_TASK_ORIGIN = task_origin
    if task_origin:
        print(f"task_origin : {task_origin}")


def write_errors_to_disk(
    clear_task_origin: bool = True,
    folder_error: str = ERROR_FOLDER,
    bool_suppress_print: bool = False,
    overwrite: bool = True,
) -> None:
    global ERROR_LIST
    error_task_origin: str
    error_file_origin: str
    if ERROR_FILE_ORIGIN:
        error_file_origin = ERROR_FILE_ORIGIN
    else:
        error_file_origin = "unknown"
        print(f"No file origin was specified for the error log.")
    if ERROR_TASK_ORIGIN:
        error_task_origin = ERROR_TASK_ORIGIN
    else:
        error_task_origin = "unknown"
        print(f"No task origin was specified for the error log.")

    output_filename: str = generate_filename(
        nt_filename=NT_filename_errors(
            error_file_origin=error_file_origin,
            error_task_origin=error_task_origin,
            extension=".txt",
        ),
        delimiter="-",
        folder=folder_error,
    )
    output_write_type: str
    if overwrite:
        output_write_type = "w+"
    elif os.path.exists(output_filename):
        output_write_type = "a+"
    else:
        output_write_type = "w+"

    with open(output_filename, output_write_type) as error_log_file:
        current_datetime: str = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        error_log_file.write(f"{current_datetime} : {error_task_origin}\n")
        error: str
        for error in ERROR_LIST:
            error_log_file.write(f"{error}\n")
        error_log_file.write("\n\n")

    ERROR_LIST = []
    if clear_task_origin:
        set_error_task_origin("")
    if not bool_suppress_print:
        print(f"Error log outputted to: {output_filename}")


def log_error(
    error: str,
    log: bool = False,
    bool_suppress_print: bool = False,
    should_exit: bool = False,
) -> None:
    global ERROR_LIST
    if error:
        ERROR_LIST.append(error)
    if not bool_suppress_print:
        if log:
            print(f"log: {error}")
        else:
            print(f"error: {error}")
    if should_exit:
        write_errors_to_disk()
        exit(1)


def cast_named_tuple(
    named_tuple: NamedTuple, named_tuple_template: NamedTuple, dt_dict: Dict[str, Any]
) -> NamedTuple:
    if not dt_dict:
        return named_tuple
    else:
        named_tuple_dict: Dict[str, Any] = named_tuple._asdict()
        list_casted_data: List[Any] = []
        for key, value in named_tuple_dict.items():
            cast_type: Any = dt_dict.get(key, None)
            if cast_type:
                casted_value: Any
                if callable(cast_type):
                    casted_value = cast_type(value)
                else:
                    casted_value = cast(
                        cast_object=value,
                        cast_type=cast_type,
                    )
                list_casted_data.append(casted_value)
            else:
                list_casted_data.append(value)
        return named_tuple_template(*list_casted_data)


def unwrap_filename_into_named_tuple(
    filename: str,
    delimiter: str,
    named_tuple_template,
    dt_dict: Dict[str, Any],
) -> NamedTuple:
    named_tuple_to_be_cast: NamedTuple
    if not delimiter:
        try:
            return cast_named_tuple(
                named_tuple=named_tuple_template(filename),
                named_tuple_template=named_tuple_template,
                dt_dict=dt_dict,
            )
        except TypeError:
            log_error(
                error=f"named_tuple_size_mismatch_without_delimiter-{filename}",
                should_exit=True,
            )
    else:
        split_filename: List[str] = filename.split(delimiter)
        try:
            return cast_named_tuple(
                named_tuple=named_tuple_template(*split_filename),
                named_tuple_template=named_tuple_template,
                dt_dict=dt_dict,
            )
        except TypeError:
            log_error(
                error=f"named_tuple_size_mismatch_with_delimiter-{filename}",
                should_exit=True,
            )


def parse_filename(
    filename: str,
    named_tuple_template: NamedTuple,  # NamedTuple annotation doesn't work when using it as a callable
    delimiter: str = "",
    dt_dict: Dict[str, Any] = None,
) -> tuple:
    EXTENSION: str = "extension"
    set_error_task_origin("parse_filename")
    if not filename:
        log_error(
            error=f"filename_is_empty",
            should_exit=True,
        )
    else:
        match filename.split("."):
            case _, _, *multiple_periods, _:
                if multiple_periods:
                    log_error(
                        error=f"filename_contains_multiple_periods-{filename}",
                        should_exit=True,
                    )
            case "", _:
                log_error(error=f"filename_is_hidden_file-{filename}", log=True)
                return unwrap_filename_into_named_tuple(
                    filename=filename,
                    delimiter=delimiter,
                    named_tuple_template=named_tuple_template,
                    dt_dict=dt_dict,
                )
            case _, "":
                log_error(error=f"filename_is_missing_extension-{filename}", log=True)
                return unwrap_filename_into_named_tuple(
                    filename=filename,
                    delimiter=delimiter,
                    named_tuple_template=named_tuple_template,
                    dt_dict=dt_dict,
                )
            case f, e:
                if EXTENSION not in named_tuple_template._fields:
                    log_error(
                        error=f"named_tuple_generator_is_missing_extensions_field-{named_tuple_template}",
                        should_exit=True,
                    )
                    return unwrap_filename_into_named_tuple(
                        filename=filename,
                        delimiter=delimiter,
                        named_tuple_template=named_tuple_template,
                        dt_dict=dt_dict,
                    )
                else:
                    partial_named_tuple = partial_named_tuple_generator(
                        named_tuple_template=named_tuple_template,
                        data={
                            EXTENSION: e,
                        },
                    )
                    return unwrap_filename_into_named_tuple(
                        filename=f,
                        delimiter=delimiter,
                        named_tuple_template=partial_named_tuple,
                        dt_dict=dt_dict,
                    )
            case _, _:
                log_error(error=f"Unmatched_case-{filename}", should_exit=True)
                return unwrap_filename_into_named_tuple(
                    filename=filename,
                    delimiter=delimiter,
                    named_tuple_template=named_tuple_template,
                    dt_dict=dt_dict,
                )


if __name__ == "__main__":
    set_error_file_origin(os.path.basename(__file__).rstrip(".py"))
    set_error_task_origin("main")
    log_error(
        error=f"Not meant to be run as a file. Aborting script.", should_exit=True
    )
