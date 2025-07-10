try:
    import pyautogui
    import cv2
    import pygetwindow as gw
    from PIL import ImageGrab
    import numpy as np
except ImportError as e:
    print(f"[!] Missing module: {e.name}")
    print("Run this to install everything:\n  pip install pyautogui opencv-python pygetwindow numpy pillow")
    exit(1)

import time
import os

def capture_bluestacks_window(window_title="BlueStacks App Player"):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window.isMinimized or not window.visible:
            print("[!] BlueStacks window is minimized or not visible.")
            return None

        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        img_np = np.array(screenshot)
        return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    except IndexError:
        print("[!] BlueStacks window not found.")
        return None

def find_button(screen, template_path, threshold=0.65):
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"[!] Template not found: {template_path}")
        return None

   
    if template.shape[2] == 4:
        template = template[:, :, :3]  

   
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)

    return None


def click_at(pos, window_title="BlueStacks App Player", double=False):
    window = gw.getWindowsWithTitle(window_title)[0]
    x, y = pos
    click_x = window.left + x
    click_y = window.top + y

    pyautogui.moveTo(click_x, click_y)
    if double:
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(click_x, click_y -  90)
        time.sleep(1.5)
    else:
        pyautogui.click()
    
    print(f"[+] {'Double clicked' if double else 'Clicked'} at ({click_x}, {click_y})")

def find_and_click(template_path, window_title="BlueStacks App Player", double=False):
    screen = capture_bluestacks_window(window_title)
    if screen is None:
        return False

    pos = find_button(screen, template_path)
    if pos:
        click_at(pos, window_title, double=double)
        return True
    else:
        print(f"[!] Button not found: {template_path}")
        return False

def menu():
    while True:
        print("gotcbot v0.1\n")
        print("Which type of farming will you be doing today?")
        print("[1] Normal creatures")
        print("[2] Event creatures")
        choice = input("> ").strip()

        if not choice:
            print("[!] Input can't be empty.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            continue

        if not choice.isdigit():
            print("[!] Please enter a valid number.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            continue

        int_choice = int(choice)

        if int_choice == 1:
            # Normal farming mode — not implemented yet
            return int_choice
        elif int_choice == 2:
            # Event farming mode
            return int_choice
        else:
            print("[!] Not a valid option.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")

            


def main():
    choice = menu()
    print("[*] Starting bot in 3 seconds...")
    time.sleep(3)
    os.system("cls" if os.name == "nt" else "clear")

    assets = "assets/"
    clicked_event_tab_once = False

    if choice == 1:
        sequence1 = [
            ("search.png", False),
            ("freedom.png", False),
            ("search2.png", False),
            ("creature_found.png", True)
        ]
    elif choice == 2:
        sequence1 = [
            ("search.png", False),
            ("event.png", False),    
            ("freedom.png", False),
            ("search2.png", False),
            ("creature_found.png", True)
        ]

    sequence2 = [
        ("attack.png", False),
        ("march.png", False)
    ]

    max_tries_per_button = 2
    move_up_amount = 90  

    while True:
 
        for filename, double_click in sequence1:
            if filename == "event.png" and clicked_event_tab_once:
                print("[*] Skipping event.png — already clicked once.")
                continue

            full_path = os.path.join(assets, filename)
            tries = 0
            while tries < max_tries_per_button:
                print(f"[*] Looking for: {filename} (try {tries + 1}/{max_tries_per_button})")
                success = find_and_click(full_path, double=double_click)
                if success:
                    if filename == "event.png":
                        clicked_event_tab_once = True

                    time.sleep(1)
                    if filename == "creature_found.png" and double_click:
                        current_x, current_y = pyautogui.position()
                        pyautogui.moveTo(current_x, current_y - move_up_amount)
                        print(f"[+] Moved cursor up by {move_up_amount} pixels after double-clicking {filename}")
                    break
                else:
                    print(f"[!] Failed to find/click {filename}")
                    tries += 1
                    time.sleep(2)
            else:
                print(f"[!] Could not find {filename} after {max_tries_per_button} tries, moving on...\n")

      
        for filename, double_click in sequence2:
            full_path = os.path.join(assets, filename)
            tries = 0
            while tries < max_tries_per_button:
                print(f"[*] Looking for: {filename} (try {tries + 1}/{max_tries_per_button})")
                success = find_and_click(full_path, double=double_click)
                if success:
                    time.sleep(1)
                    if filename == "march.png":
                        current_x, current_y = pyautogui.position()
                        pyautogui.moveTo(current_x, current_y - move_up_amount)
                        print(f"[+] Moved cursor up by {move_up_amount} pixels after clicking {filename}")
                    break
                else:
                    print(f"[!] Failed to find/click {filename}")
                    tries += 1
                    time.sleep(2)
            else:
                print(f"[!] Could not find {filename} after {max_tries_per_button} tries, moving on...\n")

        print("[*] Cycle complete, waiting 1 second before repeating...\n")
        time.sleep(1)





if __name__ == "__main__":
    main()
