import os
import re
import flet as ft
from ciphers import playfair, monoalphabetic, caesar, vigenere, substitution, transposition, rail_fence, affine

class CipherValidator:    
    @staticmethod
    def validate_text_input(text):
        if not text or not text.strip():
            raise ValueError("Please enter the text to process.")
        return text.strip()
    
    @staticmethod
    def validate_caesar_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        try:
            shift = int(key.strip())
            if shift < -25 or shift > 25:
                raise ValueError("Caesar cipher key must be a number between -25 and 25.")
            return shift
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Caesar cipher key must be a number between -25 and 25.")
            raise
    
    @staticmethod
    def validate_vigenere_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        key = key.strip()
        if not re.match(r'^[A-Za-z]+$', key):
            raise ValueError("Vigenère cipher key must contain only letters.")
        return key
    
    @staticmethod
    def validate_playfair_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        key = key.strip()
        if not re.match(r'^[A-Za-z]+$', key):
            raise ValueError("Playfair cipher key must contain only letters.")
        return key
    
    @staticmethod
    def validate_monoalphabetic_key(key):
        if not key or not key.strip():
            return "QWERTYUIOPLKJHGFDSAZXCVBNM"
        
        key = key.strip().upper()
        
        if not re.match(r'^[A-Za-z]+$', key):
            raise ValueError("The substitution key must be exactly 26 unique letters.")
        
        if len(key) != 26:
            raise ValueError("The substitution key must be exactly 26 unique letters.")
        
        if len(set(key)) != 26:
            raise ValueError("The substitution key must be exactly 26 unique letters.")
        
        return key
    
    @staticmethod
    def validate_rail_fence_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        try:
            rails = int(key.strip())
            if rails < 2:
                raise ValueError("Rail fence cipher key must be a number greater than 1.")
            return rails
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Rail fence cipher key must be a number greater than 1.")
            raise
    
    @staticmethod
    def validate_transposition_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        try:
            columns = int(key.strip())
            if columns < 2:
                raise ValueError("Transposition cipher key must be a number greater than 1.")
            return columns
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Transposition cipher key must be a number greater than 1.")
            raise
    
    @staticmethod
    def validate_affine_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        key = key.strip()
        
        if not re.match(r'^\d+,\d+$', key):
            raise ValueError("Affine cipher key must be in format 'a,b' (e.g., '5,8').")
        
        try:
            a, b = map(int, key.split(','))
            
            valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
            if a not in valid_a_values:
                raise ValueError("The 'a' value must be coprime with 26.")
            
            return key
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Affine cipher key must be in format 'a,b' (e.g., '5,8').")
            raise
    
    @staticmethod
    def validate_substitution_key(key):
        if not key or not key.strip():
            raise ValueError("Please enter a key.")
        
        key = key.strip()
        
        if len(key) != 26:
            raise ValueError("Substitution cipher key must be 26 unique letters.")
        
        if not re.match(r'^[A-Za-z]+$', key):
            raise ValueError("Substitution cipher key must be 26 unique letters.")
        
        if len(set(key.lower())) != 26:
            raise ValueError("Substitution cipher key must be 26 unique letters.")
        
        return key.upper()


