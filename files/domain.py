ORACLE_HOME = '/opt/oraclefmw/product/oracle_home'
WLHOME      = ORACLE_HOME+'/wlserver'
DOMAIN      = 'domain1'
DOMAIN_PATH = '/opt/oraclefmw/config/domains/' + DOMAIN
APP_PATH    = '/opt/oraclefmw/config/applications/' + DOMAIN

ADMIN_SERVER_ADDRESS = 'admin-server'
SOA_SERVER_ADDRESS = 'soa-server'
OSB_SERVER_ADDRESS = 'osb-server'
BAM_SERVER_ADDRESS = 'bam-server'
LOG_FOLDER     = '/opt/oraclefmw/weblogic/'

# Expanded or Compact
DOMAIN_MODE = 'Expanded'
JSSE_ENABLED     = true
DEVELOPMENT_MODE = true
WEBTIER_ENABLED  = false

ADMIN_SERVER   = 'AdminServer'
ADMIN_USER     = 'weblogic'
ADMIN_PASSWORD = 'welcome1'

JAVA_HOME      = '/usr/java/latest'

ADM_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+LOG_FOLDER+'AdminServer_err.out'
OSB_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1024m '
SOA_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=752m -Xms1024m -Xmx1532m '
BAM_JAVA_ARGUMENTS = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m '

SOA_REPOS_DBURL          = 'jdbc:oracle:thin:@soa-database:1521/orcl'
SOA_REPOS_DBUSER_PREFIX  = 'DEV'
SOA_REPOS_DBPASSWORD     = 'welcome1'

SOA_ENABLED=false
OSB_ENABLED=true
BPM_ENABLED=false
BAM_ENABLED=false
B2B_ENABLED=false
ESS_ENABLED=false

def createBootPropertiesFile(directoryPath,fileName, username, password):
    serverDir = File(directoryPath)
    bool = serverDir.mkdirs()
    fileNew=open(directoryPath + '/'+fileName, 'w')
    fileNew.write('username=%s\n' % username)
    fileNew.write('password=%s\n' % password)
    fileNew.flush()
    fileNew.close()

def createAdminStartupPropertiesFile(directoryPath, args):
    adminserverDir = File(directoryPath)
    bool = adminserverDir.mkdirs()
    fileNew=open(directoryPath + '/startup.properties', 'w')
    args=args.replace(':','\\:')
    args=args.replace('=','\\=')
    fileNew.write('Arguments=%s\n' % args)
    fileNew.flush()
    fileNew.close()

def defineMachine(machineName, machineAddress):
    print('Create machine ' + machineName + ' with type UnixMachine')
    cd('/')
    create(machineName,'UnixMachine')
    cd('UnixMachine/' + machineName)
    create(machineName,'NodeManager')
    cd('NodeManager/' + machineName)
    set('ListenAddress',machineAddress)

def changeDatasourceToXA(datasource):
    print 'Change datasource '+datasource
    cd('/')
    cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDriverParams/NO_NAME_0')
    set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
    set('UseXADataSourceInterface','True')
    cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDataSourceParams/NO_NAME_0')
    set('GlobalTransactionsProtocol','TwoPhaseCommit')
    cd('/')

def changeManagedServer(server,machine,address,port,java_arguments):
    cd('/Servers/'+server)
    set('Machine'      ,machine)
    set('ListenAddress',address)
    set('ListenPort'   ,port)

    create(server,'ServerStart')
    cd('ServerStart/'+server)
    set('Arguments' , java_arguments+' -Dweblogic.Stdout='+LOG_FOLDER+server+'.out -Dweblogic.Stderr='+LOG_FOLDER+server+'_err.out')
    set('JavaVendor','Sun')
    set('JavaHome'  , JAVA_HOME)

    cd('/Server/'+server)
    create(server,'SSL')
    cd('SSL/'+server)
    set('Enabled'                    , 'False')
    set('HostNameVerificationIgnored', 'True')

    if JSSE_ENABLED == true:
        set('JSSEEnabled','True')
    else:
        set('JSSEEnabled','False')

    cd('/Server/'+server)
    create(server,'Log')
    cd('/Server/'+server+'/Log/'+server)
    set('FileName'     , LOG_FOLDER+server+'.log')
    set('FileCount'    , 10)
    set('FileMinSize'  , 5000)
    set('RotationType' ,'byTime')
    set('FileTimeSpan' , 24)

