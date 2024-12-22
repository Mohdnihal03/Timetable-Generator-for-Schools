# Timetable Generator for Schools

This project is a **Timetable Generator for Schools**, using a combination of traditional methods and a **Genetic Algorithm** to create optimal schedules. While functional, this approach may occasionally produce inaccuracies, depending on the dataset quality. I am currently exploring a hybrid approach that integrates traditional methods with machine learning to enhance accuracy and adaptability.

---

## Purpose of the Project

The primary aim of this project is to automate the generation of school timetables. It seeks to:

- Save time and effort compared to manual scheduling.
- Ensure fairness and balance in resource allocation.
- Adhere to constraints such as subject hours, teacher availability, and lab schedules.

---

## Getting Started

### Prerequisites

1. Create a `.env` file in the root directory to store environment variables (if needed for advanced features):

```env
# Example environment variables
KEY=your_key
```

2. Set up a virtual environment and install the required Python dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Running the Project

To generate the timetable, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. Activate the virtual environment if it is not already activated:

```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Run the main script:

```bash
python main.py
```

---

## Key Features

- **Traditional Method**: A rule-based approach for generating timetables.
- **Genetic Algorithm**: An optimization technique that enhances the timetable's quality by simulating natural selection.
- **Visualization**: Timetable visualization implemented using Plotly for clear and interactive displays.
- **Constraints Checking**: Ensures all constraints, such as teacher availability and room allocation, are respected.
- **Validation**: Cross-checks the generated timetable for logical inconsistencies.

---

## Limitations

As this project uses a traditional approach combined with a Genetic Algorithm, results may not always be optimal or accurate. The outcome depends heavily on the dataset's structure and quality.

---

## Future Work

I am actively working on integrating **Machine Learning** into the timetable generation process to enhance its accuracy and scalability. This hybrid approach aims to address the limitations of the current system.

If you are interested in contributing or collaborating, feel free to contact me:

**Email**: mohd.nihalll@gmail.com

---

## Contributions

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request with your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
