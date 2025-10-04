from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io
import logging

_logger = logging.getLogger(__name__)

class SiapExport(models.Model):
    _name = 'siap.export'
    _description = 'SIAP Export'
    _order = 'create_date desc'

    export_type = fields.Selection([
        ('receivable', 'Accounts Receivable'),
        ('payable', 'Accounts Payable')
    ], required=True, string="Export Type")
    
    export_date = fields.Date(required=True, string="Export Date", default=fields.Date.context_today)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('exported', 'Exported'),
    ], default='draft', string='State')
    
    attachment_id = fields.Many2one('ir.attachment', string='Export File', readonly=True)
    
    def export_data(self):
        """Export data based on the selected type and date"""
        try:
            if self.export_type == 'receivable':
                partners = self._get_top_partners('customer')
            else:
                partners = self._get_top_partners('supplier')
            
            if not partners:
                raise UserError(_('No partners found for the selected criteria.'))
            
            txt_data = self._generate_txt(partners)
            attachment = self._create_export_file(txt_data)
            self.write({
                'state': 'exported',
                'attachment_id': attachment.id
            })
            
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }
        except Exception as e:
            _logger.error(f"Error during SIAP export: {str(e)}")
            raise UserError(_('Error during export: %s') % str(e))

    def _get_top_partners(self, partner_type):
        """Get top 20 partners based on type with improved performance"""
        Partner = self.env['res.partner']
        
        if partner_type == 'supplier':
            domain = [
                ('supplier_rank', '>', 0),
                ('is_company', '=', True)
            ]
        else:
            domain = [
                ('customer_rank', '>', 0),
                ('is_company', '=', True)
            ]
        
        # Get partners with invoice data for sorting by amount
        partners_with_amounts = []
        all_partners = Partner.search(domain)
        
        for partner in all_partners:
            total_amount = self._get_total_amount(partner)
            if total_amount > 0:
                partners_with_amounts.append((partner, total_amount))
        
        # Sort by amount (descending) and take top 20
        partners_with_amounts.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in partners_with_amounts[:20]]

    def _generate_txt(self, partners):
        """Generate SIAP-compliant TXT format"""
        output = io.StringIO()
        
        # Add header
        header = f"SIAP Export - {self.export_type.upper()} - {self.export_date}\n"
        output.write(header)
        output.write("-" * 80 + "\n")
        
        for i, partner in enumerate(partners, 1):
            total_amount = self._get_total_amount(partner)
            # SIAP format: Code|Name|Amount|Date
            line = f"{i:02d}|{partner.name[:50]}|{total_amount:.2f}|{self.export_date}\n"
            output.write(line)
            
        return output.getvalue()

    def _get_total_amount(self, partner):
        """Calculate total amount for partner with improved query performance"""
        AccountMove = self.env['account.move']
        
        base_domain = [
            ('partner_id', '=', partner.id),
            ('state', 'in', ['posted']),
            ('invoice_date', '<=', self.export_date)
        ]
        
        if self.export_type == 'receivable':
            domain = base_domain + [('move_type', 'in', ['out_invoice', 'out_refund'])]
        else:
            domain = base_domain + [('move_type', 'in', ['in_invoice', 'in_refund'])]
            
        invoices = AccountMove.search(domain)
        
        # Calculate amounts considering refunds
        total_amount = 0
        for invoice in invoices:
            if invoice.move_type in ['out_invoice', 'in_invoice']:
                total_amount += invoice.amount_total
            else:  # refunds
                total_amount -= invoice.amount_total
                
        return abs(total_amount)  # Return absolute value for SIAP reporting

    def _create_export_file(self, txt_data):
        """Create attachment with improved security and metadata"""
        file_name = f"siap_export_{self.export_type}_{self.export_date.strftime('%Y%m%d')}.txt"
        file_data = base64.b64encode(txt_data.encode('utf-8')).decode('ascii')
        
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_data,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'text/plain',
            'description': f'SIAP Export for {self.export_type} as of {self.export_date}',
        })
        
        _logger.info(f"SIAP export file created: {file_name} for {self.export_type}")
        return attachment