print('Start...wls domain with template ORACLE_HOME/wlserver/common/templates/wls/wls.jar')
readTemplate(ORACLE_HOME+'/wlserver/common/templates/wls/wls.jar', DOMAIN_MODE)


cd('/')

print('Set domain log')
create('base_domain','Log')

cd('/Log/base_domain')
set('FileName'    ,LOG_FOLDER+DOMAIN+'.log')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

cd('/Servers/AdminServer')
# name of adminserver
set('Name',ADMIN_SERVER )

cd('/Servers/'+ADMIN_SERVER)

# address and port
set('ListenAddress',ADMIN_SERVER_ADDRESS)
set('ListenPort'   ,7001)

setOption( "AppDir", APP_PATH )

create(ADMIN_SERVER,'ServerStart')
cd('ServerStart/'+ADMIN_SERVER)
set('Arguments' , ADM_JAVA_ARGUMENTS)
set('JavaVendor','Sun')
set('JavaHome'  , JAVA_HOME)

cd('/Server/'+ADMIN_SERVER)
create(ADMIN_SERVER,'SSL')
cd('SSL/'+ADMIN_SERVER)
set('Enabled'                    , 'False')
set('HostNameVerificationIgnored', 'True')

if JSSE_ENABLED == true:
    set('JSSEEnabled','True')
else:
    set('JSSEEnabled','False')


cd('/Server/'+ADMIN_SERVER)

create(ADMIN_SERVER,'Log')
cd('/Server/'+ADMIN_SERVER+'/Log/'+ADMIN_SERVER)
set('FileName'    ,LOG_FOLDER+ADMIN_SERVER+'.log')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

print('Set password...')
cd('/')
cd('Security/base_domain/User/weblogic')

# weblogic user name + password
set('Name',ADMIN_USER)
cmo.setPassword(ADMIN_PASSWORD)

if DEVELOPMENT_MODE == true:
    setOption('ServerStartMode', 'dev')
else:
    setOption('ServerStartMode', 'prod')

setOption('JavaHome', JAVA_HOME)

print('write domain...')
# write path + domain name
writeDomain(DOMAIN_PATH)
closeTemplate()

