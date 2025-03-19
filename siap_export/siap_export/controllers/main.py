from odoo import http
from odoo.http import request
import base64
import io

class SiapExportController(http.Controller):

    @http.route('/siap/export', type='http', auth='user', methods=['POST'], csrf=False)
    def export_data(self, export_type, date):
        # Validate export_type
        if export_type not in ['receivable', 'payable']:
            return request.make_response("Invalid export type", status=400)

        # Fetch data based on export_type
        if export_type == 'receivable':
            partners = self._get_top_customers()
        else:
            partners = self._get_top_suppliers()

        # Generate TXT file content
        txt_content = self._generate_txt_file(partners, date)

        # Prepare response
        response = request.make_response(txt_content,
                                          headers={
                                              'Content-Type': 'text/plain',
                                              'Content-Disposition': 'attachment; filename="siap_export.txt"'
                                          })
        return response

    def _get_top_customers(self):
        # Logic to fetch top 20 customers based on total amount
        partners = request.env['res.partner'].search([
            ('customer_rank', '>', 0)
        ], limit=20)
        return partners

    def _get_top_suppliers(self):
        # Logic to fetch top 20 suppliers based on total amount
        partners = request.env['res.partner'].search([
            ('supplier_rank', '>', 0)
        ], limit=20)
        return partners

    def _generate_txt_file(self, partners, date):
        output = io.StringIO()
        output.write(f"Export Date: {date}\n")
        output.write("Partner Name\tTotal Amount\n")
        for partner in partners:
            total_amount = sum(invoice.amount_total for invoice in partner.invoice_ids)
            output.write(f"{partner.name}\t{total_amount}\n")
        return output.getvalue()