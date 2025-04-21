import os
import flet as ft
from ciphers import playfair, monoalphabetic, caesar, vigenere


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
    
    # Set custom theme with rounded corners and modern look
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
        visual_density=ft.VisualDensity.COMFORTABLE,
        use_material3=True,
    )

    is_dark = True

    # Light/Dark Theme Toggle
    theme_icon = ft.Icon(name=ft.icons.DARK_MODE)
    theme_label = ft.Text("Dark Mode", weight="w500")
    
    def toggle_theme(e):
        nonlocal is_dark
        is_dark = not is_dark
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        theme_label.value = "Dark Mode" if is_dark else "Light Mode"
        theme_icon.name = ft.icons.DARK_MODE if is_dark else ft.icons.LIGHT_MODE
        page.update()

    theme_toggle = ft.Switch(value=True, on_change=toggle_theme)

    # Responsive theme toggle
    def get_theme_toggle():
        if page.width < 600:
            return ft.Row([theme_toggle], alignment=ft.MainAxisAlignment.END)
        else:
            return ft.Row([theme_icon, theme_label, theme_toggle], alignment=ft.MainAxisAlignment.END)

    theme_toggle_container = ft.Container(
        content=get_theme_toggle()
    )

    # Update UI based on window size
    def page_resize(e):
        theme_toggle_container.content = get_theme_toggle()
        page.update()

    page.on_resize = page_resize

    def build_cipher_tab(cipher_name, encrypt_fn, decrypt_fn, default_key="KEY", is_key_numeric=False):
        # Add state for encrypt/decrypt mode
        is_encrypt_mode = True
        
        # Modern style for text fields
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
            expand=True,  # Allow key field to expand in small screens
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
            key_field.hint_text = "Enter numeric key"
            key_field.keyboard_type = ft.KeyboardType.NUMBER

        def get_key():
            key_val = key_field.value or default_key
            return int(key_val) if is_key_numeric and key_val.isdigit() else key_val

        # Encrypt/Decrypt toggle
        mode_label = ft.Text("Encrypt", weight="w500", color="#4CAF50")
        
        def toggle_mode(e):
            nonlocal is_encrypt_mode
            is_encrypt_mode = not is_encrypt_mode
            
            # Update UI
            if is_encrypt_mode:
                mode_label.value = "Encrypt"
                mode_label.color = "#4CAF50"  # Green for encrypt
                encrypt_toggle.active_color = "#4CAF50"
            else:
                mode_label.value = "Decrypt"
                mode_label.color = "#2196F3"  # Blue for decrypt
                encrypt_toggle.active_color = "#2196F3"
                
            # Re-process text with new mode
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
                if not input_text.value:
                    output_text.value = ""
                    page.update()
                    return
                    
                key_val = get_key()
                
                # Use the appropriate function based on mode
                if is_encrypt_mode:
                    result = encrypt_fn(input_text.value, key_val)
                else:
                    result = decrypt_fn(input_text.value, key_val)
                    
                output_text.value = result
            except Exception as e:
                output_text.value = f"Error: {str(e)}"
            page.update()

        def upload_file(e: ft.FilePickerResultEvent):
            if e.files:
                try:
                    with open(e.files[0].path, "r", encoding="utf-8") as f:
                        input_text.value = f.read()
                    update_output()
                except Exception as e:
                    page.show_snack_bar(ft.SnackBar(
                        content=ft.Text(f"Error reading file: {str(e)}"),
                        action="OK"
                    ))

        def download_file(e):
            if output_text.value:
                save_dialog.save_file(
                    dialog_title="Save output text",
                    file_type="txt",
                    allowed_extensions=["txt"]
                )

        def save_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    with open(e.path, "w", encoding="utf-8") as f:
                        f.write(output_text.value)
                    page.show_snack_bar(ft.SnackBar(
                        content=ft.Text("File saved successfully!"),
                        action="OK",
                        bgcolor="#4CAF50"
                    ))
                except Exception as e:
                    page.show_snack_bar(ft.SnackBar(
                        content=ft.Text(f"Error saving file: {str(e)}"),
                        action="OK"
                    ))

        # Swap input and output
        def swap_text(e):
            if input_text.value or output_text.value:
                input_text.value, output_text.value = output_text.value, input_text.value
                update_output()
                page.update()

        # Triggers real-time encryption/decryption
        input_text.on_change = update_output
        key_field.on_change = update_output

        file_picker = ft.FilePicker(on_result=upload_file)
        save_dialog = ft.FilePicker(on_result=save_file_result)
        page.overlay.extend([file_picker, save_dialog])

        cipher_info = {
            "Playfair": "A symmetric encryption technique that uses a 5×5 grid of letters for encryption.",
            "Monoalphabetic": "A substitution cipher that uses a fixed replacement for each letter in the plaintext.",
            "Caesar": "A simple substitution cipher where each letter is shifted by a fixed number of positions.",
            "Vigenère": "A method of encrypting text using a series of interwoven Caesar ciphers."
        }

        # Responsive buttons row
        def get_action_buttons():
            swap_btn = ft.IconButton(
                icon=ft.icons.SWAP_HORIZ,
                tooltip="Swap input/output",
                on_click=swap_text,
                icon_color="#FF9800"  # Orange
            )
            
            upload_btn = ft.ElevatedButton(
                "Upload File",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: file_picker.pick_files(),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            )
            
            save_btn = ft.ElevatedButton(
                "Save Output",
                icon=ft.icons.DOWNLOAD,
                on_click=download_file,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            )
            
            # On smaller screens, stack buttons vertically
            if page.width < 600:
                return ft.Column([
                    ft.Row([swap_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        upload_btn,
                        save_btn,
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ], spacing=10, expand=True)
            else:
                # On larger screens, use horizontal layout
                return ft.Row([
                    swap_btn,
                    upload_btn,
                    save_btn,
                ], spacing=10, alignment=ft.MainAxisAlignment.END)

        # Create buttons container with initial layout
        action_buttons = ft.Container(content=get_action_buttons())

        # Config row with key and mode toggle
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

        # Create the content structure
        cipher_content = ft.Column([
            # Cipher description card
            ft.Card(
                content=ft.Container(
                    content=ft.Text(cipher_info[cipher_name], size=14),
                    padding=10,
                ),
                elevation=0,
                color="#303030" if is_dark else "#E0E0E0",
                margin=ft.margin.only(bottom=15)
            ),
            # Input section
            ft.Text("Configure", size=18, weight="w500"),
            config_row,
            ft.Divider(height=2, thickness=1),
            # Content section
            ft.Text("Content", size=18, weight="w500"),
            input_text,
            action_buttons,
            ft.Divider(height=2, thickness=1),
            ft.Text("Result", size=18, weight="w500"),
            output_text
        ], spacing=15, expand=True)

        # Update layout on resize
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

    # Tabs for each cipher
    tab_contents = {
        "Playfair": build_cipher_tab("Playfair", playfair.encrypt, playfair.decrypt),
        "Monoalphabetic": build_cipher_tab("Monoalphabetic", monoalphabetic.encrypt, monoalphabetic.decrypt),
        "Caesar": build_cipher_tab("Caesar", caesar.encrypt, caesar.decrypt, default_key="3", is_key_numeric=True),
        "Vigenère": build_cipher_tab("Vigenère", vigenere.encrypt, vigenere.decrypt),
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

    # Responsive tabs
    def get_tabs():
        if page.width < 600:
            # For mobile: Bottom navigation
            return ft.NavigationBar(
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.GRID_VIEW, label="Playfair"),
                    ft.NavigationDestination(icon=ft.icons.ABC, label="Monoalpha"),
                    ft.NavigationDestination(icon=ft.icons.LOCK_CLOCK, label="Caesar"),
                    ft.NavigationDestination(icon=ft.icons.KEY, label="Vigenère"),
                ],
                on_change=lambda e: set_tab_content(e.control.selected_index),
                selected_index=0,
            )
        else:
            # For desktop: Top tabs
            return ft.Tabs(
                selected_index=0,
                on_change=tab_changed,
                animation_duration=300,
                tabs=[
                    ft.Tab(text="Playfair", icon=ft.icons.GRID_VIEW),
                    ft.Tab(text="Monoalphabetic", icon=ft.icons.ABC),
                    ft.Tab(text="Caesar", icon=ft.icons.LOCK_CLOCK),
                    ft.Tab(text="Vigenère", icon=ft.icons.KEY),
                ],
                expand=False,
            )

    def set_tab_content(index):
        tab_names = ["Playfair", "Monoalphabetic", "Caesar", "Vigenère"]
        switcher.content = tab_contents[tab_names[index]]
        page.update()

    # Create tabs container
    tabs_container = ft.Container(content=get_tabs())

    # Update tabs on window resize
    def update_tabs(e=None):
        tabs_container.content = get_tabs()
        theme_toggle_container.content = get_theme_toggle()
        page.update()

    page.on_resize = update_tabs

    # App header for different screen sizes
    def get_header():
        if page.width < 600:
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.SECURITY, size=24),
                        ft.Text("Text Cipher App", size=20, weight="bold", expand=True),
                    ]),
                    theme_toggle_container
                ]),
                margin=ft.margin.only(bottom=10),
            )
        else:
            return ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.SECURITY, size=32),
                    ft.Text("Text Cipher App", size=28, weight="bold", expand=True),
                    theme_toggle_container
                ]),
                margin=ft.margin.only(bottom=10),
            )

    header_container = ft.Container(content=get_header())

    # Update header on window resize
    def update_header(e=None):
        header_container.content = get_header()
        page.update()

    # Combine resize handlers
    def on_page_resize(e):
        update_header()
        update_tabs()
        # This will call the update_layout for the active tab

    page.on_resize = on_page_resize

    # Main layout with responsive design
    content_layout = ft.Column(
        [
            header_container,
            tabs_container,
            switcher,
            ft.Container(
                content=ft.Row(
                    [ft.Text("Made By Haris Khan ❤️", size=12, italic=True)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                margin=ft.margin.only(top=10),
            ),
        ],
        spacing=5,
        expand=True,
    )

    # Add main layout to page
    page.add(content_layout)
    
    # Force initial layout update
    page.update()


ft.app(target=main)