# Huffman Coding Compression Tool

A user-friendly desktop application for compressing and decompressing text files using the Huffman coding algorithm. Built with Python and Tkinter, this tool provides an intuitive graphical interface for efficient file compression.

## Features

- **File Compression**: Compress text files (.txt) using Huffman coding algorithm
- **File Decompression**: Decompress previously compressed files back to original format
- **Visual Interface**: Clean, modern GUI built with Tkinter
- **Compression Statistics**: View original size, compressed size, and compression ratio
- **Huffman Code Display**: See the generated Huffman codes for each character
- **File Preview**: Preview text file contents before compression
- **Multiple File Support**: Works with various text file formats

## Screenshot
<img width="888" height="738" alt="Screenshot 2025-09-27 at 1 59 11 PM" src="https://github.com/user-attachments/assets/bbd55157-50b2-4641-a129-98768dcd145d" />


The application features a modern interface with:
- File selection and preview
- One-click compression and decompression
- Real-time compression statistics
- Huffman code visualization

## Installation

### Prerequisites

- Python 3.6 or higher
- Required Python packages (install via pip):

```bash
pip install bitarray
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/huffman-compression-tool.git
cd huffman-compression-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Compressing Files

1. Click **Browse** to select a text file (.txt)
2. The file content will be displayed in the preview area
3. Click **Compress** to create a compressed version
4. The compressed file will be saved with a `.bin` extension
5. View compression statistics and Huffman codes in the results area

### Decompressing Files

1. Select either:
   - The original `.txt` file (if corresponding `.bin` exists)
   - The compressed `.bin` file directly
2. Click **Decompress** to restore the original content
3. The decompressed file will be saved with `_decompressed` suffix
4. View the restored content in the results area

## How It Works

The Huffman coding algorithm works by:

1. **Frequency Analysis**: Counting character frequencies in the input text
2. **Tree Building**: Creating a binary tree where frequent characters have shorter codes
3. **Code Generation**: Assigning binary codes to each character
4. **Compression**: Replacing characters with their binary codes
5. **Decompression**: Using the stored tree to decode binary data back to text
   

## Technical Details

- **Algorithm**: Huffman Coding
- **GUI Framework**: Tkinter
- **File Format**: Binary (.bin) with pickle serialization
- **Compression**: Uses bitarray for efficient bit manipulation
- **Character Encoding**: UTF-8 support

## Compression Performance

Compression ratios vary based on text content:
- **Repetitive text**: 60-80% size reduction
- **Natural language**: 40-60% size reduction
- **Random text**: 10-30% size reduction

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on the Huffman coding algorithm developed by David A. Huffman
- Built using Python's Tkinter for cross-platform GUI support
- Uses bitarray library for efficient binary data handling
