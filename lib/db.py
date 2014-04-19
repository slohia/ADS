######################################################################################
## Copyright (C) Georgia Institute of Technology. All Rights Reserved.
## Name         : db.py
## Description  : module to provide interfaces for database operations
## Author       : Manish Choudhary
## Start Date   : 15 MAR 2014
## Last Revised :
######################################################################################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import datetime
Base = declarative_base()


class Network(Base):

    __tablename__ = 'network'
    id = Column(Integer, primary_key=True)
    vm_id = Column(String(100))
    latency = Column(Integer)
    throughput = Column(Integer)
    packet_loss = Column(Integer)
    open_ports = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())

    def __init__(self, vm_id, latency, throughput, packet_loss, open_ports, timestamp):
        self.vm_id = vm_id
        self.latency = latency
        self.throughput = throughput
        self.packet_loss = packet_loss
        self.open_ports = open_ports
        self.timestamp = timestamp

    def __repr__(self):
        return "<Network(%s, %s, %s, %s, %s, %s)>" % (self.vm_id, str(self.latency), str(self.throughput), str(self.packet_loss), str(self.open_ports), str(self.timestamp))


class CPU(Base):

    __tablename__ = 'cpu'
    id = Column(Integer, primary_key=True)
    vm_id = Column(String(100))
    processes = Column(Integer)
    system_time = Column(Integer)
    user_time = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vm_id, processes, system_time, user_time, timestamp):
        self.vm_id = vm_id
        self.processes = processes
        self.system_time = system_time
        self.user_time = user_time
        self.timestamp = timestamp

    def __repr__(self):
        return "<CPU(%s, %s, %s, %s, %s)>" % (self.vm_id, str(self.processes), str(self.system_time), str(self.user_time), str(self.timestamp))


class Memory(Base):

    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True)
    vm_id = Column(String(100))
    utilization = Column(Integer)
    page_faults = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vm_id, utilization, page_faults,timestamp):
        self.vm_id = vm_id
        self.utilization = utilization
        self.page_faults = page_faults
        self.timestamp = timestamp

    def __repr__(self):
        return "<Memory(%s, %s, %s, %s)>" % (self.vm_id, str(self.utilization), str(self.page_faults), str(self.timestamp))


class Disk(Base):

    __tablename__ = 'disk'
    id = Column(Integer, primary_key=True)
    vm_id = Column(String(100))
    cache_read_bytes_rate = Column(Integer)
    buffer_read_bytes_rate = Column(Integer)
    write_bytes_rate = Column(Integer)
    total_files = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vm_id, cache_read_bytes_rate, buffer_read_bytes_rate, write_bytes_rate, total_files, timestamp):
        self.vm_id = vm_id
        self.cache_read_bytes_rate = cache_read_bytes_rate
        self.buffer_read_bytes_rate = buffer_read_bytes_rate
        self.write_bytes_rate = write_bytes_rate
        self.total_files = total_files
        self.timestamp = timestamp

    def __repr__(self):
        return "<Disk(%s, %s, %s, %s, %s, %s)>" % (self.vm_id, str(self.cache_read_bytes_rate), str(self.buffer_read_bytes_rate), str(self.write_bytes_rate), str(self.total_files), str(self.timestamp))


class Clients(Base):

    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    vm_name = Column(String(100))
    vm_id = Column(String(100))
    vm_ip = Column(String(100))
    initial_vm_ip = Column(String(100))
    initial_vm_name = Column(String(100))
    primary_server = Column(String(100))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vm_name, vm_id, vm_ip, initial_vm_ip, initial_vm_name, primary_server, timestamp):
        self.vm_name = vm_name
        self.vm_id = vm_id
        self.vm_ip = vm_ip
        self.initial_vm_ip = initial_vm_ip
        self.initial_vm_name = initial_vm_name
        self.primary_server = primary_server
        self.timestamp = timestamp

    def __repr__(self):
        return "<Clients(%s, %s, %s, %s, %s, %s, %s)>" % (self.vm_name, str(self.vm_id), self.vm_ip, str(self.initial_vm_ip), str(self.initial_vm_name), str(self.primary_server), str(self.timestamp))


