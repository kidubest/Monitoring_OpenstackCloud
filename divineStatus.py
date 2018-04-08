import json
import logging

from openstack import connection
from collections import OrderedDict

logger = logging.getLogger(__name__)

conn = connection.Connection(cloud='divine')

def get_projects():

    global projects

    logger.info('Getting projects ..')
    projects = {}
    projectList = []
    for project in conn.list_projects():
        projectDict = OrderedDict()
        projects[project.get('id')]=project.get('name')
        projectDict['name']=project.get('name')
        projectDict['id']=project.get('id')
        projectDict['description'] = project.get('description')

        for user in conn.list_users():
            if project.get('id') == user.get('default_project_id'):
                projectDict['user'] = user.get('name')

        projectList.append(projectDict)

    projectsDict = {'projects' : projectList}
    return projectsDict

def get_users():

    logger.info('Getting users ...')
    usersList = []
    for user in conn.list_users():
        userDict = OrderedDict()


        userDict['name'] = user.get('name')
        userDict['id'] = user.get('id')
        for key in projects.keys():
            if key == user.get('default_project_id'):
                userDict['project'] = projects.get(key) 

        usersList.append(userDict)

    users = {'users' : usersList}
    return users


def get_floatingIps():

    logger.info('Getting Floating IPs ..')
    floatingIpList = []
    ipSet = set()

    for server in conn.list_servers(all_projects=True):
        serverIpDict = OrderedDict()
        serverIp = server.get('public_v4')
        ipSet.add(serverIp)
        if len(serverIp) != 0: 
            serverIpDict['name'] = server.get('name')
            serverIpDict['floating_ip'] = serverIp
            serverIpDict['status'] = server.get('status')

            floatingIpList.append(serverIpDict)

    for floatingIp in conn.list_floating_ips():
        floatingIPDict = OrderedDict()
        ip = floatingIp.get('floating_ip_address')
        if ip not in ipSet:
            for key in projects.keys():
                if key == floatingIp.get('project_id'):
                    floatingIPDict['name'] = projects.get(key) 
            floatingIPDict['floating_ip'] = ip
            floatingIPDict['status'] = floatingIp.get('status')

            floatingIpList.append(floatingIPDict)

    for router in conn.list_routers():
        routerIpDict = OrderedDict()
        external_gateway_info = router.get('external_gateway_info')
        if external_gateway_info is not None:
            routerIpDict['name'] = router.get('name')
            routerIpDict['floating_ip'] = external_gateway_info.get('external_fixed_ips')[0].get('ip_address')
            routerIpDict['status'] = router.get('status')

            floatingIpList.append(routerIpDict)

    floatingIps = {"floatingIps" : floatingIpList}
    return floatingIps


def get_servers():

    logger.info('Getting Servers ...')
    serverTaskList = []
    for server in conn.list_servers(all_projects=True):
        serverDict = OrderedDict()
        serverIpDict = OrderedDict()
        for key in projects.keys():
            if key == server.get('tenant_id'):
                serverDict['project'] = projects.get(key) 

        serverDict['id'] = server.get('id')
        serverDict['Host'] = server.get('OS-EXT-SRV-ATTR:host')
        serverDict['name'] = server.get('name')
        serverDict['floating_ip'] = server.get('public_v4')
        serverDict['status'] = server.get('status')

        serverTaskList.append(serverDict)

    servers = {'servers' : serverTaskList}
    return servers


