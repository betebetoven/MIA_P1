
# EXT2/EXT3 Filesystem Simulation with Command Line Interface

This project is an academic endeavor that simulates the Linux EXT2 and EXT3 filesystems using a command line interface. The core of this project lies in its implementation of an interpreter, crafted using the PLY (Python Lex-Yacc) library. This interpreter allows for the simulation of a hard disk, creation of partitions, and the establishment of the desired filesystem, providing a comprehensive understanding of filesystem management and operations.

## Project Overview

The project aims to deliver a hands-on experience with the inner workings of the EXT2 and EXT3 filesystems, offering insights into partition management, filesystem creation, and file manipulation. Utilizing the PLY library, a custom grammar was developed to interpret commands related to filesystem operations, making it an ideal showcase for understanding and designing complex grammars.

## Features

- **Simulation of Hard Disk**: Create a virtual representation of a hard disk to experiment with.
- **Partition Management**: Allows for the creation and manipulation of disk partitions.
- **Filesystem Creation and Management**: Supports the creation of EXT2 and EXT3 filesystems and managing files within these partitions.
- **Custom Grammar for Filesystem Operations**: A highlight of the project, showcasing the ability to design and implement complex grammars using PLY.

## Getting Started

To get started with this simulation, follow the steps below to set up the environment and run the project on your local machine.

### Prerequisites

- Python 3.x
- PLY (Python Lex-Yacc)

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/EXT2-EXT3-Filesystem-Simulation.git
   ```

2. **Navigate to the project directory**

   ```sh
   cd EXT2-EXT3-Filesystem-Simulation
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

### Usage

Run the main interpreter interface using Python:

```sh
python main.py
```

Follow the command-line prompts to simulate hard disk operations, create partitions, and manage your EXT2/EXT3 filesystems.

## Example Commands

- `mkdisk -size=500B` - Simulates the creation of a 500B hard disk.
- `fdisk` - Partitions the disk into EXT2 or EXT3 filesystem.
- `rep` - Displays  different kinds of information from the filesystem or the disk.

this project was made for academic porpouses, but I think it is an excellent exercise to understand ext2 and ext3 filesystems, also the command line was made with PLY, you can see the grammar in the main.py file.
I tried to make it as less ambiguous as possible, but also taking advantages of the nature of the Python language and the use of Json objects, so the Grammar can seem ambiguous in some parts but it was intentional.
Hope this code helps you understand filesystems and the use of Grammars and Interpreters.

## Contributing

Contributions are welcome to enhance the simulation, fix bugs, or improve the documentation. Follow the standard fork and pull request workflow.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- Gratitude to the developers of PLY for providing a powerful tool for lexer and parser generation.
- Appreciation to all contributors and the academic community for guidance and support.