class DB:

    def __init__(self, ads):
        self.log = ads.log
        self.config = ads.config
        self.anomaly_detection_period = self.config.usr_env['anomaly_detection_period']

    def connect_db(self, db_type='mysql', user_name='root', password='root', db_server='localhost', db_name='ads'):
        try:
            self.log.log_msg("Request to connect to the database with following arguments.")
            self.log.log_msg("db_type : %s" % db_type)
            self.log.log_msg("user_name : %s" % user_name)
            #self.log.log_msg("password : %s" % password)
            self.log.log_msg("db_server : %s" % db_server)
            self.log.log_msg("db_name : %s" % db_name)
            engine = create_engine('%s://%s:%s@%s/%s' %(db_type, user_name, password, db_server, db_name), echo=False)
            Session = sessionmaker()
            Session.configure(bind=engine)
            self.log.log_msg("Engine Creation, Session Making and Engine Binding completed successfully")
            return Session()
        except Exception, e:
            self.log.log_msg("Exception in the function connect_db: %s" % str(e))

    def connect_and_generate_db(self, db_type='mysql', user_name='root', password='root', db_server='localhost', db_name='ads'):
        try:
            self.log.log_msg("Request to connect and create the database with following arguments.")
            self.log.log_msg("db_type : %s" % db_type)
            self.log.log_msg("user_name : %s" % user_name)
            self.log.log_msg("password : %s" % password)
            self.log.log_msg("db_server : %s" % db_server)
            self.log.log_msg("db_name : %s" % db_name)
            engine = create_engine('%s://%s:%s@%s/%s' %(db_type, user_name, password, db_server, db_name), echo=False)
            Session = sessionmaker()
            Session.configure(bind=engine)
            self.log.log_msg("Engine Creation, Session Making and Engine Binding completed successfully")
            Base.metadata.create_all(engine)
            self.log.log_msg("The database tables have been created")
            return Session()
        except Exception, e:
            self.log.log_msg("Exception in the function connect_and_generate_db: %s" % str(e))

    def insert_db(self, session, table_name, client_dict, param_dict=[]):
        self.log.log_msg("Request to insert in the database.")
        new_record = None
        print client_dict
        try:
            if len(param_dict) == 4:
                self.log.log_msg("The number of targeted columns is 6")
                if table_name == 'network':
                    self.log.log_msg("The insert request is for the database table 'network'")
                    new_record = Network(vm_id=client_dict['vm_id'], latency=param_dict['latency'], throughput=param_dict['throughput'], packet_loss=param_dict['packet_loss'], open_ports=param_dict['open_ports'], timestamp=datetime.datetime.utcnow())
            if len(param_dict) == 5:
                if table_name == 'disk':
                    self.log.log_msg("The insert request is for the database table 'disk'")
                    new_record = Disk(vm_id=client_dict['vm_id'], cache_read_bytes_rate=param_dict['cache_read_bytes_rate'], buffer_read_bytes_rate=param_dict['buffer_read_bytes_rate'], write_bytes_rate=param_dict['write_bytes_rate'], total_files=param_dict['total_files'], timestamp=datetime.datetime.utcnow())
            if len(param_dict) == 3:
                if table_name == 'cpu':
                    self.log.log_msg("The insert request is for the database table 'cpu'")
                    new_record = CPU(vm_id=client_dict['vm_id'], processes=param_dict['processes'], system_time=param_dict['system_time'], user_time=param_dict['user_time'], timestamp=datetime.datetime.utcnow())
            if len(param_dict) == 2:
                if table_name == 'memory':
                    self.log.log_msg("The insert request is for the database table 'memory'")
                    new_record = Memory(vm_id=client_dict['vm_id'], utilization=param_dict['utilization'], page_faults=param_dict['page_faults'], timestamp=datetime.datetime.utcnow())
            if table_name == 'clients':
                    self.log.log_msg("The insert request is for the database table 'clients'")
                    new_record = Clients(vm_name=client_dict['vm_name'], vm_id=client_dict['vm_id'], vm_ip=client_dict['vm_ip'], initial_vm_ip=client_dict['vm_ip'], initial_vm_name=client_dict['vm_name'], primary_server=client_dict['primary_server'], timestamp=datetime.datetime.utcnow())
            if new_record is None:
                print param_dict, len(param_dict)
                self.log.log_msg("Wrong Arguments passed.")
                return
            else:
                session.add(new_record)
                self.log.log_msg("New record has been added.")

        except Exception, e:
            self.log.log_msg("Exception in insert_db(): %s" % str(e))

    def commit_transaction(self, session):
        try:
            session.commit()
            self.log.log_msg("The data has been committed successfully to the database")
        except Exception, e:
            session.rollback()
            self.log.log_msg("Exception in commit_transaction(): %s" % str(e))

    def fetch_db(self, session, vm_id_arg, table_name_arg):
        try:
            self.log.log_msg("Request to fetch data from table %s for vm %s" % (table_name_arg, vm_id_arg))
            current_time = datetime.datetime.utcnow()
            fetch_for_period = datetime.timedelta(minutes=self.anomaly_detection_period)
            time_to_check = current_time - fetch_for_period
            print time_to_check
            if table_name_arg == 'network':
                fetched_result = session.query(Network).filter(Network.vm_id == vm_id_arg).filter(Network.timestamp>time_to_check)
            elif table_name_arg == 'cpu':
                fetched_result = session.query(CPU).filter(CPU.vm_id == vm_id_arg).filter(CPU.timestamp>time_to_check)
            elif table_name_arg == 'memory':
                fetched_result = session.query(Memory).filter(Memory.vm_id == vm_id_arg).filter(Memory.timestamp>time_to_check)
            elif table_name_arg == 'disk':
                fetched_result = session.query(Disk).filter(Disk.vm_id == vm_id_arg).filter(Disk.timestamp>time_to_check)
            elif table_name_arg == 'clients':
                fetched_result = session.query(Clients).filter(Clients.vm_id == vm_id_arg).filter(Clients.timestamp>time_to_check)
            else:
                self.log.log_msg("Wrong table name passed.")
                return False
            if fetched_result:
                return fetched_result.all()
        except Exception, e:
            self.log.log_msg("Exception in fetch_db(): %s" % str(e))

    def fetch_vm_ids_from_db(self, session):
        try:
            fetched_result = session.query(Clients.vm_id)
            return fetched_result.all()
        except Exception, e:
            self.log.log_msg("Exception in fetch_vm_ids_from_db() %s" % str(e))

    def update_client_info(self, session, client_dict):
        try:
            fetched_result = session.query(Clients).filter(Clients.vm_id == client_dict['vm_id']).first()
            if fetched_result:
                fetched_result.vm_ip = client_dict['vm_ip']
                fetched_result.vm_name = client_dict['vm_name']
                return True
            else:
                return False
        except Exception, e:
            self.log.log_msg("Exception in fetch_vm_ids_from_db() %s" % str(e))

    def disconnect_db(self, session):
        try:
            session.close()
        except Exception, e:
            self.log.log_msg("Exception in disconnect_db() %s" % str(e))