from fpdf import FPDF

class PayslipGenerator:
    def __init__(self, company_name, company_address, company_id):
        self.company_name = company_name
        self.company_address = company_address
        self.company_id = company_id

    def generate_payslip(self, payslip_data, output_file):
        """
        Generates a payslip PDF based on the provided data.
        
        :param payslip_data: Dictionary containing all payslip details.
        :param output_file: Path to save the generated PDF.
        """
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Set Title Font
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Payslip', ln=True, align='C')

        # Add Employee Details
        pdf.set_font('Arial', '', 12)
        pdf.ln(10)
        pdf.cell(100, 10, f"Employee Name: {payslip_data['employee_name']}")
        pdf.cell(0, 10, f"Date: {payslip_data['date']}", ln=True)
        pdf.cell(100, 10, f"National ID: {payslip_data['national_id']}")
        pdf.cell(0, 10, f"Period: {payslip_data['period']}", ln=True)
        pdf.cell(100, 10, f"Payslip No: {payslip_data['payslip_number']}")
        pdf.cell(0, 10, f"Department: {payslip_data['department']}", ln=True)

        # Earnings Section
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Earnings:', ln=True)
        pdf.set_font('Arial', '', 12)
        for earning in payslip_data['earnings']:
            pdf.cell(100, 10, earning['description'])
            pdf.cell(0, 10, f"${earning['amount']:.2f}", ln=True)

        # Deductions Section
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Deductions:', ln=True)
        pdf.set_font('Arial', '', 12)
        for deduction in payslip_data['deductions']:
            pdf.cell(100, 10, deduction['description'])
            pdf.cell(0, 10, f"${deduction['amount']:.2f}", ln=True)

        # Summary Section
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(100, 10, 'Total Earnings:')
        pdf.cell(0, 10, f"${payslip_data['total_earnings']:.2f}", ln=True)
        pdf.cell(100, 10, 'Total Deductions:')
        pdf.cell(0, 10, f"${payslip_data['total_deductions']:.2f}", ln=True)
        pdf.cell(100, 10, 'Net Pay:')
        pdf.cell(0, 10, f"${payslip_data['net_pay']:.2f}", ln=True)

        # Footer Section
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 10)
        pdf.multi_cell(0, 10, f"{self.company_name}\n{self.company_address}\nID: {self.company_id}")

        # Save PDF
        pdf.output(output_file)


payslip_data = {
    'employee_name': 'Kristófer Orri Guðmundsson',
    'date': '31.12.2024',
    'period': '01.12.2024 - 31.12.2024',
    'payslip_number': '2',
    'national_id': '110703-2360',
    'department': 'Skrifstofa',
    'earnings': [
        {'description': 'Base Salary', 'amount': 500000},
        {'description': 'Vacation Pay (10.64%)', 'amount': 53200},
    ],
    'deductions': [
        {'description': 'Pension Contribution (4%)', 'amount': 22128},
        {'description': 'Union Fee (0.70%)', 'amount': 3872},
        {'description': 'Tax Withholding', 'amount': 107777},
    ],
    'total_earnings': 553200,
    'total_deductions': 133777,
    'net_pay': 419423,
}

generator = PayslipGenerator(
    company_name="V.M. ehf",
    company_address="Gilsbúð 5, 6504780539",
    company_id="6504780539"
)

# Generate the payslip
generator.generate_payslip(payslip_data, "payslip_kristofer.pdf")

