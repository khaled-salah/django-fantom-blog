url = 'http://13.64.66.156'
db = 'CrmSmaker2'
username = 'ahmednazmey@hotmail.com'
password = 'Admin.2o20'



################################
url2 = 'http://13.94.64.47/'
db2 = 'CrmSmaker'
username2 = 'admin'
password2 = 'Admin.2o20'

import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
companies = models.execute_kw(db, uid, password,
                              'crm.lead', 'search', [[]])

read_leads = models.execute_kw(db, uid, password,
                               'crm.lead', 'read',
                               [companies], {'fields':
        [
            'create_date',
            'date_deadline',
            'name',
            'partner_id',
            'email_from',
            'phone',
            'city',
            'state_id',
            'country_id',
            'activity_date_deadline',
            'campaign_id',
            'stage_id',
            'probability',
            'user_id',
            'team_id',
        ]})


models.execute_kw(db2, uid2, password2, 'crm.lead', 'create', [{
    'name': "Custom Model",
    'model': "x_custom_model",
    'state': 'manual',
}])

print(len(companies))
