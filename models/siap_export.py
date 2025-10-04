from odoo import models, fields, api
import base64
import io

class SiapExport(models.Model):
    _name = 'siap.export'
    _description = 'SIAP Export'

    export_type = fields.Selection([
        ('receivable', 'Accounts Receivable'),
        ('payable', 'Accounts Payable')
    ], required=True, string="Export Type")
    
    export_date = fields.Date(required=True, string="Export Date")
    
    def export_data(self):
        if self.export_type == 'receivable':
            partners = self._get_top_partners('customer')
        else:
            partners = self._get_top_partners('supplier')
        
        txt_data = self._generate_txt(partners)
        self._create_export_file(txt_data)

    def _get_top_partners(self, partner_type):
        Partner = self.env['res.partner']
        domain = [('supplier_rank', '>', 0)] if partner_type == 'supplier' else [('customer_rank', '>', 0)]
        partners = Partner.search(domain, limit=20)
        return partners

    def _generate_txt(self, partners):
        output = io.StringIO()
        for partner in partners:
            total_amount = self._get_total_amount(partner)
            output.write(f"{partner.name}\t{total_amount}\n")
        return output.getvalue()

    def _get_total_amount(self, partner):
        if self.export_type == 'receivable':
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'out_invoice'),
                ('state', 'in', ['posted', 'paid']),
                ('invoice_date', '<=', self.export_date)
            ])
        else:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', '=', 'in_invoice'),
                ('state', 'in', ['posted', 'paid']),
                ('invoice_date', '<=', self.export_date)
            ])
        return sum(invoices.mapped('amount_total'))

    def _create_export_file(self, txt_data):
        file_name = f"siap_export_{self.export_date}.txt"
        file_data = base64.b64encode(txt_data.encode()).decode()
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_data,
            'store_fname': file_name,
            'res_model': 'siap.export',
            'res_id': self.id,
        })
        return attachment