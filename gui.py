import tkinter as tk
from tkinter import filedialog
import asyncio
import subprocess
import threading
from helpers.common import *
# from main import main as bot_main

# def test_start():
#     print('test_start')
    # bot_main()

class GamePathApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Path App")

        # Load the last saved path
        self.last_saved_path = self.load_last_saved_path()

        # Create a label
        self.label = tk.Label(master, text="Enter game path:")
        self.label.pack(pady=10)

        # Create an entry widget to get the game path
        self.entry = tk.Entry(master, width=50)
        self.entry.pack(pady=5)

        # Bind the Control-v key combination to the entry widget
        self.entry.bind('<Control-v>', self.paste_clipboard)

        # Create a button to browse for the game path
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_game_path)
        self.browse_button.pack(pady=5)

        # Create a button to submit the game path
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_game_path)
        self.submit_button.pack(pady=5)

        # Create a big "Start" button
        start_button = tk.Button(self.master, text="Start", font=("Arial", 20), command=self.start_process)
        start_button.pack(pady=20)

        # Task handles for asynchronous processes
        self.task1 = None
        self.task2 = None

    def browse_game_path(self):
        # Open a file dialog to select the game path
        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        # Update the entry widget with the selected game path
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, file_path)

    def validate_game_path(self, game_path):
        # Perform abstract validation here
        # For example, check if the file exists or meets certain criteria
        return True  # For demonstration purposes, always return True

    def submit_game_path(self):
        # Get the game path from the entry widget
        game_path = self.entry.get()

        # Perform validation
        if self.validate_game_path(game_path):
            print("Game path is valid")

            # Save the current path as the last saved path
            self.save_last_saved_path(game_path)

            # Run the executable file
            try:
                print(game_path)
                subprocess.run(f"{game_path} -gameid=101 -tray-start")

                # Show loading screen
                loading_screen = tk.Toplevel(self.master)
                loading_screen.title("Loading...")
                loading_label = tk.Label(loading_screen, text="Loading...")
                loading_label.pack(padx=20, pady=20)

                # Call the abstract function after 5 seconds
                # self.master.after(5000, lambda: self.execute_abstract_function(loading_screen))

                while not is_index_page(logger=False):
                    print('Waiting the game window')
                    sleep(5)

                loading_screen.destroy()
                print('Game window is ready')

                # Create a big "Start" button
                start_button = tk.Button(self.master, text="Start", font=("Arial", 20), command=self.start_process)
                start_button.pack(pady=20)


            except Exception as e:
                print("Error:", e)

            # Start asynchronous parallel processes
            # self.task1 = asyncio.create_task(self.process1())
            # self.task2 = asyncio.create_task(self.process2())
        else:
            print("Invalid game path:", game_path)

    def start_process(self):
        # Start asynchronous parallel processes in a separate thread
        threading.Thread(target=self.run_async_tasks).start()

    def run_async_tasks(self):
        # self.task1 = asyncio.create_task(bot_main())

        # Create a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Start asynchronous parallel processes
        self.task1 = asyncio.create_task(self.process1())
        self.task2 = asyncio.create_task(self.process2())

    async def process1(self):
        # First asynchronous process
        print("Starting process 1...")
        await asyncio.sleep(3)  # Simulating some asynchronous task
        print("Process 1 completed.")

    async def process2(self):
        # Second asynchronous process
        print("Starting process 2...")
        await asyncio.sleep(5)  # Simulating some asynchronous task
        print("Process 2 completed.")

    # def cancel_process1(self):
    #     # Cancel process 1 if it is running
    #     if self.task1 and not self.task1.done():
    #         self.task1.cancel()
    #         print("Process 1 canceled.")

    def paste_clipboard(self, event):
        # Clear the entry widget before pasting the clipboard content
        self.entry.delete(0, tk.END)
        # Get the clipboard content
        clipboard_content = self.master.clipboard_get()
        # Insert the clipboard content into the entry widget
        self.entry.insert(0, clipboard_content)

    def load_last_saved_path(self):
        # Load the last saved path from a file
        if os.path.exists("last_saved_path.txt"):
            with open("last_saved_path.txt", "r") as file:
                return file.read().strip()

    def save_last_saved_path(self, game_path):
        # Save the last saved path to a file
        with open("last_saved_path.txt", "w") as file:
            file.write(game_path)


def main():
    root = tk.Tk()
    app = GamePathApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
