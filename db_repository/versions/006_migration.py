from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
prescription = Table('prescription', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('medical_id', Integer),
    Column('name', String(length=512)),
    Column('reason', String(length=2000)),
    Column('dosage', String(length=128)),
    Column('schedule', String(length=512)),
    Column('admin', String(length=512)),
    Column('other', String(length=512)),
)

medical_form = Table('medical_form', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('vaccine', String(length=500)),
    Column('dtap', Date),
    Column('mump', Date),
    Column('polio', Date),
    Column('ckpox', Date),
    Column('meningitis', Date),
    Column('hib', Date),
    Column('pcv', Date),
    Column('tb', Date),
    Column('tbtest', Boolean),
    Column('hosp', Boolean),
    Column('surg', Boolean),
    Column('chro', Boolean),
    Column('bedw', Boolean),
    Column('recinj', Boolean),
    Column('asth', Boolean),
    Column('diab', Boolean),
    Column('seiz', Boolean),
    Column('dizz', Boolean),
    Column('chestpain', Boolean),
    Column('add', Boolean),
    Column('emodisorder', Boolean),
    Column('seenprof', Boolean),
    Column('other', Boolean),
    Column('explain', String(length=1024)),
    Column('swim', Boolean),
    Column('restrictions', String(length=1024)),
    Column('insu', Boolean),
    Column('insucomp', String(length=128)),
    Column('insupoli', String(length=128)),
    Column('insusubs', String(length=128)),
    Column('insuphon', String(length=128)),
    Column('sign', Boolean),
    Column('parents_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['prescription'].create()
    post_meta.tables['medical_form'].columns['add'].create()
    post_meta.tables['medical_form'].columns['asth'].create()
    post_meta.tables['medical_form'].columns['bedw'].create()
    post_meta.tables['medical_form'].columns['chestpain'].create()
    post_meta.tables['medical_form'].columns['chro'].create()
    post_meta.tables['medical_form'].columns['ckpox'].create()
    post_meta.tables['medical_form'].columns['diab'].create()
    post_meta.tables['medical_form'].columns['dizz'].create()
    post_meta.tables['medical_form'].columns['dtap'].create()
    post_meta.tables['medical_form'].columns['emodisorder'].create()
    post_meta.tables['medical_form'].columns['explain'].create()
    post_meta.tables['medical_form'].columns['hib'].create()
    post_meta.tables['medical_form'].columns['hosp'].create()
    post_meta.tables['medical_form'].columns['insu'].create()
    post_meta.tables['medical_form'].columns['insucomp'].create()
    post_meta.tables['medical_form'].columns['insuphon'].create()
    post_meta.tables['medical_form'].columns['insupoli'].create()
    post_meta.tables['medical_form'].columns['insusubs'].create()
    post_meta.tables['medical_form'].columns['meningitis'].create()
    post_meta.tables['medical_form'].columns['mump'].create()
    post_meta.tables['medical_form'].columns['other'].create()
    post_meta.tables['medical_form'].columns['parents_id'].create()
    post_meta.tables['medical_form'].columns['pcv'].create()
    post_meta.tables['medical_form'].columns['polio'].create()
    post_meta.tables['medical_form'].columns['recinj'].create()
    post_meta.tables['medical_form'].columns['restrictions'].create()
    post_meta.tables['medical_form'].columns['seenprof'].create()
    post_meta.tables['medical_form'].columns['seiz'].create()
    post_meta.tables['medical_form'].columns['sign'].create()
    post_meta.tables['medical_form'].columns['surg'].create()
    post_meta.tables['medical_form'].columns['swim'].create()
    post_meta.tables['medical_form'].columns['tb'].create()
    post_meta.tables['medical_form'].columns['tbtest'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['prescription'].drop()
    post_meta.tables['medical_form'].columns['add'].drop()
    post_meta.tables['medical_form'].columns['asth'].drop()
    post_meta.tables['medical_form'].columns['bedw'].drop()
    post_meta.tables['medical_form'].columns['chestpain'].drop()
    post_meta.tables['medical_form'].columns['chro'].drop()
    post_meta.tables['medical_form'].columns['ckpox'].drop()
    post_meta.tables['medical_form'].columns['diab'].drop()
    post_meta.tables['medical_form'].columns['dizz'].drop()
    post_meta.tables['medical_form'].columns['dtap'].drop()
    post_meta.tables['medical_form'].columns['emodisorder'].drop()
    post_meta.tables['medical_form'].columns['explain'].drop()
    post_meta.tables['medical_form'].columns['hib'].drop()
    post_meta.tables['medical_form'].columns['hosp'].drop()
    post_meta.tables['medical_form'].columns['insu'].drop()
    post_meta.tables['medical_form'].columns['insucomp'].drop()
    post_meta.tables['medical_form'].columns['insuphon'].drop()
    post_meta.tables['medical_form'].columns['insupoli'].drop()
    post_meta.tables['medical_form'].columns['insusubs'].drop()
    post_meta.tables['medical_form'].columns['meningitis'].drop()
    post_meta.tables['medical_form'].columns['mump'].drop()
    post_meta.tables['medical_form'].columns['other'].drop()
    post_meta.tables['medical_form'].columns['parents_id'].drop()
    post_meta.tables['medical_form'].columns['pcv'].drop()
    post_meta.tables['medical_form'].columns['polio'].drop()
    post_meta.tables['medical_form'].columns['recinj'].drop()
    post_meta.tables['medical_form'].columns['restrictions'].drop()
    post_meta.tables['medical_form'].columns['seenprof'].drop()
    post_meta.tables['medical_form'].columns['seiz'].drop()
    post_meta.tables['medical_form'].columns['sign'].drop()
    post_meta.tables['medical_form'].columns['surg'].drop()
    post_meta.tables['medical_form'].columns['swim'].drop()
    post_meta.tables['medical_form'].columns['tb'].drop()
    post_meta.tables['medical_form'].columns['tbtest'].drop()
