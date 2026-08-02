# 🏢 Core Employee Domain Model

A robust, object-oriented Python module designed as the foundational business logic for an HR Management backend. This model demonstrates strict data validation, state management, and encapsulation, making it ideal for integration with web frameworks like FastAPI, Django, or Flask.

## 🚀 Key Features

* **Data Encapsulation & Integrity:** Utilizes Python `@property` decorators to enforce strict getter/setter rules, preventing unauthorized mutation of core identifiers (like `employee_id`).
* **Business Logic Validation:** Built-in validation constraints for salaries and hikes, ensuring data consistency before it ever reaches a database.
* **Class-Level State Management:** Tracks organizational-level metrics (like `total_employees`) independently of instance states.
* **Secure Attributes:** Implements Python's name mangling (`__`) for sensitive data (e.g., PAN numbers) and protected access (`_`) for internal attributes.
* **Developer Friendly:** Clean `__str__` representations for easy logging and debugging in a web server environment.

## 📁 File Structure

```text
├── employee.py       # Core domain model and execution script
└── README.md         # Documentation

```

## 💻 Usage

This module can be executed directly to view the demonstration in the terminal, or imported into a larger backend service.

### Running the Demo

```bash
python employee.py

```

### Importing into a Web Service (Example)

```python
from employee import Employee

# Example FastAPI route
@app.post("/employees/")
def create_employee(name: str, emp_id: int, dept: str, salary: float, pan: str):
    try:
        new_emp = Employee(name, emp_id, dept, salary, pan)
        return {"status": "success", "employee": str(new_emp)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

```

## 🛠️ The Code (`employee.py`)

```python
class Employee:
    """
    Core Domain Model for an Employee.
    Handles business logic, validation, and state representation.
    """
    company_name = "TechCorp Solutions"
    pf_percentage = 0.12
    MIN_SALARY = 15000
    MAX_SALARY = 500000
    total_employees = 0

    def __init__(self, name, employee_id, department, salary, pan_number):
        self.name = name
        self._employee_id = employee_id
        self._department = department
        self.__pan_number = pan_number  # Strictly private via name mangling
        self.salary = salary            # Uses setter for validation
        Employee.total_employees += 1

    @property
    def employee_id(self):
        """Read-only property. Cannot be mutated after initialization."""
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        raise AttributeError("Employee ID is immutable and cannot be changed after creation.")

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        """Validates numerical types and domain-specific boundaries."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Salary must be a numerical value.")
        if not self.MIN_SALARY <= value <= self.MAX_SALARY:
            raise ValueError(f"Salary must be between {self.MIN_SALARY} and {self.MAX_SALARY}.")
        self._salary = value

    def apply_hike(self, percentage):
        """Applies a percentage-based hike with boundary validation."""
        if isinstance(percentage, bool) or not isinstance(percentage, (int, float)):
            raise TypeError("Hike percentage must be a numerical value.")
        if not 0 <= percentage <= 50:
            raise ValueError("Hike percentage must be between 0 and 50.")
        self.salary = self.salary * (1 + percentage / 100)

    def calculate_pf(self):
        """Calculates Provident Fund based on class-level constraints."""
        return self.salary * self.pf_percentage

    def transfer_department(self, new_department):
        if not isinstance(new_department, str) or not new_department.strip():
            raise ValueError("Department assignment cannot be empty.")
        self._department = new_department

    @classmethod
    def get_total_employees(cls):
        """Returns the organizational headcount."""
        return cls.total_employees
        
    @classmethod
    def is_valid_salary(cls, salary):
        """Utility method to validate salary prior to instantiation."""
        return cls.MIN_SALARY <= salary <= cls.MAX_SALARY

    def __str__(self):
        """Standardized string representation for server logs and CLI."""
        return (
            f"Employee[{self.employee_id}] {self.name} | "
            f"{self._department} | Rs.{self.salary:,.2f}"
        )


def main():
    """Demonstration of model capabilities."""
    print(f"🏢 Company: {Employee.company_name}")
    print(f"👥 Initial Headcount: {Employee.get_total_employees()}\n")

    # Initialization
    e1 = Employee("Ravi Kumar", 101, "Engineering", 60000, "ABCDE1234F")
    e2 = Employee("Anita Sharma", 102, "Finance", 75000, "PQRSX5678K")

    print("--- Current Roster ---")
    print(e1)
    print(e2)
    print(f"\n👥 Updated Headcount: {Employee.get_total_employees()}\n")

    # Business Logic execution
    print("--- Financial Operations ---")
    print(f"PF for {e1.name}: Rs.{e1.calculate_pf():,.2f}")
    
    e1.apply_hike(10)
    print(f"Salary post 10% hike for {e1.name}: Rs.{e1.salary:,.2f}\n")

    # State mutations
    old_dept = e1._department
    e1.transfer_department("Data Science")
    print(f"🔄 Transfer: {e1.name} moved from {old_dept} to {e1._department}\n")

    # Validation Checks
    print("--- Validation & Security Handling ---")
    print(f"Checking if 9000 is a valid starting salary: {Employee.is_valid_salary(9000)}")

    try:
        e1.salary = 5000
    except ValueError as err:
        print(f"🔒 Blocked invalid salary mutation: {err}")

    try:
        e1.employee_id = 999
    except AttributeError as err:
        print(f"🔒 Blocked ID mutation: {err}")

    # Security demonstration
    print(f"\nProtected attribute access (Department): {e1._department}")
    print(f"Private attribute access via mangling (PAN): {e1._Employee__pan_number}")
    print("\nNote: Protected members are convention-based, while private members use name mangling to prevent accidental access.")

if __name__ == "__main__":
    main()

```