createAdminStartupPropertiesFile(DOMAIN_PATH+'/servers/'+ADMIN_SERVER+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(DOMAIN_PATH+'/servers/'+ADMIN_SERVER+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DOMAIN_PATH+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

es = encrypt(ADMIN_PASSWORD,DOMAIN_PATH)
readDomain(DOMAIN_PATH)

print('set domain password...')
cd('/SecurityConfiguration/'+DOMAIN)
set('CredentialEncrypted',es)

print('Set nodemanager password')
set('NodeManagerUsername'         ,ADMIN_USER )
set('NodeManagerPasswordEncrypted',es )

cd('/')
setOption( "AppDir", APP_PATH )

if OSB_ENABLED == true:
    print('Extend...osb domain with template ORACLE_HOME/osb/common/templates/wls/oracle.osb_template.jar')
    addTemplate(ORACLE_HOME+'/oracle_common/common/templates/wls/oracle.wls-webservice-template.jar')
    addTemplate(ORACLE_HOME+'/osb/common/templates/wls/oracle.osb_template.jar')

print 'Adding ApplCore Template'
addTemplate(ORACLE_HOME+'/oracle_common/common/templates/wls/oracle.applcore.model.stub_template.jar')

if SOA_ENABLED == true:
    print 'Adding SOA Template'
    addTemplate(ORACLE_HOME+'/soa/common/templates/wls/oracle.soa_template.jar')

if BAM_ENABLED == true:
    print 'Adding BAM Template'
    addTemplate(ORACLE_HOME+'/soa/common/templates/wls/oracle.bam.server_template.jar')

if BPM_ENABLED == true:
    print 'Adding BPM Template'
    addTemplate(ORACLE_HOME+'/soa/common/templates/wls/oracle.bpm_template.jar')

if WEBTIER_ENABLED == true:
    print 'Adding OHS Template'
    addTemplate(ORACLE_HOME+'/ohs/common/templates/wls/ohs_managed_template.jar')

if B2B_ENABLED == true:
    print 'Adding B2B Template'
    addTemplate(ORACLE_HOME+'/soa/common/templates/wls/oracle.soa.b2b_template.jar')

if ESS_ENABLED == true:
    print 'Adding ESS Template'
    addTemplate(ORACLE_HOME+'/oracle_common/common/templates/wls/oracle.ess.basic_template.jar')
    addTemplate(ORACLE_HOME+'/em/common/templates/wls/oracle.em_ess_template.jar')


dumpStack()

print 'Change datasources'

print 'Change datasource LocalScvTblDataSource'
cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL',SOA_REPOS_DBURL)
set('PasswordEncrypted',SOA_REPOS_DBPASSWORD)
cd('Properties/NO_NAME_0/Property/user')
set('Value',SOA_REPOS_DBUSER_PREFIX+'_STB')

print 'Call getDatabaseDefaults which reads the service table'
getDatabaseDefaults()

if SOA_ENABLED == true:
    changeDatasourceToXA('EDNDataSource')

if OSB_ENABLED == true:
    changeDatasourceToXA('wlsbjmsrpDataSource')

changeDatasourceToXA('OraSDPMDataSource')
changeDatasourceToXA('SOADataSource')

if BAM_ENABLED == true:
    changeDatasourceToXA('BamDataSource')

print 'end datasources'

if SOA_ENABLED == true:
    defineMachine('SOA_Machine', SOA_SERVER_ADDRESS)

if OSB_ENABLED == true:
    defineMachine('OSB_Machine', OSB_SERVER_ADDRESS)

if BAM_ENABLED == true:
    defineMachine('BAM_Machine', BAM_SERVER_ADDRESS)

print('Create machine AdminMachine with type UnixMachine')
cd('/')
create('AdminMachine','UnixMachine')
cd('UnixMachine/AdminMachine')
create('AdminMachine','NodeManager')
cd('NodeManager/AdminMachine')
set('ListenAddress',ADMIN_SERVER_ADDRESS)

print 'Change AdminServer'
cd('/Servers/'+ADMIN_SERVER)
set('Machine','AdminMachine')

if SOA_ENABLED == true:
    print 'change soa_server1'
    cd('/')
    changeManagedServer('soa_server1','SOA_Machine',SOA_SERVER_ADDRESS,8001,SOA_JAVA_ARGUMENTS)

if BAM_ENABLED == true:
    print 'change bam_server1'
    cd('/')
    changeManagedServer('bam_server1','BAM_Machine',BAM_SERVER_ADDRESS,9001,BAM_JAVA_ARGUMENTS)

if OSB_ENABLED == true:
    print 'change osb_server1'
    cd('/')
    changeManagedServer('osb_server1','OSB_Machine',OSB_SERVER_ADDRESS,8011,OSB_JAVA_ARGUMENTS)

print 'Add server groups WSM-CACHE-SVR WSMPM-MAN-SVR JRF-MAN-SVR to AdminServer'
serverGroup = ["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"]
setServerGroups(ADMIN_SERVER, serverGroup)

if SOA_ENABLED == true:
    if ESS_ENABLED == true:
        print 'Add server group SOA-MGD-SVRS,ESS-MGD-SVRS to soa_server1'
        cd('/')
        delete('ess_server1', 'Server')
        serverGroup = ["SOA-MGD-SVRS","ESS-MGD-SVRS"]
    else:
        print 'Add server group SOA-MGD-SVRS to soa_server1'
        serverGroup = ["SOA-MGD-SVRS"]

    setServerGroups('soa_server1', serverGroup)

if BAM_ENABLED == true:
    print 'Add server group BAM12-MGD-SVRS to bam_server1'
    serverGroup = ["BAM12-MGD-SVRS"]
    setServerGroups('bam_server1', serverGroup)

if OSB_ENABLED == true:
    print 'Add server group OSB-MGD-SVRS-COMBINED to osb_server1'
    serverGroup = ["OSB-MGD-SVRS-COMBINED"]
    setServerGroups('osb_server1', serverGroup)

print 'end server groups'

updateDomain()
closeDomain();

if SOA_ENABLED == true:
    createBootPropertiesFile(DOMAIN_PATH+'/servers/soa_server1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

if BAM_ENABLED == true:
    createBootPropertiesFile(DOMAIN_PATH+'/servers/bam_server1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

if OSB_ENABLED == true:
    createBootPropertiesFile(DOMAIN_PATH+'/servers/osb_server1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

print('Exiting SOA Domain creation completed ...')
exit()
