
# Project Monolith

![Project Monolith](frontend/images/project%20MONOLITH.png) <!-- Add a banner or representative image for the project if available -->

## Overview

**Project Monolith** is a cross-platform application designed for Linux and Windows, providing cybersecurity professionals and ethical hackers with a comprehensive suite of tools for vulnerability assessment, intelligence gathering, and secure operations. With an intuitive frontend and powerful backend, Project Monolith consolidates essential tools to enhance efficiency and streamline the penetration testing and security evaluation process.

## Features

### 1. Website Vulnerability Assessment
- Access robust pentesting tools to analyze and detect vulnerabilities in websites and web applications:
  - **Nmap**: Network scanning and discovery.
  - **Nikto**: Comprehensive web server scanner.
  - **Amass**: Subdomain enumeration and information gathering.

### 2. OSINT (Open Source Intelligence)
- A suite of tools designed for data collection and analysis to aid in:
  - System penetration.
  - Security evaluation.

### 3. Miscellaneous Utilities
- Additional tools to support cybersecurity operations, including:
  - **Encryption and Decryption functionalities**.
  - Other utilities to streamline various security tasks.

## Technical Details

### Backend
- Developed using **Python** to ensure efficient execution of tools and processes.

### Frontend
- Built with **HTML**, **CSS**, and **JavaScript** for an intuitive and responsive user experience.
- Integrated using **PyWebView** to seamlessly bridge the frontend and backend.

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)
- Node.js and npm (for frontend development, if needed)
- **Nmap, Nikto, Amass, and other required tools must be installed on your system.**

### Automatic Installation
To simplify the setup process, we provide automated installation scripts for both Linux and Windows.

#### Linux
Run the following command to execute the setup script:
```bash
chmod +x setup.sh && ./setup.sh
```

#### Windows
Run the following command in PowerShell:
```powershell
setup.bat
```

### Manual Installation
If you prefer to install dependencies manually, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/notme6000/project-monolith.git
   cd project-monolith
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install required tools manually if not already installed:
   ```bash
   sudo apt install nmap nikto amass  # For Debian-based Linux
   sudo pacman -S nmap nikto amass  # For Arch-based Linux
   winget install Nmap  # For Windows
   ```
4. Run the application:
   ```bash
   python main.py
   ```

### Running on Linux or Windows
- Ensure all dependencies are installed and permissions are configured appropriately for your operating system.

## Usage

1. Launch the application using the instructions above.
2. Navigate through the three main sections:
   - Perform vulnerability assessments using tools like Nmap, Nikto, or Amass.
   - Gather intelligence with OSINT tools.
   - Utilize miscellaneous utilities for encryption, decryption, and more.
3. Results are displayed in a user-friendly interface, and outputs from tools can be viewed in dedicated windows.

## Screenshots
<!-- Add screenshots or images to visually represent the app -->

![monolith screenshot](screenshot/OSINT.png)
![monolith screenshot](screenshot/misc.png)
![monolith screenshot](screenshot/encryption.png)
![monolith screenshot](screenshot/web-pentesting.png)



## Contributing

We welcome contributions from the community! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git commit -m "Add feature name"
   git push origin feature-name
   ```
4. Create a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Nmap, Nikto, and Amass** for their powerful tools.
- The open-source community for inspiration and resources.

## Disclaimer

**Project Monolith** is intended for ethical hacking and cybersecurity purposes only. The authors and contributors do not condone illegal activities or misuse of this tool.

---

**Follow Us**  
Stay updated with the latest features and releases by following this repository.
