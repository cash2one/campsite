from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
prescription = Table('prescription', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('medical_id', INTEGER),
    Column('name', VARCHAR(length=512)),
    Column('reason', VARCHAR(length=2000)),
    Column('dosage', VARCHAR(length=128)),
    Column('schedule', VARCHAR(length=512)),
    Column('admin', VARCHAR(length=512)),
    Column('other', VARCHAR(length=512)),
)

medication = Table('medication', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('medical_id', Integer),
    Column('name', String(length=512)),
    Column('reason', String(length=2000)),
    Column('dosage', String(length=128)),
    Column('schedule', String(length=512)),
    Column('admin', String(length=512)),
    Column('other', String(length=512)),
)

medical_form = Table('medical_form', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('add', BOOLEAN),
    Column('asth', BOOLEAN),
    Column('bedw', BOOLEAN),
    Column('chestpain', BOOLEAN),
    Column('chro', BOOLEAN),
    Column('ckpox', DATE),
    Column('diab', BOOLEAN),
    Column('dizz', BOOLEAN),
    Column('dtap', DATE),
    Column('emodisorder', BOOLEAN),
    Column('explain', VARCHAR(length=1024)),
    Column('hib', DATE),
    Column('hosp', BOOLEAN),
    Column('insu', BOOLEAN),
    Column('insucomp', VARCHAR(length=128)),
    Column('insuphon', VARCHAR(length=128)),
    Column('insupoli', VARCHAR(length=128)),
    Column('insusubs', VARCHAR(length=128)),
    Column('meningitis', DATE),
    Column('mump', DATE),
    Column('other', BOOLEAN),
    Column('parents_id', INTEGER),
    Column('pcv', DATE),
    Column('polio', DATE),
    Column('recinj', BOOLEAN),
    Column('restrictions', VARCHAR(length=1024)),
    Column('seenprof', BOOLEAN),
    Column('seiz', BOOLEAN),
    Column('sign', BOOLEAN),
    Column('surg', BOOLEAN),
    Column('swim', BOOLEAN),
    Column('tb', DATE),
    Column('tbtest', BOOLEAN),
    Column('allergies', VARCHAR(length=1024)),
)

medical_form = Table('medical_form', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('allergies', String(length=1024)),
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
    Column('envallg', Boolean),
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
    Column('parent', String(length=128)),
    Column('submission_timestamp', TIMESTAMP),
    Column('camper_registration_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['prescription'].drop()
    post_meta.tables['medication'].create()
    pre_meta.tables['medical_form'].columns['parents_id'].drop()
    post_meta.tables['medical_form'].columns['camper_registration_id'].create()
    post_meta.tables['medical_form'].columns['envallg'].create()
    post_meta.tables['medical_form'].columns['parent'].create()
    post_meta.tables['medical_form'].columns['submission_timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['prescription'].create()
    post_meta.tables['medication'].drop()
    pre_meta.tables['medical_form'].columns['parents_id'].create()
    post_meta.tables['medical_form'].columns['camper_registration_id'].drop()
    post_meta.tables['medical_form'].columns['envallg'].drop()
    post_meta.tables['medical_form'].columns['parent'].drop()
    post_meta.tables['medical_form'].columns['submission_timestamp'].drop()
