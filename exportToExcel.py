import pandas as pd
import logging

import divineStatus

logger = logging.getLogger(__name__)

def export_to_excel():

    projectsDict = divineStatus.get_projects()
    users = divineStatus.get_users()
    floatingIps = divineStatus.get_floatingIps()
    servers = divineStatus.get_servers()
    hypervisors = divineStatus.get_hypervisors()
    images = divineStatus.get_images()
    networks = divineStatus.get_networks()
    routers = divineStatus.get_routers()
    flavors = divineStatus.get_flavors()
    volumes = divineStatus.get_volumes()

    df_projects = pd.DataFrame(projectsDict['projects'])
    df_users = pd.DataFrame(users['users'])
    df_floatingIps = pd.DataFrame(floatingIps['floatingIps'])
    df_servers = pd.DataFrame(servers['servers'])
    df_hypervisors = pd.DataFrame(hypervisors['hypervisors'])
    df_images = pd.DataFrame(images['images'])
    df_networks = pd.DataFrame(networks['networks'])
    df_routers = pd.DataFrame(routers['routers'])
    df_flavors = pd.DataFrame(flavors['flavors'])
    df_volumes = pd.DataFrame(volumes['volumes'])

    writer = pd.ExcelWriter('fileOutput.xlsx', engine='xlsxwriter')

    try:

        logger.info('Exporting data to excel file ...')
        df_projects.to_excel(writer, sheet_name = 'PROJECTS', index=False)
        df_users.to_excel(writer, sheet_name = 'USERS', index=False)
        df_floatingIps.to_excel(writer, sheet_name = 'IPS', index=False)
        df_servers.to_excel(writer, sheet_name = 'SERVERS', index=False)
        df_hypervisors.to_excel(writer, sheet_name = 'HYPERVISORS', index=False)
        df_images.to_excel(writer, sheet_name = 'IMAGES', index=False)
        df_networks.to_excel(writer, sheet_name = 'NETWORKS', index=False)
        df_routers.to_excel(writer, sheet_name = 'ROUTERS', index=False)    
        df_flavors.to_excel(writer, sheet_name = 'FLAVORS', index=False)
        df_volumes.to_excel(writer, sheet_name = 'VOLUMES', index=False)

    except Exception as e:
        logger.exception('Error occured while exporting to excel file {0}'.format(e))

    workbook = writer.book
    worksheet_projects = writer.sheets['PROJECTS']
    worksheet_users = writer.sheets['USERS']
    worksheet_floatingIps = writer.sheets['IPS']
    worksheet_servers = writer.sheets['SERVERS']
    worksheet_hypervisors = writer.sheets['HYPERVISORS']
    worksheet_images = writer.sheets['IMAGES']
    worksheet_networks = writer.sheets['NETWORKS']
    worksheet_routers = writer.sheets['ROUTERS']
    worksheet_flavors = writer.sheets['FLAVORS']
    worksheet_volumes = writer.sheets['VOLUMES']

    worksheet_projects.set_column('A:C', 40)
    worksheet_users.set_column('A:C', 30)
    worksheet_floatingIps.set_column('A:D', 18)
    worksheet_servers.set_column('B:B', 34)
    worksheet_servers.set_column('C:F', 16)
    worksheet_hypervisors.set_column('A:I', 12)
    worksheet_images.set_column('A:A', 16)
    worksheet_images.set_column('B:C', 34)
    worksheet_images.set_column('D:G', 16)
    worksheet_networks.set_column('A:E', 18)
    worksheet_routers.set_column('A:B', 16)
    worksheet_routers.set_column('C:C', 34)
    worksheet_routers.set_column('D:G', 16)
    worksheet_flavors.set_column('A:F', 12)
    worksheet_volumes.set_column('A:A', 12)
    worksheet_volumes.set_column('B:C', 32)
    worksheet_volumes.set_column('D:G', 12)

    writer.save() 




