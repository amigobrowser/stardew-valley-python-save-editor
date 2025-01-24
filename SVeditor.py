from lxml import etree
import os
import re
import shutil
import datetime

def get_current_value(root, tag):
    for elem in root.iter(tag):
        return elem.text
    return None

def update_element_value(xml_file, tag, new_value):
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(xml_file, parser)
    root = tree.getroot()

    for elem in root.iter(tag):
        elem.text = str(new_value)
        break  # Update only the first occurrence

    tree.write(xml_file, encoding="utf-8", xml_declaration=True, pretty_print=False)
    print(f"Value of {tag} in file {xml_file} has been updated to {new_value}")

def find_files(directory, pattern):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        # Ignore the SAVE_BACKUP folder
        if "SAVE_BACKUP" in dirnames:
            dirnames.remove("SAVE_BACKUP")

        for file_name in filenames:
            if re.match(pattern, file_name):
                files.append(os.path.join(dirpath, file_name))
    return files

def create_backup(xml_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(script_dir, "SAVE_BACKUP")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    base_name = os.path.basename(xml_file)
    backup_name = f"{current_time}_{base_name}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    shutil.copy2(xml_file, backup_path)
    print(f"Backup of the file has been created: {backup_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pattern = r".*_\d{9}$"

    files = find_files(script_dir, pattern)

    if not files:
        print("No files found matching the specified pattern.")
    else:
        print("The following files were found:")
        for i, file_name in enumerate(files, start=1):
            print(f"{i}. {file_name}")

        choice = input("Select the file number to edit: ")
        try:
            chosen_file = files[int(choice) - 1]
            xml_file_path = chosen_file
            save_game_info_path = os.path.join(os.path.dirname(xml_file_path), "SaveGameInfo")

            create_backup(xml_file_path)
            if os.path.exists(save_game_info_path):
                create_backup(save_game_info_path)
            
            while True:
                command = input("Available actions: \n money - edit current gold amount \n totalmoney - edit amount of money ever earned \n player name - edit player name \n farm name - edit farm name \n favorite name - edit favorite thing \n house level - edit your house level \n skills - open skill edition page \n about - about this script \n exit - close script \n").strip().lower()
                if command == "money":
                    parser = etree.XMLParser(remove_blank_text=False)
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()
                    current_value = get_current_value(root, 'money')
                    print(f"Current value of money: {current_value}")

                    while True:
                        new_value = input("Enter the new value for money (numbers only): ")
                        if new_value.isdigit():
                            break
                        else:
                            print("Please enter a valid numeric value.")
                    update_element_value(xml_file_path, 'money', new_value)
                    if os.path.exists(save_game_info_path):
                        update_element_value(save_game_info_path, 'money', new_value)
                elif command == "player name":
                    parser = etree.XMLParser(remove_blank_text=False)
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()
                    current_value = get_current_value(root, 'name')
                    print(f"Current value of name: {current_value}")

                    new_value = input("Enter the new value for name: ")
                    update_element_value(xml_file_path, 'name', new_value)
                    if os.path.exists(save_game_info_path):
                        update_element_value(save_game_info_path, 'name', new_value)
                elif command == "farm name":
                    parser = etree.XMLParser(remove_blank_text=False)
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()
                    current_value = get_current_value(root, 'farmName')
                    print(f"Current value of farmName: {current_value}")

                    new_value = input("Enter the new value for farmName: ")
                    update_element_value(xml_file_path, 'farmName', new_value)
                    if os.path.exists(save_game_info_path):
                        update_element_value(save_game_info_path, 'farmName', new_value)
                elif command == "favorite name":
                    parser = etree.XMLParser(remove_blank_text=False)
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()
                    current_value = get_current_value(root, 'favoriteThing')
                    print(f"Current value of favoriteThing: {current_value}")

                    new_value = input("Enter the new value for favoriteThing: ")
                    update_element_value(xml_file_path, 'favoriteThing', new_value)
                    if os.path.exists(save_game_info_path):
                        update_element_value(save_game_info_path, 'favoriteThing', new_value)
                elif command == "totalmoney":
                    parser = etree.XMLParser(remove_blank_text=False)
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()
                    current_value = get_current_value(root, 'totalMoneyEarned')
                    print(f"Current value of totalMoneyEarned: {current_value}")

                    while True:
                        new_value = input("Enter the new value for totalMoneyEarned (numbers only): ")
                        if new_value.isdigit():
                            break
                        else:
                            print("Please enter a valid numeric value.")
                    update_element_value(xml_file_path, 'totalMoneyEarned', new_value)
                    if os.path.exists(save_game_info_path):
                        update_element_value(save_game_info_path, 'totalMoneyEarned', new_value)
                elif command == "house level":
                    parser = etree.XMLParser(remove_blank_text=False)
                    tree = etree.parse(xml_file_path, parser)
                    root = tree.getroot()
                    current_value = get_current_value(root, 'houseUpgradeLevel')
                    print(f"Current value of houseUpgradeLevel: {current_value}")

                    while True:
                        new_value = input("Enter the new value for houseUpgradeLevel (0-2): ")
                        if new_value.isdigit() and 0 <= int(new_value) <= 2:
                            break
                        else:
                            print("Please enter a valid number between 0 and 2.")
                    update_element_value(xml_file_path, 'houseUpgradeLevel', new_value)
                    if os.path.exists(save_game_info_path):
                        update_element_value(save_game_info_path, 'houseUpgradeLevel', new_value)
                elif command == "skills":
                    while True:
                        skill_command = input("Enter a skill command (farming, mining, combat, foraging, fishing or back): ").strip().lower()
                        skill_tags = {
                            "farming": "farmingLevel",
                            "mining": "miningLevel",
                            "combat": "combatLevel",
                            "foraging": "foragingLevel",
                            "fishing": "fishingLevel"
                        }
                        if skill_command in skill_tags:
                            skill_tag = skill_tags[skill_command]
                            while True:
                                new_value = input(f"Enter the new value for {skill_command} (0-10): ")
                                if new_value.isdigit() and 0 <= int(new_value) <= 10:
                                    break
                                else:
                                    print("Please enter a valid number between 0 and 10.")
                            update_element_value(xml_file_path, skill_tag, new_value)
                            if os.path.exists(save_game_info_path):
                                update_element_value(save_game_info_path, skill_tag, new_value)
                        elif skill_command == "back":
                            break
                        else:
                            print("Unknown command. Please enter either 'farming', 'mining', 'combat', 'foraging', 'fishing' or 'back'.")
                elif command == "about":
                    print("(C) 2025 \nmade by amigobrowser and copilot AI")
                elif command == "exit":
                    print("Exiting the program.")
                    break
                else:
                    print("Unknown command. Please enter either 'money', 'player name', 'farm name', 'favorite name', 'totalmoney', 'house level', 'skills', 'about' or 'exit'.")
        except (IndexError, ValueError):
            print("Invalid file selection.")