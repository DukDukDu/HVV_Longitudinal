import os

data_path = '/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/delpycondor/sample'

Lumi = 300  # fb^-1

sample_dict = {
    'gg2e2m_tot': 'mc.000.gg2e2m_tot.showersimul/',
    'gg2e2m_bkg': 'mc.001.gg2e2m_bkg.showersimul/',
    'gg2e2m_sig': 'mc.002.gg2e2m_sig.showersimul/',
    'gg4e_tot': 'mc.003.gg4e_tot.showersimul/',
    'gg4e_bkg': 'mc.004.gg4e_bkg.showersimul/',
    'gg4e_sig': 'mc.005.gg4e_sig.showersimul/',
    'gg4m_tot': 'mc.006.gg4m_tot.showersimul/',
    'gg4m_bkg': 'mc.007.gg4m_bkg.showersimul',
    'gg4m_sig': 'mc.008.gg4m_sig.showersimul',
}

id2proc_dict = {
    '000': 'gg2e2m_tot',
    '001': 'gg2e2m_bkg',
    '002': 'gg2e2m_sig',
    '003': 'gg4e_tot',
    '004': 'gg4e_bkg',
    '005': 'gg4e_sig',
    '006': 'gg4m_tot',
    '007': 'gg4m_bkg',
    '008': 'gg4m_sig',
}

xsec_dict = {
    'gg2e2m_tot': 1.668,
    'gg2e2m_bkg': 1.776,
    'gg2e2m_sig': 0.0956,
    'gg4e_tot': 0.8231,
    'gg4e_bkg': 0.8656,
    'gg4e_sig': 0.04811,
    'gg4m_tot': 0.8231,
    'gg4m_bkg': 0.8656,
    'gg4m_sig': 0.04811,
}

eff_dict = {
    'gg2e2m_tot': 1.0,
    'gg2e2m_bkg': 1.0,
    'gg2e2m_sig': 1.0,
    'gg4e_tot': 1.0,
    'gg4e_bkg': 1.0,
    'gg4e_sig': 1.0,
    'gg4m_tot': 1.0,
    'gg4m_bkg': 1.0,
    'gg4m_sig': 1.0,
}

kFactor_dict = {
    'gg2e2m_tot': 1.0,
    'gg2e2m_bkg': 1.0,
    'gg2e2m_sig': 1.0,
    'gg4e_tot': 1.0,
    'gg4e_bkg': 1.0,
    'gg4e_sig': 1.0,
    'gg4m_tot': 1.0,
    'gg4m_bkg': 1.0,
    'gg4m_sig': 1.0,
}

ntotal_dict = {
    'gg2e2m_tot': 1000.0,
    'gg2e2m_bkg': 1000.0,
    'gg2e2m_sig': 1000.0,
    'gg4e_tot': 1000.0,
    'gg4e_bkg': 1000.0,
    'gg4e_sig': 1000.0,
    'gg4m_tot': 1000.0,
    'gg4m_bkg': 1000.0,
    'gg4m_sig': 1000.0,
}