def main(page: ft.Page):
    page.title = "Text Cipher App"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = True
    page.padding = ft.padding.all(16)
    page.window_width = 900
    page.window_height = 700
    page.window_min_width = 480
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
    }
    
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
        visual_density=ft.VisualDensity.COMFORTABLE,
        use_material3=True,
    )

    is_dark = True

    theme_icon = ft.Icon(name=ft.Icons.DARK_MODE)
    theme_label = ft.Text("Dark Mode", weight="w500")
    
    def toggle_theme(e):
        nonlocal is_dark
        is_dark = not is_dark
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        theme_label.value = "Dark Mode" if is_dark else "Light Mode"
        theme_icon.name = ft.Icons.DARK_MODE if is_dark else ft.Icons.LIGHT_MODE
        page.update()

    theme_toggle = ft.Switch(value=True, on_change=toggle_theme)

    def get_theme_toggle():
        if page.width < 600:
            return ft.Row([theme_toggle], alignment=ft.MainAxisAlignment.END)
        else:
            return ft.Row([theme_icon, theme_label, theme_toggle], alignment=ft.MainAxisAlignment.END)

    theme_toggle_container = ft.Container(
        content=get_theme_toggle()
    )

    def show_error_snackbar(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor="#F44336"
        )
        page.snack_bar.open = True
        page.update()

    def show_success_snackbar(message):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor="#4CAF50"
        )
        page.snack_bar.open = True
        page.update()

    def build_cipher_tab(cipher_name, encrypt_fn, decrypt_fn, default_key="KEY", is_key_numeric=False):
        is_encrypt_mode = True
        
        input_text = ft.TextField(
            label="Input Text",
            multiline=True,
            min_lines=3,
            expand=True,
            text_size=16,
            border_radius=10,
            filled=True,
        )
        
        key_field = ft.TextField(
            label="Key",
            value=default_key,
            border_radius=10,
            filled=True,
            expand=True,
            text_size=16,
        )
        
        output_text = ft.TextField(
            label="Output",
            multiline=True,
            min_lines=3,
            expand=True,
            read_only=True,
            border_radius=10,
            filled=True,
            text_size=16,
        )

        if cipher_name == "Caesar":
            key_field.hint_text = "Enter numeric key (-25 to 25)"
            key_field.keyboard_type = ft.KeyboardType.NUMBER
        elif cipher_name == "Vigenère":
            key_field.hint_text = "Enter alphabetic key"
        elif cipher_name == "Playfair":
            key_field.hint_text = "Enter alphabetic key"
        elif cipher_name == "Monoalphabetic":
            key_field.hint_text = "Enter 26 unique letters (optional)"
            key_field.value = ""
        elif cipher_name == "Substitution":
            key_field.hint_text = "Enter 26 unique letters"
            key_field.value = "QWERTYUIOPLKJHGFDSAZXCVBNM"
        elif cipher_name == "Rail Fence":
            key_field.hint_text = "Enter number of rails (>1)"
            key_field.keyboard_type = ft.KeyboardType.NUMBER
            key_field.value = "3"
        elif cipher_name == "Transposition":
            key_field.hint_text = "Enter number of columns (>1)"
            key_field.keyboard_type = ft.KeyboardType.NUMBER
            key_field.value = "4"
        elif cipher_name == "Affine":
            key_field.hint_text = "Enter a,b format (e.g., 5,8)"
            key_field.value = "5,8"

        def get_validated_inputs():
            try:
                text = CipherValidator.validate_text_input(input_text.value)
                
                if cipher_name == "Caesar":
                    key = CipherValidator.validate_caesar_key(key_field.value)
                elif cipher_name == "Vigenère":
                    key = CipherValidator.validate_vigenere_key(key_field.value)
                elif cipher_name == "Playfair":
                    key = CipherValidator.validate_playfair_key(key_field.value)
                elif cipher_name == "Monoalphabetic":
                    key = CipherValidator.validate_monoalphabetic_key(key_field.value)
                elif cipher_name == "Substitution":
                    key = CipherValidator.validate_substitution_key(key_field.value)
                elif cipher_name == "Rail Fence":
                    key = CipherValidator.validate_rail_fence_key(key_field.value)
                elif cipher_name == "Transposition":
                    key = CipherValidator.validate_transposition_key(key_field.value)
                elif cipher_name == "Affine":
                    key = CipherValidator.validate_affine_key(key_field.value)
                else:
                    if not key_field.value or not key_field.value.strip():
                        raise ValueError("Please enter a key.")
                    key = key_field.value.strip()
                
                return text, key
            except ValueError as e:
                raise e

        mode_label = ft.Text("Encrypt", weight="w500", color="#4CAF50")
        
        def toggle_mode(e):
            nonlocal is_encrypt_mode
            is_encrypt_mode = not is_encrypt_mode
            
            if is_encrypt_mode:
                mode_label.value = "Encrypt"
                mode_label.color = "#4CAF50"
                encrypt_toggle.active_color = "#4CAF50"
            else:
                mode_label.value = "Decrypt"
                mode_label.color = "#2196F3"
                encrypt_toggle.active_color = "#2196F3"
                
            update_output()
            page.update()
        
        encrypt_toggle = ft.Switch(
            value=True,
            active_color="#4CAF50",
            on_change=toggle_mode
        )
        
        mode_row = ft.Row([
            mode_label,
            encrypt_toggle,
        ], alignment=ft.MainAxisAlignment.END)

        def update_output(_=None):
            try:
                key_field.error_text = None
                key_field.border_color = None

                if not input_text.value or not input_text.value.strip():
                    output_text.value = ""
                    page.update()
                    return
                
                text, key = get_validated_inputs()
                
                if is_encrypt_mode:
                    result = encrypt_fn(text, key)
                else:
                    result = decrypt_fn(text, key)
                    
                output_text.value = result
                
                input_text.error_text = None
                
            except ValueError as e:
                error_msg = str(e)
                output_text.value = f"Error: {error_msg}"
                
                if "text to process" in error_msg.lower():
                    input_text.error_text = "Text is required"
                elif "key" in error_msg.lower():
                    key_field.error_text = error_msg.replace("Error: ", "")
                    key_field.border_color = ft.colors.RED
                
                show_error_snackbar(error_msg)
            
            except Exception as e:
                error_msg = f"Cipher error: {str(e)}"
                output_text.value = f"Error: {error_msg}"
                show_error_snackbar(error_msg)
            
            page.update()

        def upload_file(e: ft.FilePickerResultEvent):
            if e.files:
                try:
                    with open(e.files[0].path, "r", encoding="utf-8") as f:
                        content = f.read()
                        input_text.value = content
                    update_output()
                    show_success_snackbar("File uploaded successfully!")
                except Exception as e:
                    show_error_snackbar(f"Error reading file: {str(e)}")

        def download_file(e):
            if output_text.value and not output_text.value.startswith("Error:"):
                save_dialog.save_file(
                    dialog_title="Save output text",
                    file_type="txt",
                    allowed_extensions=["txt"]
                )
            else:
                show_error_snackbar("No valid output to save!")

        def save_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    with open(e.path, "w", encoding="utf-8") as f:
                        f.write(output_text.value)
                    show_success_snackbar("File saved successfully!")
                except Exception as e:
                    show_error_snackbar(f"Error saving file: {str(e)}")

        def swap_text(e):
            if input_text.value or output_text.value:
                if not output_text.value.startswith("Error:"):
                    input_text.value, output_text.value = output_text.value, input_text.value
                    update_output()
                    page.update()
                else:
                    show_error_snackbar("Cannot swap: Output contains an error!")

        def on_input_change(e):
            input_text.error_text = None
            update_output()

        def on_key_change(e):
            key_field.error_text = None
            key_field.border_color = None
            update_output()

        input_text.on_change = on_input_change
        key_field.on_change = on_key_change

        file_picker = ft.FilePicker(on_result=upload_file)
        save_dialog = ft.FilePicker(on_result=save_file_result)
        page.overlay.extend([file_picker, save_dialog])

        cipher_info = {
            "Playfair": "A symmetric encryption technique that uses a 5×5 grid of letters for encryption. Key must contain only letters.",
            "Monoalphabetic": "A substitution cipher that uses a fixed replacement for each letter. Key should be 26 unique letters (optional - uses default if empty).",
            "Caesar": "A simple substitution cipher where each letter is shifted by a fixed number of positions. Key must be a number between -25 and 25.",
            "Vigenère": "A method of encrypting text using a series of interwoven Caesar ciphers. Key must contain only letters.",
            "Substitution": "A monoalphabetic substitution cipher that replaces each letter with another letter from a 26-letter key. Key must be 26 unique letters.",
            "Rail Fence": "A transposition cipher that writes text in a zigzag pattern across multiple rails, then reads it off row by row. Key is the number of rails (must be >1).",
            "Transposition": "A columnar transposition cipher that arranges text in columns and reads it column by column. Key is the number of columns (must be >1).",
            "Affine": "A mathematical cipher using the formula E(x)=(ax+b) mod 26. Key format is 'a,b' where 'a' must be coprime with 26 (valid: 1,3,5,7,9,11,15,17,19,21,23,25)."
        }

        def get_action_buttons():
            swap_btn = ft.IconButton(
                icon=ft.Icons.SWAP_HORIZ,
                tooltip="Swap input/output",
                on_click=swap_text,
                icon_color="#FF9800"
            )
            
            upload_btn = ft.ElevatedButton(
                "Upload File",
                icon=ft.Icons.UPLOAD_FILE,
                on_click=lambda _: file_picker.pick_files(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            )
            
            save_btn = ft.ElevatedButton(
                "Save Output",
                icon=ft.Icons.DOWNLOAD,
                on_click=download_file,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            )
            
            if page.width < 600:
                return ft.Column([
                    ft.Row([swap_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        upload_btn,
                        save_btn,
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ], spacing=10, expand=True)
            else:
                return ft.Row([
                    swap_btn,
                    upload_btn,
                    save_btn,
                ], spacing=10, alignment=ft.MainAxisAlignment.END)

        action_buttons = ft.Container(content=get_action_buttons())

        def get_config_row():
            if page.width < 600:
                return ft.Column([
                    key_field,
                    mode_row,
                ], spacing=10)
            else:
                return ft.Row([
                    ft.Container(content=key_field, expand=True),
                    mode_row,
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        config_row = ft.Container(content=get_config_row())

        cipher_content = ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Text(
                        cipher_info[cipher_name], 
                        size=14,
                        color="#FFFFFF" if is_dark else "#000000"
                    ),
                    padding=10,
                ),
                elevation=0,
                color="#303030" if is_dark else "#E0E0E0",
                margin=ft.margin.only(bottom=15)
            ),
            ft.Text("Configure", size=18, weight="w500"),
            config_row,
            ft.Divider(height=2, thickness=1),
            ft.Text("Content", size=18, weight="w500"),
            input_text,
            action_buttons,
            ft.Divider(height=2, thickness=1),
            ft.Text("Result", size=18, weight="w500"),
            output_text
        ], spacing=15, expand=True)

        def update_layout(_=None):
            action_buttons.content = get_action_buttons()
            config_row.content = get_config_row()
            page.update()

        page.on_resize = lambda e: update_layout()

        return ft.Container(
            content=cipher_content,
            padding=15,
            border_radius=12,
            expand=True,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

    tab_contents = {
        "Playfair": build_cipher_tab("Playfair", playfair.encrypt, playfair.decrypt),
        "Monoalphabetic": build_cipher_tab("Monoalphabetic", monoalphabetic.encrypt, monoalphabetic.decrypt),
        "Caesar": build_cipher_tab("Caesar", caesar.encrypt, caesar.decrypt, default_key="3", is_key_numeric=True),
        "Vigenère": build_cipher_tab("Vigenère", vigenere.encrypt, vigenere.decrypt),
        "Substitution": build_cipher_tab("Substitution", substitution.encrypt, substitution.decrypt, default_key="QWERTYUIOPLKJHGFDSAZXCVBNM"),
        "Rail Fence": build_cipher_tab("Rail Fence", rail_fence.encrypt, rail_fence.decrypt, default_key="3", is_key_numeric=True),
        "Transposition": build_cipher_tab("Transposition", transposition.encrypt, transposition.decrypt, default_key="4", is_key_numeric=True),
        "Affine": build_cipher_tab("Affine", affine.encrypt, affine.decrypt, default_key="5,8"),
    }

    switcher = ft.AnimatedSwitcher(
        content=tab_contents["Playfair"],
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=300,
        expand=True
    )

    def tab_changed(e):
        selected_tab = e.control.tabs[e.control.selected_index].text
        switcher.content = tab_contents[selected_tab]
        page.update()

    def get_tabs():
        if page.width < 600:
            return ft.NavigationBar(
                destinations=[
                    ft.NavigationDestination(icon=ft.Icons.GRID_VIEW, label="Playfair"),
                    ft.NavigationDestination(icon=ft.Icons.ABC, label="Monoalpha"),
                    ft.NavigationDestination(icon=ft.Icons.LOCK_CLOCK, label="Caesar"),
                    ft.NavigationDestination(icon=ft.Icons.KEY, label="Vigenère"),
                    ft.NavigationDestination(icon=ft.Icons.SWAP_CALLS, label="More..."),
                ],
                on_change=lambda e: handle_mobile_nav(e.control.selected_index),
                selected_index=0,
            )
        else:
            return ft.Tabs(
                selected_index=0,
                on_change=tab_changed,
                animation_duration=300,
                scrollable=True,
                tabs=[
                    ft.Tab(text="Playfair", icon=ft.Icons.GRID_VIEW),
                    ft.Tab(text="Monoalphabetic", icon=ft.Icons.ABC),
                    ft.Tab(text="Caesar", icon=ft.Icons.LOCK_CLOCK),
                    ft.Tab(text="Vigenère", icon=ft.Icons.KEY),
                    ft.Tab(text="Substitution", icon=ft.Icons.FIND_REPLACE),
                    ft.Tab(text="Rail Fence", icon=ft.Icons.RAILWAY_ALERT),
                    ft.Tab(text="Transposition", icon=ft.Icons.TABLE_ROWS),
                    ft.Tab(text="Affine", icon=ft.Icons.FUNCTIONS),
                ],
                expand=False,
            )

    mobile_cipher_index = 0
    
    def handle_mobile_nav(index):
        nonlocal mobile_cipher_index
        if index == 4:
            show_cipher_selector()
        else:
            mobile_cipher_index = index
            set_tab_content(index)

    def show_cipher_selector():
        cipher_names = ["Playfair", "Monoalphabetic", "Caesar", "Vigenère", 
                       "Substitution", "Rail Fence", "Transposition", "Affine"]
        
        def select_cipher(e):
            cipher_index = int(e.control.data)
            set_tab_content(cipher_index)
            page.dialog.open = False
            page.update()
        
        dialog_content = ft.Column([
            ft.Text("Select Cipher", size=20, weight="bold"),
            ft.Divider(),
        ] + [
            ft.TextButton(
                text=cipher_name,
                data=str(i),
                on_click=select_cipher,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ) for i, cipher_name in enumerate(cipher_names)
        ], spacing=5)
        
        page.dialog = ft.AlertDialog(
            title=ft.Text("Choose Cipher Algorithm"),
            content=dialog_content,
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(page.dialog, 'open', False) or page.update())
            ]
        )
        page.dialog.open = True
        page.update()

    def set_tab_content(index):
        tab_names = ["Playfair", "Monoalphabetic", "Caesar", "Vigenère", 
                    "Substitution", "Rail Fence", "Transposition", "Affine"]
        if index < len(tab_names):
            switcher.content = tab_contents[tab_names[index]]
            page.update()

    tabs_container = ft.Container(content=get_tabs())

    def get_header():
        if page.width < 600:
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.SECURITY, size=24),
                        ft.Text("Text Cipher App", size=20, weight="bold", expand=True),
                    ]),
                    theme_toggle_container
                ]),
                margin=ft.margin.only(bottom=10),
            )
        else:
            return ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SECURITY, size=32),
                    ft.Text("Text Cipher App", size=28, weight="bold", expand=True),
                    theme_toggle_container
                ]),
                margin=ft.margin.only(bottom=10),
            )

    header_container = ft.Container(content=get_header())

    def update_header(e=None):
        header_container.content = get_header()
        page.update()

    def update_tabs(e=None):
        tabs_container.content = get_tabs()
        theme_toggle_container.content = get_theme_toggle()
        page.update()

    page.on_resize = lambda e: (update_header(e), update_tabs(e))

    page.add(
        header_container,
        tabs_container,
        switcher
    )


if __name__ == "__main__":
    ft.app(target=main)