def get_hypervisors():

    logger.info('Getting hypervisors ...')
    hypervisorList = []
    for hypervisor in conn.list_hypervisors():
        hypervisorDict = OrderedDict()
        hypervisorDict['hostname'] = hypervisor.get('hypervisor_hostname')
        hypervisorDict['status'] = hypervisor.get('status')
        hypervisorDict['vcpu_used'] = hypervisor.get('vcpus_used')
        hypervisorDict['vcpu_total'] = hypervisor.get('vcpus')
        hypervisorDict['memory_used_gb'] = hypervisor.get('local_gb_used')
        hypervisorDict['free_ram_gm'] = hypervisor.get('free_ram_mb')
        hypervisorDict['localdisk_gb_used'] = hypervisor.get('local_gb_used')
        hypervisorDict['free_disk_gb'] = hypervisor.get('free_disk_gb')
        hypervisorDict['instances'] = hypervisor.get('running_vms')

        hypervisorList.append(hypervisorDict)

    hypervisors = {'hypervisors' : hypervisorList}
    return hypervisors


def get_images():

    logger.info('Getting images ...')
    imageList = []
    for image in conn.list_images():
        imageDict = OrderedDict()

        for key in projects.keys():
            if key == image.get('owner'):
                imageDict['project_owner'] = projects.get(key) 
        imageDict['id'] = image.get('id')
        imageDict['name'] = image.get('name')
        imageDict['visibility'] = image.get('visibility')
        imageDict['status'] = image.get('status')
        imageDict['disk_format'] = image.get('disk_format')
        imageDict['size'] = image.get('size')

        imageList.append(imageDict)

    images = {'images' : imageList}
    return images


def get_networks():

    logger.info('Getting networks and subnets ...')
    networkList = []
    for network in conn.list_networks():
        networkDict = OrderedDict()
        for key in projects.keys():
            if key == network.get('project_id'):
                networkDict['project'] = projects.get(key)

        networkDict['name'] = network.get('name')
        for subnet in conn.list_subnets():
            if subnet.get('network_id') == network.get('id'):
                networkDict['subnet_associated'] = subnet.get('cidr')

        networkDict['status'] = network.get('status')

        networkList.append(networkDict)

    networks = {'networks' : networkList}
    return networks


def get_routers():

    logger.info('Getting routers ...')
    routerList = []
    for router in conn.list_routers():
        routerDict = OrderedDict()

        for key in projects.keys():
            if key == router.get('project_id'):
                routerDict['project_name'] = projects.get(key) 

        routerDict['name'] = router.get('name')
        routerDict['id'] = router.get('id')
        routerDict['status'] = router.get('status')
        if router.get('external_gateway_info') is not None:
            routerDict['ip_address'] = router.get('external_gateway_info').get('external_fixed_ips')[0].get('ip_address')

        routerDict['ha_mode'] = router.get('ha')
        routerDict['admin_state'] = router.get('admin_state_up')

        routerList.append(routerDict)

    routers = {'routers' : routerList}

    return routers


def get_flavors():

    logger.info('Getting flavors ...')
    flavorList = []
    for flavor in conn.list_flavors():
        flavorDict = OrderedDict()

        for key in projects.keys():
            if key == flavor.get('location').get('project').get('id'):
                flavorDict['project'] = projects.get(key) 

        flavorDict['flavor_name'] = flavor.get('name')
        flavorDict['VCPUs'] = flavor.get('vcpus')
        flavorDict['RAM'] = flavor.get('ram')
        flavorDict['Root_Disk'] = flavor.get('disk')
        flavorDict['Is_public'] = flavor.get('is_public')

        flavorList.append(flavorDict)

    flavors = {'flavors' : flavorList}

    return flavors


def get_volumes():

    logger.info('Getting volumes ...')
    volumeList = []
    query = {'all_tenants' : 1}

    for volume in conn.volume.volumes(details=True, **query):

        volumeDict = OrderedDict()
        for key in projects.keys():
            if key == volume.project_id:
                volumeDict['project'] = projects.get(key)

        volumeDict['host'] = volume.host
        volumeDict['id'] = volume.id
        volumeDict['size'] = volume.size
        volumeDict['status'] = volume.status
        volumeDict['is_bootable'] = volume.is_bootable
        volumeDict['is_encrypted'] = volume.is_encrypted

        volumeList.append(volumeDict)

    volumes = {'volumes' : volumeList}

    return volumes
    



