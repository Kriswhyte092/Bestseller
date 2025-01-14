from fpdf import FPDF
from typing import Dict

class payslip_generator:
    def generate_payslip(self, employee: Dict, payroll_data: Dict) -> Dict:
        """
        Generates the payslip data for a specific employee.
        :param employee: The employee data (from the employee API).
        :param payroll_data: The payroll data (hours worked and pay).
        :return: A dictionary representing the payslip data.
        """
        # Calculate deductions
        total_pay = payroll_data['total_pay']
        deductions = total_pay * self.tax_rate  # Simple tax deduction example
        net_pay = total_pay - deductions
        
        # Generate payslip data
        payslip = {
            'employee_name': employee['name'],
            'employee_id': employee['id'],
            'department': employee.get('department', 'Unknown'),
            'position': employee.get('position', 'Unknown'),
            'period': 'January 2025',  # This can be dynamic depending on your needs
            'basic_pay': payroll_data['total_pay'],
            'deductions': deductions,
            'net_pay': net_pay,
        }

        return payslip

    def format_payslip(self, payslip_data: Dict) -> str:
        """
        Formats the payslip data into a human-readable text format.
        :param payslip_data: The payslip data.
        :return: A formatted payslip as a string.
        """
        payslip_text = f"Payslip for {payslip_data['employee_name']}\n"
        payslip_text += f"Employee ID: {payslip_data['employee_id']}\n"
        payslip_text += f"Department: {payslip_data['department']}\n"
        payslip_text += f"Position: {payslip_data['position']}\n"
        payslip_text += f"Period: {payslip_data['period']}\n\n"

        payslip_text += f"Basic Pay: ${payslip_data['basic_pay']:.2f}\n"
        payslip_text += f"Deductions (Tax): ${payslip_data['deductions']:.2f}\n"
        payslip_text += f"Net Pay: ${payslip_data['net_pay']:.2f}\n\n"

        payslip_text += "Thank you for your hard work!\n"
        payslip_text += f"Company: {self.company_name}"

        return payslip_text

    def generate_pdf(self, payslip_text: str, employee_id: str) -> str:
        """
        Converts the payslip text into a PDF and saves it with a filename.
        :param payslip_text: The formatted payslip text.
        :param employee_id: The employee's ID to use in the PDF filename.
        :return: The file path of the generated PDF.
        """
        # Create a PDF instance
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        
        # Add payslip content
        pdf.multi_cell(0, 10, payslip_text)

        # Save the PDF file
        file_path = f"payslip_{employee_id}.pdf"
        pdf.output(file_path)
        
        return file_path
