# -*- coding: cp1252 -*-

def my_split(s, sep):
    if not s or not sep:
        return []
    return s.split(sep)

class Employee:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def ask_name(self):
        try:
            self.name = str(input("Please enter employee name:"))
        except ValueError:
            print("Invalid input. Please enter a valid name.")

class SalaryEmployee(Employee):
    def __init__(self, id, name, salary, monthly_salary):
        super().__init__(id, name)
        self.salary = 'M'
        self.monthly_salary = int(monthly_salary)

    def set_salary(self):
        try:
            self.monthly_salary = int(input("Please enter monthly salary:"))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        return self.monthly_salary

class HourlyEmployee(SalaryEmployee):
    def __init__(self, id, name, salary, hours_worked, hour_rate, monthly_salary):
        super().__init__(id, name, salary, monthly_salary)
        self.hours_worked = hours_worked
        self.hour_rate = hour_rate
        self.salary = 'H'
        self.monthly_salary = int(monthly_salary)

    def set_salary(self):
        try:
            self.hours_worked = int(input("Please enter hours worked:"))
            self.hour_rate = int(input("Please enter hour rate:"))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        self.monthly_salary = round(self.hour_rate * self.hours_worked)
        return self.monthly_salary

class CommissionEmployee(SalaryEmployee):
    def __init__(self, id, name, salary, base_salary, commission, monthly_salary):
        super().__init__(id, name, salary, monthly_salary)
        self.base_salary=base_salary
        self.commission = commission
        self.salary = 'C'
        self.monthly_salary = int(monthly_salary)

    def set_salary(self):
        try:
            self.base_salary = int(input("Please enter monthly salary:"))
            self.commission = int(input("Please enter commission:"))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        self.monthly_salary = self.base_salary + self.commission
        return self.monthly_salary

class PayrollSystem:
    def calculate_payroll(self, employees):
        for employee in employees:
            print('Employee Payroll')
            print('================')
            print(f'Payroll for: {employee.id} - {employee.name}')
            print(f'- Check amount: {employee.monthly_salary}')
            print('')

def readEmployees():
    file_path = "employee.csv"
    with open(file_path, "r") as file:
        content = file.readlines()
        employees = []
        for line in content:
            data = my_split(line.rstrip(), ",")
           
            if len(data)==4:
                id, name, salary, monthly_salary = data
                employee = SalaryEmployee(id, name, salary, monthly_salary)
                employees.append(employee)
            elif len(data) == 5 and data[2] == 'H':
                id, name, salary, hours_worked, hour_rate = data
                employee = HourlyEmployee(int(id), name, salary, int(hours_worked), int(hour_rate), monthly_salary=int(hours_worked)*int(hour_rate))
                employees.append(employee)
            elif len(data) == 5 and data[2] == 'C':
                id, name, salary, base_salary, commission = data
                employee = CommissionEmployee(int(id), name, salary, int(base_salary), int(commission),monthly_salary=int(base_salary)+int(commission))
                employees.append(employee)
        
    return employees


def writeEmployeesToFile(employees):
    file_path = "employee.csv"
    with open(file_path, "w") as file:
        data = ""
        for e in employees:
            if e.salary=="M":
                data += f"{e.id},{e.name},{e.salary},{e.monthly_salary}\n"
            elif e.salary=="H":
                data += f"{e.id},{e.name},{e.salary},{e.hours_worked},{e.hour_rate}\n"
            elif e.salary=="C":
                data += f"{e.id},{e.name},{e.salary},{e.base_salary},{e.commission}\n"
        file.write(data)
    print(f"{len(employees)}  employee(s) added to employee.csv")
    
    
def checkFile():
    file_path = 'employee.csv'
    try:
        # Trying to open the file in read mode.
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            if lines:
                # If the file is not empty, this takes the last value of id.
                last_line = lines[-1]
                if last_line.strip():  # Check if the last line is not empty or just whitespace
                    id = int(last_line.split(',')[0]) + 1
                    employees = readEmployees()
                else:
                    id = 1
                    employees = []
            else:
                # If the file is empty, this sets id to 1, also set employees as an empty list.
                id = 1
                employees = []
    except FileNotFoundError:
        # If the file does not exist, this creates it and sets id to 1 and employee as an empty list.
        with open(file_path, 'w') as file:
            id = 1
            employees = []
            
    initial_values = [id, employees]
    return initial_values

def main():
    result = checkFile()
    id = result[0]
    employees = result[1]
    

    while True:
        print("(1) Add employee to employees\n(2) Write employees to file\n(3) Read employees from file\n(4) Print payroll\n(0) Quit\n")
        selection = int(input("Please select one: "))
        
        if selection == 1:
            while True:
                salarytype = int(input("Please enter salary type:\n(1) monthly\n(2) hourly\n(3) commission\n(0) Quit\n"))
                if salarytype == 1:
                    employee = SalaryEmployee(id, '', '', 0)
                    employee.ask_name()
                    employee.set_salary()
                    employees.append(employee)
                    id += 1
                elif salarytype == 2:
                    employee = HourlyEmployee(id, '', '', 0,0,0)
                    employee.ask_name()
                    employee.set_salary()
                    employees.append(employee)
                    id += 1
                elif salarytype == 3:
                    employee = CommissionEmployee(id, '','',0, 0,0)
                    employee.ask_name()
                    employee.set_salary()
                    employees.append(employee)
                    id += 1
                elif salarytype == 0:
                    break
                else:
                    print("Incorrect selection.")
            
        elif selection == 2:
            writeEmployeesToFile(employees)
            
        elif selection == 3:
            employees=readEmployees()
            print(f"{len(employees)}  employee(s) read from employee.csv")
            
        elif selection == 4:
            payroll_system = PayrollSystem()
            payroll_system.calculate_payroll(employees)
            
        elif selection == 0:
            print("Service shutting down, thank you.")
            break
    
        else:
            print("Incorrect selection.")

if __name__ == "__main__":
    main()