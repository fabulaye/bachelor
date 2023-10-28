import sys
sys.path.append("C:/Users/lukas/Documents/GitHub/bachelor")

def import_all_libraries():
    import file_manager
    import cleaner
    import auto_account
    import txt_pdf 

def import_file_manager():
    from file_manager import change_directory
    from file_manager import del_jpg
    from file_manager import dict_to_json
    from file_manager import json_to_dict
    from file_manager import determine_file_type

def import_cleaner():
    None
def import_txt_pdf():
    from txt_pdf import pdf_to_txt
    from txt_pdf import read_txt    




