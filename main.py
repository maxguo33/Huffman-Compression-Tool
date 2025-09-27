import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import heapq
from collections import Counter
import pickle
import bitarray

# Color scheme
BACKGROUND_COLOR = "#f0f4f8"
PRIMARY_COLOR = "#1e88e5"    # Button color
SECONDARY_COLOR = "#5e35b1"  # Header color
TEXT_COLOR = "#212121"
ACCENT_COLOR = "#e91e63"
SUCCESS_COLOR = "#4caf50"

class HuffmanCompressor:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
        self.original_file_path = ""
        self.compressed_file_path = ""
        
    def build_huffman_tree(self, text):
        """Build Huffman tree based on character frequencies."""
        frequency = Counter(text)
        
        # If there's only one unique character, assign '0' to it directly
        if len(frequency) == 1:
            char = list(frequency.keys())[0]
            self.codes[char] = "0"
            self.reverse_codes["0"] = char
            return
        
        # Create a min-heap of [frequency, [char, code]]
        heap = [[freq, [char, ""]] for char, freq in frequency.items()]
        heapq.heapify(heap)
        
        # Merge the two lowest frequency nodes until only one remains
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        # Build codes from the final heap node
        huffman_codes_list = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
        self.codes = {char: code for char, code in huffman_codes_list}
        self.reverse_codes = {code: char for char, code in self.codes.items()}
        
    def compress_file(self, file_path):
        """Compress a file using Huffman coding."""
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            if not text:
                raise ValueError("File is empty")
            
            # Build Huffman tree and generate codes
            self.build_huffman_tree(text)
            
            # Encode the text using the generated codes
            encoded_text = ''.join(self.codes[char] for char in text)
            bits = bitarray.bitarray(encoded_text)
            
            # Create the compressed file path
            base_path, ext = os.path.splitext(file_path)
            compressed_file_path = f"{base_path}.bin"
            
            # Write the compressed data to the .bin file using highest pickle protocol for compactness
            with open(compressed_file_path, 'wb') as output_file:
                # Save the Huffman dictionary for decompression
                pickle.dump(self.reverse_codes, output_file, protocol=pickle.HIGHEST_PROTOCOL)
                # Save the original file extension
                pickle.dump(ext, output_file, protocol=pickle.HIGHEST_PROTOCOL)
                # Save the actual compressed bits
                bits.tofile(output_file)
            
            self.original_file_path = file_path
            self.compressed_file_path = compressed_file_path
            
            # Compute sizes and compression ratio as percentage:
            # (original file size / compressed file size) * 100
            original_size = os.path.getsize(file_path)
            compressed_size = os.path.getsize(compressed_file_path)
            ratio = (original_size / compressed_size) * 100 if compressed_size > 0 else 0
            
            # Return stats and codes
            return {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': ratio,
                'codes': self.codes,
                'source_text': text
            }
        except Exception as e:
            raise Exception(f"Compression failed: {str(e)}")
    
    def decompress_file(self, file_path):
        """Decompress a file that was compressed with Huffman coding."""
        try:
            with open(file_path, 'rb') as input_file:
                # Load the Huffman dictionary
                reverse_codes = pickle.load(input_file)
                # Load the original file extension
                original_ext = pickle.load(input_file)
                # Read the compressed data as a bitarray
                bits = bitarray.bitarray()
                bits.fromfile(input_file)
            
            # Convert bitarray to a string of bits
            encoded_text = bits.to01()
            
            # Decode the text
            current_bits = ""
            decoded_text = ""
            for bit in encoded_text:
                current_bits += bit
                if current_bits in reverse_codes:
                    decoded_text += reverse_codes[current_bits]
                    current_bits = ""
            
            # Create the decompressed file path
            base_path, _ = os.path.splitext(file_path)
            decompressed_file_path = f"{base_path}_decompressed{original_ext}"
            
            # Write the decompressed text to the file
            with open(decompressed_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(decoded_text)
            
            return {
                'path': decompressed_file_path,
                'text': decoded_text
            }
        except Exception as e:
            raise Exception(f"Decompression failed: {str(e)}")

class HuffmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Huffman Coding Compression Tool")
        self.geometry("900x750")
        self.configure(bg=BACKGROUND_COLOR)
        
        self.compressor = HuffmanCompressor()
        self.selected_file = ""
        self.file_text = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Header
        header_frame = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Huffman Coding Compression Tool", 
            font=("Arial", 24, "bold"), 
            fg="white", 
            bg=SECONDARY_COLOR,
            pady=20
        )
        header_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self, bg=BACKGROUND_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = tk.LabelFrame(
            main_frame, 
            text="File Selection", 
            font=("Arial", 12, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=10,
            pady=10
        )
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        file_path_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path_var,
            font=("Arial", 10),
            width=50,
            state="readonly"
        )
        file_path_entry.grid(row=0, column=0, padx=5, pady=10)
        
        browse_button = tk.Button(
            file_frame,
            text="Browse",
            font=("Arial", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            padx=10,
            command=self.browse_file
        )
        browse_button.grid(row=0, column=1, padx=5, pady=10)
        
        # Text display frame
        text_display_frame = tk.LabelFrame(
            main_frame, 
            text="File Content", 
            font=("Arial", 12, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=10,
            pady=10
        )
        text_display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_display = scrolledtext.ScrolledText(
            text_display_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            width=80,
            height=8
        )
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_display.config(state=tk.DISABLED)
        
        # Action buttons
        action_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR, padx=10, pady=10)
        action_frame.pack(fill=tk.X, pady=10)
        
        compress_button = tk.Button(
            action_frame,
            text="Compress",
            font=("Arial", 12, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            padx=30,
            pady=10,
            command=self.compress_file
        )
        compress_button.pack(side=tk.LEFT, padx=10)
        
        decompress_button = tk.Button(
            action_frame,
            text="Decompress",
            font=("Arial", 12, "bold"),
            bg=ACCENT_COLOR,
            fg="white",
            padx=30,
            pady=10,
            command=self.decompress_file
        )
        decompress_button.pack(side=tk.RIGHT, padx=10)
        
        # Results frame
        self.results_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        
        # Status message
        self.status_message_var = tk.StringVar()
        self.status_message = tk.Label(
            self.results_frame,
            textvariable=self.status_message_var,
            font=("Arial", 12, "bold"),
            bg=SUCCESS_COLOR,
            fg="white",
            padx=10,
            pady=10
        )
        self.status_message.pack(fill=tk.X, pady=10)
        
        # Single-line stats label
        self.combined_stats_var = tk.StringVar()
        self.combined_stats_label = tk.Label(
            self.results_frame,
            textvariable=self.combined_stats_var,
            font=("Arial", 10, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        self.combined_stats_label.pack(pady=5)
        
        # Scrolled text area for codes or decompressed text
        self.result_text_frame = tk.LabelFrame(
            self.results_frame,
            text="",  # Updated dynamically
            font=("Arial", 12, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            padx=10,
            pady=10
        )
        self.result_text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(
            self.result_text_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            width=80,
            height=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9),
            bg="#eeeeee",
            fg=TEXT_COLOR
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var.set("Ready")
        
    def browse_file(self):
        """Open file dialog to select a file."""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Text Files", "*.txt"), ("Compressed Files", "*.bin"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_path_var.set(file_path)
            
            # Hide results if visible
            if self.results_frame.winfo_ismapped():
                self.results_frame.pack_forget()
            
            try:
                # If it's a text file, display content
                if file_path.endswith('.txt'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.file_text = f.read()
                    self.text_display.config(state=tk.NORMAL)
                    self.text_display.delete(1.0, tk.END)
                    self.text_display.insert(tk.END, self.file_text)
                    self.text_display.config(state=tk.DISABLED)
                    self.status_var.set(f"File loaded: {os.path.basename(file_path)}")
                # If it's a .bin file, show a simple message
                elif file_path.endswith('.bin'):
                    self.text_display.config(state=tk.NORMAL)
                    self.text_display.delete(1.0, tk.END)
                    self.text_display.insert(tk.END, "[Binary compressed file - ready for decompression]")
                    self.text_display.config(state=tk.DISABLED)
                    self.status_var.set(f"Compressed file loaded: {os.path.basename(file_path)}")
                else:
                    self.text_display.config(state=tk.NORMAL)
                    self.text_display.delete(1.0, tk.END)
                    self.text_display.insert(tk.END, "Unsupported file format for preview")
                    self.text_display.config(state=tk.DISABLED)
                    self.status_var.set(f"File selected: {os.path.basename(file_path)}")
            except Exception as e:
                self.status_var.set(f"Error reading file: {str(e)}")
    
    def compress_file(self):
        """Compress the selected .txt file."""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        if not self.selected_file.endswith('.txt'):
            messagebox.showwarning("Warning", "Please select a text (.txt) file for compression!")
            return
        
        try:
            result = self.compressor.compress_file(self.selected_file)
            
            # Update status message
            self.status_message_var.set(
                f"Compression Successful! Saved as: {os.path.basename(self.compressor.compressed_file_path)}"
            )
            self.status_message.config(bg=SUCCESS_COLOR)
            
            # Single-line combined stats
            original_size = result['original_size']
            compressed_size = result['compressed_size']
            # Compute ratio as percentage: (original bytes / compressed bytes) * 100
            ratio = (original_size / compressed_size) * 100 if compressed_size > 0 else 0
            
            self.combined_stats_var.set(
                f"Original: {original_size} bytes | Compressed: {compressed_size} bytes | Ratio: {ratio:.2f}%"
            )
            
            # Display Huffman codes in the text area
            self.result_text_frame.config(text="Huffman Codes (Character: Code)")
            self.result_text.delete(1.0, tk.END)
            
            codes_display = ""
            # Sort letters first, then symbols
            for char, code in sorted(result['codes'].items(), key=lambda item: (0 if item[0].isalpha() else 1, item[0])):
                display_char = repr(char)[1:-1] if not char.isprintable() else char
                codes_display += f"{display_char}: {code}\n"
            
            self.result_text.insert(tk.END, codes_display)
            
            # Show results
            if not self.results_frame.winfo_ismapped():
                self.results_frame.pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set("Compression complete!")
        except Exception as e:
            self.status_message_var.set(f"Compression Failed: {str(e)}")
            self.status_message.config(bg=ACCENT_COLOR)
            if not self.results_frame.winfo_ismapped():
                self.results_frame.pack(fill=tk.BOTH, expand=True)
            self.status_var.set(f"Error: {str(e)}")
    
    def decompress_file(self):
        """Decompress a .bin file. If a .txt file is selected, use its corresponding .bin."""
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        
        if self.selected_file.endswith('.txt'):
            base_path, _ = os.path.splitext(self.selected_file)
            compressed_file = f"{base_path}.bin"
            if not os.path.exists(compressed_file):
                messagebox.showwarning("Warning", "Compressed file not found for the selected text file!")
                return
        elif self.selected_file.endswith('.bin'):
            compressed_file = self.selected_file
        else:
            messagebox.showwarning("Warning", "Unsupported file format for decompression!")
            return
        
        try:
            result = self.compressor.decompress_file(compressed_file)
            
            self.status_message_var.set(f"Decompression Successful! Saved as: {os.path.basename(result['path'])}")
            self.status_message.config(bg=SUCCESS_COLOR)
            
            # Show decompressed text
            self.result_text_frame.config(text="Decompressed Text")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result['text'])
            
            if not self.results_frame.winfo_ismapped():
                self.results_frame.pack(fill=tk.BOTH, expand=True)
            
            self.status_var.set("Decompression complete!")
        except Exception as e:
            self.status_message_var.set(f"Decompression Failed: {str(e)}")
            self.status_message.config(bg=ACCENT_COLOR)
            if not self.results_frame.winfo_ismapped():
                self.results_frame.pack(fill=tk.BOTH, expand=True)
            self.status_var.set(f"Error: {str(e)}")

if __name__ == "__main__":
    app = HuffmanApp()
    app.mainloop()
