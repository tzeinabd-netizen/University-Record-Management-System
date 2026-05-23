"""UI for the University Record Management System.

A sidebar lists queries, the right panel shows the inputs each query needs,
and the bottom panel shows the results in a table.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from sqlalchemy.orm import Session

from backend.queries import (
    all_course_students,
    final_year_students_above_70,
    students_not_enrolled,
    student_faculty_advisor_information,
    lecturer_publications_report,
    students_failed_courses,
    top_performing_courses,
    research_project_members,
    course_popularity_stats,
    lecturer_workload_stats,
    display_all_student_records,
    display_all_course_records,
    display_all_lecturer_records,
)

# Each entry: (sidebar label, description, query function,
#              [(input_label, int | str), ...]).
# Inputs use `int` for an ID spin box and `str` for a text field. They are
# passed to the query function positionally, in declaration order, after `db`.
QUERIES = [
    ("Students in a course taught by a lecturer",
        "Find all students enrolled in a specific course taught by a particular lecturer.",
        all_course_students, [("Course Name", str), ("Lecturer Last Name", str)]),
    
    ("Final-year students with average > 70%",
        "List students in their final year of studies whose average grade exceeds 70%.",
        final_year_students_above_70, []),
    
    ("Students not enrolled",
        "Identify students who have not registered for any courses.",
        students_not_enrolled,
        []),
    
    ("Advisor information for a student",
        "Retrieve the contact information for the faculty advisor of a specific student.",
        student_faculty_advisor_information, [("Student Last Name", str)]),
    
    ("Lecturer publications (previous year)",
        "Report a lecturer's publications from the past calendar year.",
        lecturer_publications_report, [("Publication year", int)]),
    
    ("Failed student courses",
        "Identify students who failed at least one course (grade < 40%)",
        students_failed_courses, []),
    
    ("Top performing courses",
        "Identify the top-performing courses based on average student grades.",
        top_performing_courses, []),
    
    ("Research project members",
        "Identify students and lecturers involved in research projects.",
        research_project_members, []),
    
    ("Course popularity stats",
        "Course popularity statistics with ranking.",
        course_popularity_stats, []),
    
    ("Lecturer workload stats",
        "Lecturer workload statistics with ranking.",
        lecturer_workload_stats, []),

    ("Display all student records",
     "",
    display_all_student_records, []),
    
    ("Display all course records",
     "",
    display_all_course_records, []),
    
    ("Display all lecturer records",
     "",
    display_all_lecturer_records, []),    
]


def _make_input(kind: type, default: int | None = None) -> QWidget:
    """Build the input widget for a field type."""
    if kind is int:
        box = QSpinBox()
        box.setRange(1, 9_999_999)
        if default!=None:
            box.setValue(default)
        return box
    return QLineEdit()


def _read_input(widget: QWidget) -> object:
    """Read the current value out of an input widget."""
    if isinstance(widget, QSpinBox):
        return widget.value()
    return widget.text().strip()


def _to_rows(result: object) -> list[dict[str, object]]:
    """Convert a query result into a list of {column: value} dicts."""
    def as_dict(obj: object) -> dict[str, object]:
        if obj is None:
            return {}
        if hasattr(obj, "__table__"):
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        # Multi-column row, e.g. query(Lecturer, project_count).all() -> Row
        if hasattr(obj, "_mapping"):
            merged: dict[str, object] = {}
            for key, val in obj._mapping.items():
                if hasattr(val, "__table__"):
                    merged.update({c.name: getattr(val, c.name) for c in val.__table__.columns})
                else:
                    merged[str(key)] = val
            return merged
        return {"value": str(obj)}

    if result is None:
        return []
    # department_staff_members returns (lecturers, non_academic_staff).
    if isinstance(result, tuple):
        lecturers, staff = result
        return ([{"role": "Lecturer", **as_dict(x)} for x in lecturers]
                + [{"role": "Non-academic", **as_dict(x)} for x in staff])
    if isinstance(result, list):
        return [as_dict(x) for x in result]
    return [as_dict(result)]


class MainWindow(QMainWindow):
    """Sidebar + per-query form + results table."""

    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        self.setWindowTitle("University Record Management System")
        self.resize(1600, 900)

        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(400)

        self.forms = QStackedWidget()
        self.form_inputs: list[list[tuple[str, QWidget]]] = []

        for label, description, _, fields in QUERIES:
            self.sidebar.addItem(label)
            self.forms.addWidget(self._build_form(label, description, fields))

        self.results = QTableWidget()
        self.results.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results.setAlternatingRowColors(True)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.forms)
        right_layout.addWidget(QLabel("<b>Results</b>"))
        right_layout.addWidget(self.results, stretch=1)
        right = QWidget()
        right.setLayout(right_layout)

        central = QWidget()
        central_layout = QHBoxLayout(central)
        central_layout.addWidget(self.sidebar)
        central_layout.addWidget(right, stretch=1)
        self.setCentralWidget(central)

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready.")

        self.sidebar.currentRowChanged.connect(self.forms.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

    def _build_form(self, label: str, description: str,
                    fields: list[tuple[str, type]]) -> QWidget:
        """Create one query's input page and remember its input widgets."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel(f"<h3>{label}</h3>"))

        desc = QLabel(description)
        layout.addWidget(desc)

        widgets: list[tuple[str, QWidget]] = []
        form = QFormLayout()
        for field_label, kind in fields:
            widget = _make_input(kind, 2020)
            
            form.addRow(field_label, widget)
            widgets.append((field_label, widget))
        layout.addLayout(form)

        run = QPushButton("Run query")
        run.clicked.connect(self._on_run)
        layout.addWidget(run)
        layout.addStretch()

        self.form_inputs.append(widgets)
        return page

    def _on_run(self) -> None:
        """Read the current form's inputs, run its query, show the results."""
        i = self.forms.currentIndex()
        _, _, query_func, _ = QUERIES[i]

        args: list[object] = []
        for field_label, widget in self.form_inputs[i]:
            value = _read_input(widget)
            if isinstance(value, str) and not value:
                QMessageBox.warning(
                    self, "Missing input",
                    f"Please provide a value for '{field_label}'.",
                )
                return
            args.append(value)

        try:
            rows = _to_rows(query_func(self.db, *args))
        except Exception as e:
            QMessageBox.critical(self, "Database error", str(e))
            self.statusBar().showMessage("Query failed.")
            return

        self._populate_results(rows)
        self.statusBar().showMessage(f"Query: \"{QUERIES[i][0]}\" returned {len(rows)} rows.")

    def _populate_results(self, rows: list[dict[str, object]]) -> None:
        """Fill the results table from a list of dict rows."""
        self.results.clear()
        if not rows:
            self.results.setRowCount(0)
            self.results.setColumnCount(0)
            return

        headers = list(rows[0].keys())
        
        self.results.setColumnCount(len(headers))
        self.results.setRowCount(len(rows))
        
        headers_displayed=[i.title().replace("_", " ") for i in headers]
        self.results.setHorizontalHeaderLabels(headers_displayed)

        for r, row in enumerate(rows):
            for c, key in enumerate(headers):
                item = QTableWidgetItem(str(row.get(key, "")))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                self.results.setItem(r, c, item)
        self.results.resizeColumnsToContents()
