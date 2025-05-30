# 🔐 Text Cipher App

A sleek and modern Python GUI application for encrypting and decrypting text using classical cipher techniques. Built with the [Flet](https://flet.dev/) framework, this app combines elegant design with real-time functionality and comprehensive support for multiple cipher algorithms.

---

## ✨ Features

- 🔢 **8 Classical Ciphers** – Complete implementation of Playfair, Monoalphabetic, Caesar, Vigenère, Substitution, Rail Fence, Transposition, and Affine ciphers
- ⚡ **Real-Time Processing** – Output updates instantly as you type with live validation
- 🎯 **Smart Input Validation** – Comprehensive error handling with helpful feedback messages
- 🌓 **Dark & Light Mode Toggle** – Seamless theme switching with animated transitions
- 📱 **Responsive Design** – Adaptive layout that works perfectly on desktop and mobile
- 🔄 **Encrypt/Decrypt Toggle** – Single-click mode switching with visual indicators
- 📂 **File Operations** – Upload text files and save encrypted/decrypted results
- 🔄 **Input/Output Swap** – Instantly swap input and output content
- 🎨 **Modern UI/UX** – Material Design 3 with smooth animations and intuitive navigation
- 📋 **Built-in Help** – Contextual information cards for each cipher algorithm

---

## 🧠 Supported Cipher Algorithms

### **Playfair Cipher**
- Symmetric encryption using a 5×5 letter grid
- Key: Alphabetic characters only
- Features: Classic digraph substitution

### **Monoalphabetic Cipher** 
- Fixed letter substitution cipher
- Key: 26 unique letters (optional - uses default if empty)
- Features: Simple character mapping

### **Caesar Cipher**
- Shift cipher with configurable offset
- Key: Numeric value (-25 to 25)
- Features: Historical Roman encryption method

### **Vigenère Cipher**
- Polyalphabetic substitution using keyword
- Key: Alphabetic characters only
- Features: Repeating key pattern encryption

### **Substitution Cipher**
- Direct character replacement cipher
- Key: Exactly 26 unique letters
- Features: Custom alphabet substitution

### **Rail Fence Cipher**
- Zigzag transposition cipher
- Key: Number of rails (must be >1)
- Features: Geometric pattern encryption

### **Transposition Cipher**
- Columnar rearrangement cipher
- Key: Number of columns (must be >1)
- Features: Position-based scrambling

### **Affine Cipher**
- Mathematical linear transformation
- Key: Format 'a,b' where 'a' must be coprime with 26
- Features: Algebraic encryption method

---

## 🎨 Interface Highlights

### **Desktop Experience**
- Full tabbed interface with all 8 ciphers
- Side-by-side input/output layout
- Comprehensive file operations toolbar
- Real-time theme switching

### **Mobile Experience**
- Bottom navigation with cipher selector
- Optimized touch-friendly controls
- Responsive layout adaptation
- Modal cipher selection dialog

### **Smart Validation**
- Real-time input validation with visual feedback
- Context-aware error messages
- Automatic error recovery
- Input format guidance and hints

---

## 🚀 Getting Started

### 📋 Prerequisites
- Python 3.7+
- Flet framework
- Custom cipher modules (included)

### 🛠 Installation

1. **Install Flet**:
```bash
pip install flet
```

2. **Ensure cipher modules are available**:
The app requires these cipher implementation files:
- `playfair.py`
- `monoalphabetic.py` 
- `caesar.py`
- `vigenere.py`
- `substitution.py`
- `transposition.py`
- `rail_fence.py`
- `affine.py`

3. **Run the application**:
```bash
python main.py
```

---

## 📱 Usage Guide

### **Basic Operation**
1. Select your desired cipher from the tabs (desktop) or navigation (mobile)
2. Enter your text in the input field
3. Configure the cipher key according to the format requirements
4. Toggle between Encrypt/Decrypt modes
5. View real-time results in the output field

### **File Operations**
- **Upload**: Click "Upload File" to load text from .txt files
- **Save**: Click "Save Output" to export results
- **Swap**: Use the swap button to exchange input/output content

### **Theme Customization**
- Toggle between Dark and Light modes using the theme switch
- Automatic adaptation of colors and contrast
- Persistent theme preference during session

---

## 🏗️ Architecture

### **Component Structure**
- `CipherValidator`: Comprehensive input validation class
- `build_cipher_tab()`: Dynamic tab generation system  
- Modular cipher implementations with consistent interface
- Responsive layout system with breakpoint handling

### **Key Features**
- **Error Handling**: Graceful error management with user feedback
- **State Management**: Efficient UI state synchronization
- **Performance**: Optimized real-time text processing
- **Accessibility**: Semantic UI elements and keyboard navigation

---

## 🎯 Technical Specifications

- **Framework**: Flet (Python GUI framework)
- **Design System**: Material Design 3
- **Theme Support**: Dynamic dark/light mode switching
- **Responsiveness**: Mobile-first adaptive design
- **File Formats**: UTF-8 text file support
- **Validation**: Real-time input validation with regex patterns
- **Animation**: Smooth transitions and visual feedback

---

## 🔮 Future Enhancements

- Additional cipher algorithms (RSA, DES, AES)
- Batch file processing capabilities
- Cipher strength analysis tools
- Export to multiple file formats
- Cipher combination and chaining
- Historical cipher information and tutorials

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features through the issue tracker.

---

*Built with ❤️ using Python and Flet framework*
