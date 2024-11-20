import re
import shutil
import sys
import os
import traceback  # noqa
from time import sleep

if __name__ == '__main__':
    sys.path.append(os.getcwd())

from core.constants import *
from core.utils.i18n import Locale

config_filename = 'config.toml'


def generate_config(file_path, language):
    config_code_list = {}
    path_ = os.path.join(file_path, config_filename)

    dir_list = ['bots', 'core', 'modules', 'schedulers']
    exclude_dir_list = [os.path.join('core', 'config'), os.path.join('core', 'scripts')]

    match_code = re.compile(r'(Config\()', re.DOTALL)

    # create empty config.toml

    with open(path_, 'w', encoding='utf-8') as f:
        f.write(
            f'default_locale = "{language}" # {
                Locale(language).t(
                    'config.comments.default_locale',
                    fallback_failed_prompt=False)}\n')
        f.write(
            f'config_version = {
                str(config_version)} # {
                Locale(language).t(
                    'config.comments.config_version',
                    fallback_failed_prompt=False)}\n')
        f.write('initialized = false\n')
        f.close()

    from core.config import Config, CFGManager  # noqa

    CFGManager.switch_config_path(file_path)

    for dir in dir_list:
        for root, dirs, files in os.walk(dir):
            if root in exclude_dir_list:
                continue
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        if f := match_code.finditer(code):  # Find all Config() functions in the code
                            for m in f:
                                left_brackets_count = 0
                                param_text = ''
                                for param in code[m.end(
                                ):]:  # Get the parameters text inside the Config() function by counting brackets
                                    if param == '(':
                                        left_brackets_count += 1
                                    elif param == ')':
                                        left_brackets_count -= 1
                                    if left_brackets_count == -1:
                                        break
                                    param_text += param
                                config_code_list[param_text] = file_path

    for c in config_code_list:
        if c.endswith(','):
            c = c[:-1]
        c += ', _generate=True'  # Add _generate=True param to the end of the config function
        try:
            eval(f'Config({c})')  # Execute the code to generate the config file, yeah, just stupid but works
        except (NameError, TypeError):
            # traceback.print_exc()
            ...

    CFGManager.write('initialized', True)


if not os.path.exists(os.path.join(config_path, config_filename)) and __name__ != '__main__':
    while True:
        i = 1
        lang = input(
            f"""Hello, it seems you are first time to run Akari-bot, what language do you want to use by default?
{''.join([f"{i}. {lang_list[list(lang_list.keys())[i - 1]]}\n" for i in range(1, len(lang_list) + 1)])}
Please input the number of the language you want to use:""")
        if (langI := (int(lang) - 1)) in range(len(lang_list)):
            lang = list(lang_list.keys())[langI]
            break
        else:
            print('Invalid input, please try again.')

    generate_config(config_path, lang)

    sleep(1)
    print('Config file generated successfully, please modify the config file according to your needs.')
    print('The config file is located at ' + config_path)
    print('Please restart the bot after modifying the config file.')
    print('Press enter to exit.')
    input()
    exit(0)


if __name__ == '__main__':
    import zipfile
    config_store_path = os.path.join(assets_path, 'config_store')
    config_store_packed_path = os.path.join(assets_path, 'config_store_packed')
    shutil.rmtree(config_store_path, ignore_errors=True)
    shutil.rmtree(config_store_packed_path, ignore_errors=True)
    if not os.path.exists(config_store_path):
        os.makedirs(config_store_path)
    if not os.path.exists(config_store_packed_path):
        os.makedirs(config_store_packed_path)
    for lang in lang_list:
        config_store_path_ = os.path.join(config_store_path, lang)
        if not os.path.exists(config_store_path_):
            os.makedirs(config_store_path_)
        generate_config(config_store_path_, lang)
        zipfile.ZipFile(os.path.join(config_store_packed_path, lang + '.zip'), 'w').write(config_store_path_)
    print('Config files generated successfully.')
