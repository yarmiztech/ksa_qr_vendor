# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions,api
import requests
import base64
import math
import json
import os
from odoo.exceptions import UserError


class ZatcaConfig(models.Model):
    _name = 'zatca.config'
    _rec_name = 'company_id'

    @api.model
    def create(self, vals_list):
        company_len = len(self.env['zatca.config'].search([('company_id.id', '=', vals_list['company_id'])]))
        if company_len > 0:
            raise UserError("Zatca details for this company already exist,delete the record to complete the process")
        res = super(ZatcaConfig, self).create(vals_list)
        return res

    company_id = fields.Many2one('res.company', required=1)
    link = fields.Char("Api Link", required="1", default="https://gw-apic-gov.gazt.gov.sa/e-invoicing/developer-portal")
    sdk_path = fields.Char()
    status = fields.Char(default='invoices\n')
    certificate_status = fields.Boolean()
    onboarding_status = fields.Boolean()
    on_board_status_details = fields.Char(default='{"error": "404"}')
    pih = fields.Char(
        default='NWZlY2ViNjZmZmM4NmYzOGQ5NTI3ODZjNmQ2OTZjNzljMmRiYzIzOWRkNGU5MWI0NjcyOWQ3M2EyN2ZiNTdlOQ==')

    common_name = fields.Char("Common Name", required="1",default="127.0.0.1")  # CN
    serial_number = fields.Char("EGS Serial Number", required="1",default="1-TST|2-TST|3-47f16c26-806b-4e15-b269-7a803884be9c")  # SN
    organization_identifier = fields.Char("Organization Identifier", required="1",default="300075588700003")  # UID
    organization_unit_name = fields.Char("Organization Unit Name", required="1",default="haya yaghmour")  # OU
    organization_name = fields.Char("Organization Name", required="1",default="agile")  # O
    country_name = fields.Char("Country Name", required="1",default="SA")  # C
    invoice_type = fields.Char("Invoice Type", required="1",default="1100")  # title
    location_address = fields.Char("Location", required="1",default="Zatca 12")  # registeredAddress
    industry_business_category = fields.Char("Industry", required="1",default="Food Bussiness3")  # BusinessCategory
    otp = fields.Char("Otp",default="123345")
    certificate = fields.Char("Certificate",default="MIID6jCCA5CgAwIBAgITbwAAfsboAdNVNKd+1wABAAB+xjAKBggqhkjOPQQDAjBjMRUwEwYKCZImiZPyLGQBGRYFbG9jYWwxEzARBgoJkiaJk/IsZAEZFgNnb3YxFzAVBgoJkiaJk/IsZAEZFgdleHRnYXp0MRwwGgYDVQQDExNUU1pFSU5WT0lDRS1TdWJDQS0xMB4XDTIyMDgxNjE0MjU0OFoXDTI0MDgxNTE0MjU0OFowTjELMAkGA1UEBhMCU0ExEzARBgNVBAoTCjMxMDIzMzM3NDYxDDAKBgNVBAsTA1RTVDEcMBoGA1UEAxMTVFNULTMxMDIzMzM3NDYwMDAwMzBWMBAGByqGSM49AgEGBSuBBAAKA0IABGGDDKDmhWAITDv7LXqLX2cmr6+qddUkpcLCvWs5rC2O29W/hS4ajAK4Qdnahym6MaijX75Cg3j4aao7ouYXJ9GjggI5MIICNTCBmgYDVR0RBIGSMIGPpIGMMIGJMTswOQYDVQQEDDIxLVRTVHwyLVRTVHwzLTBiZTk2ZTI3LWI5MTgtNDliYy05N2RiLTMzOWY1OWMyMzA0ZDEfMB0GCgmSJomT8ixkAQEMDzMxMDIzMzM3NDYwMDAwMzENMAsGA1UEDAwEMTEwMDEMMAoGA1UEGgwDVFNUMQwwCgYDVQQPDANUU1QwHQYDVR0OBBYEFDuWYlOzWpFN3no1WtyNktQdrA8JMB8GA1UdIwQYMBaAFHZgjPsGoKxnVzWdz5qspyuZNbUvME4GA1UdHwRHMEUwQ6BBoD+GPWh0dHA6Ly90c3RjcmwuemF0Y2EuZ292LnNhL0NlcnRFbnJvbGwvVFNaRUlOVk9JQ0UtU3ViQ0EtMS5jcmwwga0GCCsGAQUFBwEBBIGgMIGdMG4GCCsGAQUFBzABhmJodHRwOi8vdHN0Y3JsLnphdGNhLmdvdi5zYS9DZXJ0RW5yb2xsL1RTWkVpbnZvaWNlU0NBMS5leHRnYXp0Lmdvdi5sb2NhbF9UU1pFSU5WT0lDRS1TdWJDQS0xKDEpLmNydDArBggrBgEFBQcwAYYfaHR0cDovL3RzdGNybC56YXRjYS5nb3Yuc2Evb2NzcDAOBgNVHQ8BAf8EBAMCB4AwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMDMCcGCSsGAQQBgjcVCgQaMBgwCgYIKwYBBQUHAwIwCgYIKwYBBQUHAwMwCgYIKoZIzj0EAwIDSAAwRQIhAMWDOI67/kAqLSDMGeUDUettoh+1dRGNHppri9d7y02vAiAtfnOLHuJBlO8QqNxXOdeQZphNYai0DDzQXmESb+6FZA==")

    is_sandbox = fields.Boolean('Testing ?')
    private_key = fields.Char("Private key",default="MHQCAQEEIDyLDaWIn/1/g3PGLrwupV4nTiiLKM59UEqUch1vDfhpoAcGBSuBBAAKoUQDQgAEYYMMoOaFYAhMO/steotfZyavr6p11SSlwsK9azmsLY7b1b+FLhqMArhB2dqHKboxqKNfvkKDePhpqjui5hcn0Q==")
    cert_sig_algo = fields.Char()
    certificate_template_name = fields.Char(default='1.3.6.1.4.1.311.20.2')
    email_id = fields.Char(default='myEmail@gmail.com')

    xml_sequence = fields.Char(default='0')
    sb_bs_token = fields.Char('Sandbox Binary Security Token')
    sb_reqid = fields.Char('Sandbox Binary Request ID')
    sb_secret = fields.Char('Sandbox Binary Secret')
    reqid = fields.Char('Request ID')
    bs_token = fields.Char('Binary Security Token')
    secret = fields.Char('Secret')



    def generate_zatca_certificate(self):
        self.onboarding_status = None
        if not self.otp:
            raise exceptions.MissingError("OTP required")
        try:
            company = self.company_id.name.replace(" ", "")
            config_cnf = '''
                oid_section = OIDs
                [ OIDs ]
                certificateTemplateName= '''+ self.certificate_template_name +'''
                [ req ]
                default_bits = 2048
                emailAddress = '''+ self.email_id +'''
                req_extensions = v3_req
                x509_extensions = v3_ca
                prompt = no
                default_md = sha256
                req_extensions = req_ext
                distinguished_name = dn
                [ dn ]
                C = ''' + self.country_name + '''
                OU = ''' + self.organization_unit_name + '''
                O = ''' + self.organization_name + '''
                CN = ''' + self.common_name + '''
                [ v3_req ]
                basicConstraints = CA:FALSE
                keyUsage = digitalSignature, nonRepudiation, keyEncipherment
                [ req_ext ]
                certificateTemplateName = ASN1:PRINTABLESTRING:ZATCA-Code-Signing
                subjectAltName = dirName:alt_names            
                [ alt_names ]
                SN = ''' + self.serial_number + '''
                UID = ''' + self.organization_identifier + '''
                title = ''' + self.invoice_type + '''
                registeredAddress = ''' + self.location_address + '''
                businessCategory = ''' + self.industry_business_category + '''
            '''

            f = open('/tmp/enz_zatca_'+ company +'_zatca.cnf', 'w+')
            f.write(config_cnf)
            f.close()

            # Certiciate calculation moved to new function

            if self.is_sandbox:
                private_key = self.private_key
                if private_key.find('-----BEGIN EC PRIVATE KEY-----') > -1:
                    private_key = private_key.replace('-----BEGIN EC PRIVATE KEY-----', '') \
                        .replace('-----END EC PRIVATE KEY-----', '').replace(' ', '').replace('\n', '')
                for x in range(1, math.ceil(len(private_key) / 64)):
                    private_key = private_key[:64 * x + x -1] + '\n' + private_key[64 * x + x -1:]
                private_key = "-----BEGIN EC PRIVATE KEY-----\n" + private_key + "\n-----END EC PRIVATE KEY-----"

                f = open('/tmp/enz_zatca_'+ company +'_privatekey.pem', 'w+')
                f.write(private_key)
                f.close()
            else:
                private_key = 'openssl ecparam -name secp256k1 -genkey -noout -out /tmp/enz_zatca_'+ company +'_privatekey.pem'
            public_key = 'openssl ec -in /tmp/enz_zatca_'+ company +'_privatekey.pem -pubout -conv_form compressed -out /tmp/enz_zatca_'+ company +'_publickey.pem'
            public_key_bin = 'openssl base64 -d -in /tmp/enz_zatca_'+ company +'_publickey.pem -out /tmp/enz_zatca_'+ company +'_publickey.bin'
            csr = 'openssl req -new -sha256 -key /tmp/enz_zatca_'+ company +'_privatekey.pem -extensions v3_req -config /tmp/enz_zatca_'+ company +'_zatca.cnf -out /tmp/enz_zatca_'+ company +'_taxpayper.csr'
            csr_base64 = "openssl base64 -in /tmp/enz_zatca_"+ company +"_taxpayper.csr -out /tmp/enz_zatca_"+ company +"_taxpayper_64.csr"
            if not self.is_sandbox:
                os.system(private_key)
            os.system(public_key)
            os.system(public_key_bin)
            os.system(csr)
            os.system(csr_base64)
            self.status = 'Certificate, private & public key generated'
            csr_invoice_type = self.invoice_type

            qty = 3
            if csr_invoice_type == '1100':
                zatca_on_board_status_details = {
                    'standard': {
                        'credit': 0,
                        'debit': 0,
                        'invoice': 0,
                    },
                    'simplified': {
                        'credit': 0,
                        'debit': 0,
                        'invoice': 0,
                    }
                }
                message = "Standard & its associated invoices and Simplified & its associated invoices"
                message = "Standard: invoice, debit, credit, \nSimplified: invoice, debit, credit, "
                qty = 6
            elif csr_invoice_type == '1000':
                zatca_on_board_status_details = {
                    'standard': {
                        'credit': 0,
                        'debit': 0,
                        'invoice': 0,
                    }
                }
                message = "Standard & its associated invoices"
                message = "Standard: invoice, debit, credit, "
            elif csr_invoice_type == '0100':
                zatca_on_board_status_details = {
                    'simplified': {
                        'credit': 0,
                        'debit': 0,
                        'invoice': 0,
                    }
                }
                message = "Simplified & its associated invoices"
                message = "Simplified: invoice, debit, credit, "
            self.on_board_status_details = json.dumps(zatca_on_board_status_details)
            self.status = 'Onboarding started, required ' + str(qty) + ' invoices' + "\n" + message

            # filepath = os.popen("find -name 'zatca_sdk'").read()
            # filepath = filepath.replace('zatca_sdk', '').replace('\n', '')
            # self.env['ir.config_parameter'].sudo().set_param("zatca_sdk_path", filepath)

        except Exception as e:
            # raise exceptions.MissingError(e)
            raise exceptions.MissingError('Server Error, Contact administrator.')
        self.compliance_api()
        self.otp = None
        # self.compliance_api('/production/csids', 1)
        #     CNF, PEM, CSR created

    def compliance_api(self, endpoint='/compliance', renew=0):
        company = self.company_id.name.replace(" ", "")
        link = self.link
        if endpoint == '/compliance':
            zatca_otp = self.otp
            headers = {'accept': 'application/json',
                       'OTP': zatca_otp,
                       'Accept-Version': 'V2',
                       'Content-Type': 'application/json'}

            f = open('/tmp/enz_zatca_'+ company +'_taxpayper_64.csr', 'r')
            csr = f.read()
            data = {'csr': csr.replace('\n', '')}
        elif endpoint == '/production/csids' and not renew:
            user = self.sb_bs_token
            password = self.sb_secret
            compliance_request_id = self.sb_reqid
            auth = base64.b64encode(('%s:%s' % (user, password)).encode('utf-8')).decode('utf-8')
            headers = {'accept': 'application/json',
                       'Accept-Version': 'V2',
                       'Authorization': 'Basic ' + auth,
                       'Content-Type': 'application/json'}

            data = {'compliance_request_id': compliance_request_id}
        elif endpoint == '/production/csids' and renew:
            user = self.bs_token
            password = self.secret
            auth = base64.b64encode(('%s:%s' % (user, password)).encode('utf-8')).decode('utf-8')
            zatca_otp = self.otp
            headers = {'accept': 'application/json',
                       'OTP': zatca_otp,
                       'Accept-Language': 'en',
                       'Accept-Version': 'V2',
                       'Authorization': 'Basic ' + auth,
                       'Content-Type': 'application/json'}
            f = open('/tmp/enz_zatca_'+ company +'_taxpayper_64.csr', 'r')
            csr = f.read()
            data = {'csr': csr.replace('\n', '')}
        try:
            req = requests.post(link + endpoint, headers=headers, data=json.dumps(data))
            if req.status_code == 500:
                if req.text:
                    response = json.loads(req.text)
                    raise exceptions.AccessError(response['message'])
                raise exceptions.AccessError('Invalid Request, zatca, \ncontact system administer')
            elif req.status_code == 400:
                if req.text:
                    response = json.loads(req.text)
                    raise exceptions.AccessError(response['message'])
                raise exceptions.AccessError('Invalid Request, odoo, \ncontact system administer')
            elif req.status_code == 401:
                if req.text:
                    response = json.loads(req.text)
                    raise exceptions.AccessError(response['message'])
                raise exceptions.AccessError('Unauthorized, \ncontact system administer')
            elif req.status_code == 200:
                response = json.loads(req.text)
                if endpoint == '/compliance':
                    self.sb_bs_token = response['binarySecurityToken']
                    self.sb_reqid = response['requestID']
                    self.sb_secret = response['secret']
                else:
                    self.bs_token = response['binarySecurityToken']
                    self.reqid = response['requestID']
                    self.secret = response['secret']
                # if endpoint == '/compliance':
                #     self.compliance_api('/production/csids')
                # else:
                #     response['tokenType']
                #     response['dispositionMessage']
        except Exception as e:
            raise exceptions.AccessDenied(e)

    def production_credentials(self):
        company = self.company_id.name.replace(" ", "")
        if self.certificate_status != "1":
            raise exceptions.MissingError("Register Certificate before proceeding.")
        if self.is_sandbox:
            zatca_bsToken = "TUlJRDFEQ0NBM21nQXdJQkFnSVRid0FBZTNVQVlWVTM0SS8rNVFBQkFBQjdkVEFLQmdncWhrak9QUVFEQWpCak1SVXdFd1lLQ1pJbWlaUHlMR1FCR1JZRmJHOWpZV3d4RXpBUkJnb0praWFKay9Jc1pBRVpGZ05uYjNZeEZ6QVZCZ29Ka2lhSmsvSXNaQUVaRmdkbGVIUm5ZWHAwTVJ3d0dnWURWUVFERXhOVVUxcEZTVTVXVDBsRFJTMVRkV0pEUVMweE1CNFhEVEl5TURZeE1qRTNOREExTWxvWERUSTBNRFl4TVRFM05EQTFNbG93U1RFTE1Ba0dBMVVFQmhNQ1UwRXhEakFNQmdOVkJBb1RCV0ZuYVd4bE1SWXdGQVlEVlFRTEV3MW9ZWGxoSUhsaFoyaHRiM1Z5TVJJd0VBWURWUVFERXdreE1qY3VNQzR3TGpFd1ZqQVFCZ2NxaGtqT1BRSUJCZ1VyZ1FRQUNnTkNBQVRUQUs5bHJUVmtvOXJrcTZaWWNjOUhEUlpQNGI5UzR6QTRLbTdZWEorc25UVmhMa3pVMEhzbVNYOVVuOGpEaFJUT0hES2FmdDhDL3V1VVk5MzR2dU1ObzRJQ0p6Q0NBaU13Z1lnR0ExVWRFUVNCZ0RCK3BId3dlakViTUJrR0ExVUVCQXdTTVMxb1lYbGhmREl0TWpNMGZETXRNVEV5TVI4d0hRWUtDWkltaVpQeUxHUUJBUXdQTXpBd01EYzFOVGc0TnpBd01EQXpNUTB3Q3dZRFZRUU1EQVF4TVRBd01SRXdEd1lEVlFRYURBaGFZWFJqWVNBeE1qRVlNQllHQTFVRUR3d1BSbTl2WkNCQ2RYTnphVzVsYzNNek1CMEdBMVVkRGdRV0JCU2dtSVdENmJQZmJiS2ttVHdPSlJYdkliSDlIakFmQmdOVkhTTUVHREFXZ0JSMllJejdCcUNzWjFjMW5jK2FyS2NybVRXMUx6Qk9CZ05WSFI4RVJ6QkZNRU9nUWFBL2hqMW9kSFJ3T2k4dmRITjBZM0pzTG5waGRHTmhMbWR2ZGk1ellTOURaWEowUlc1eWIyeHNMMVJUV2tWSlRsWlBTVU5GTFZOMVlrTkJMVEV1WTNKc01JR3RCZ2dyQmdFRkJRY0JBUVNCb0RDQm5UQnVCZ2dyQmdFRkJRY3dBWVppYUhSMGNEb3ZMM1J6ZEdOeWJDNTZZWFJqWVM1bmIzWXVjMkV2UTJWeWRFVnVjbTlzYkM5VVUxcEZhVzUyYjJsalpWTkRRVEV1WlhoMFoyRjZkQzVuYjNZdWJHOWpZV3hmVkZOYVJVbE9WazlKUTBVdFUzVmlRMEV0TVNneEtTNWpjblF3S3dZSUt3WUJCUVVITUFHR0gyaDBkSEE2THk5MGMzUmpjbXd1ZW1GMFkyRXVaMjkyTG5OaEwyOWpjM0F3RGdZRFZSMFBBUUgvQkFRREFnZUFNQjBHQTFVZEpRUVdNQlFHQ0NzR0FRVUZCd01DQmdnckJnRUZCUWNEQXpBbkJna3JCZ0VFQVlJM0ZRb0VHakFZTUFvR0NDc0dBUVVGQndNQ01Bb0dDQ3NHQVFVRkJ3TURNQW9HQ0NxR1NNNDlCQU1DQTBrQU1FWUNJUUNWd0RNY3E2UE8rTWNtc0JYVXovdjFHZGhHcDdycVNhMkF4VEtTdjgzOElBSWhBT0JOREJ0OSszRFNsaWpvVmZ4enJkRGg1MjhXQzM3c21FZG9HV1ZyU3BHMQ=="
            zatca_secret = "Xlj15LyMCgSC66ObnEO/qVPfhSbs3kDTjWnGheYhfSs="
            self.bs_token = zatca_bsToken
            self.reqid = 'N/A'
            self.secret = zatca_secret
        else:
            self.compliance_api('/production/csids', 0)
        self.status = 'production credentials received.'
        self.otp = None

    def production_credentials_renew(self):
        company = self.company_id.name.replace(" ", "")
        if self.certificate_status != "1":
            raise exceptions.MissingError("Register Certificate before proceeding.")
        if not self.otp:
            raise exceptions.MissingError("OTP required")
        if self.is_sandbox:
            zatca_bsToken = "TUlJRDFEQ0NBM21nQXdJQkFnSVRid0FBZTNVQVlWVTM0SS8rNVFBQkFBQjdkVEFLQmdncWhrak9QUVFEQWpCak1SVXdFd1lLQ1pJbWlaUHlMR1FCR1JZRmJHOWpZV3d4RXpBUkJnb0praWFKay9Jc1pBRVpGZ05uYjNZeEZ6QVZCZ29Ka2lhSmsvSXNaQUVaRmdkbGVIUm5ZWHAwTVJ3d0dnWURWUVFERXhOVVUxcEZTVTVXVDBsRFJTMVRkV0pEUVMweE1CNFhEVEl5TURZeE1qRTNOREExTWxvWERUSTBNRFl4TVRFM05EQTFNbG93U1RFTE1Ba0dBMVVFQmhNQ1UwRXhEakFNQmdOVkJBb1RCV0ZuYVd4bE1SWXdGQVlEVlFRTEV3MW9ZWGxoSUhsaFoyaHRiM1Z5TVJJd0VBWURWUVFERXdreE1qY3VNQzR3TGpFd1ZqQVFCZ2NxaGtqT1BRSUJCZ1VyZ1FRQUNnTkNBQVRUQUs5bHJUVmtvOXJrcTZaWWNjOUhEUlpQNGI5UzR6QTRLbTdZWEorc25UVmhMa3pVMEhzbVNYOVVuOGpEaFJUT0hES2FmdDhDL3V1VVk5MzR2dU1ObzRJQ0p6Q0NBaU13Z1lnR0ExVWRFUVNCZ0RCK3BId3dlakViTUJrR0ExVUVCQXdTTVMxb1lYbGhmREl0TWpNMGZETXRNVEV5TVI4d0hRWUtDWkltaVpQeUxHUUJBUXdQTXpBd01EYzFOVGc0TnpBd01EQXpNUTB3Q3dZRFZRUU1EQVF4TVRBd01SRXdEd1lEVlFRYURBaGFZWFJqWVNBeE1qRVlNQllHQTFVRUR3d1BSbTl2WkNCQ2RYTnphVzVsYzNNek1CMEdBMVVkRGdRV0JCU2dtSVdENmJQZmJiS2ttVHdPSlJYdkliSDlIakFmQmdOVkhTTUVHREFXZ0JSMllJejdCcUNzWjFjMW5jK2FyS2NybVRXMUx6Qk9CZ05WSFI4RVJ6QkZNRU9nUWFBL2hqMW9kSFJ3T2k4dmRITjBZM0pzTG5waGRHTmhMbWR2ZGk1ellTOURaWEowUlc1eWIyeHNMMVJUV2tWSlRsWlBTVU5GTFZOMVlrTkJMVEV1WTNKc01JR3RCZ2dyQmdFRkJRY0JBUVNCb0RDQm5UQnVCZ2dyQmdFRkJRY3dBWVppYUhSMGNEb3ZMM1J6ZEdOeWJDNTZZWFJqWVM1bmIzWXVjMkV2UTJWeWRFVnVjbTlzYkM5VVUxcEZhVzUyYjJsalpWTkRRVEV1WlhoMFoyRjZkQzVuYjNZdWJHOWpZV3hmVkZOYVJVbE9WazlKUTBVdFUzVmlRMEV0TVNneEtTNWpjblF3S3dZSUt3WUJCUVVITUFHR0gyaDBkSEE2THk5MGMzUmpjbXd1ZW1GMFkyRXVaMjkyTG5OaEwyOWpjM0F3RGdZRFZSMFBBUUgvQkFRREFnZUFNQjBHQTFVZEpRUVdNQlFHQ0NzR0FRVUZCd01DQmdnckJnRUZCUWNEQXpBbkJna3JCZ0VFQVlJM0ZRb0VHakFZTUFvR0NDc0dBUVVGQndNQ01Bb0dDQ3NHQVFVRkJ3TURNQW9HQ0NxR1NNNDlCQU1DQTBrQU1FWUNJUUNWd0RNY3E2UE8rTWNtc0JYVXovdjFHZGhHcDdycVNhMkF4VEtTdjgzOElBSWhBT0JOREJ0OSszRFNsaWpvVmZ4enJkRGg1MjhXQzM3c21FZG9HV1ZyU3BHMQ=="
            zatca_secret = "Xlj15LyMCgSC66ObnEO/qVPfhSbs3kDTjWnGheYhfSs="
            self.bs_token = zatca_bsToken
            self.reqid = 'N/A'
            self.secret = zatca_secret
        else:
            self.compliance_api('/production/csids', 1)
        self.status = 'production credentials renewed.'
        self.otp = None

    def register_certificate(self):
        company = self.company_id.name.replace(" ", "")
        certificate = self.certificate
        if certificate.find('-----BEGIN CERTIFICATE-----') > -1:
            certificate = certificate.replace('-----BEGIN CERTIFICATE-----', '') \
                .replace('-----END CERTIFICATE-----', '').replace(' ', '').replace('\n', '')
        for x in range(1, math.ceil(len(certificate) / 64)):
            certificate = certificate[:64 * x + x - 1] + '\n' + certificate[64 * x + x - 1:]
        certificate = "-----BEGIN CERTIFICATE-----\n" + certificate + "\n-----END CERTIFICATE-----"

        f = open('/tmp/enz_zatca_'+ company +'_cert.pem', 'w+')
        f.write(certificate)
        f.close()

        certificate_public_key = "openssl x509 -pubkey -noout -in /tmp/enz_zatca_"+ company +"_cert.pem -out /tmp/enz_zatca_"+ company +"_cert_publickey.pem"
        certificate_public_key_bin = "openssl base64 -d -in /tmp/enz_zatca_"+ company +"_cert_publickey.pem -out /tmp/enz_zatca_"+ company +"_cert_publickey.bin"
        certificate_signature_algorithm = "openssl x509 -in /tmp/enz_zatca_"+ company +"_cert.pem -text -noout"
        cert = os.popen(certificate_signature_algorithm).read()
        cert_find = cert.rfind("Signature Algorithm: ecdsa-with-SHA256")
        if cert_find > 0 and cert_find + 38 < len(cert):
            cert_sig_algo = cert[cert.rfind("Signature Algorithm: ecdsa-with-SHA256") + 38:].replace('\n', '') \
                .replace(':', '') \
                .replace(' ', '')
            self.cert_sig_algo = cert_sig_algo
        else:
            raise exceptions.ValidationError("Invalid Certificate Provided.")

        os.system(certificate_public_key)
        os.system(certificate_public_key_bin)
        self.certificate_status = 1
