from multiprocessing.reduction import steal_handle
from typing import Optional
from unicodedata import name
from pydantic import BaseModel

class User(BaseModel):
    username: Optional[str] = "LattineGroup"

class Project(BaseModel):
    username: Optional[str] = "Lattine"
    project_name: Optional[str] = "GroupMBL"

class UserAccount(BaseModel):
    user_email: Optional[str] = 'leonardo.menezes3@portalsesisp.org.br'
    user_password: Optional[str] = 'M4@gta5u'
    
    subscription_id: Optional[str] = 'b1ef0eb9-7827-4dae-ab19-4ab3cf4e1ae4'
    client_id: Optional[str] = 'azure-cli-2022-05-20-00-07-55'
    client_secret: Optional[str] = 'evv_lZJT.hL4_74mKzJEuO~H9RUvsHM2zC'
    tenant_id: Optional[str] = 'b1051c4b-3b94-41ab-9441-e73a72342fdd'

class ResourceGroup(BaseModel):
    name: str = 'MBL'
    location: str = 'brazilsouth'

class VirtualNetwork(BaseModel):
    name:str = "vnet-mbl"
    rg: str = "MBL"
    cidr_block: str = '10.0.0.0/16'


class Subnet(BaseModel):
    name: str = "subnet-mbl" 
    vnet: str = "vnet-mbl"
    cidrblock: str = '10.0.1.0/24'
    resource_group: str = "MBL" 

class NatGateway(BaseModel):
    name: str = "nat-mbl"
    resource_group: str = "MBL"

class WindowsVirtualMachine(BaseModel):
    name: Optional [str] = "MachineMBL"
    rg: Optional [str] = "MBL"
    nsg: Optional[str] = "SG-MBL"
    subnet: Optional [str] = "subnet-mbl"
    size: Optional[str] = 'Standard_DS1_v2'
    username: Optional[str] = 'rootuser'
    password: Optional[str] = 'Senai@132'
    hostname: Optional[str] = 'azurevm'
    image: Optional[list] = ['MicrosoftWindowsServer', 'WindowsServer', '2016-Datacenter', 'latest']

class Rando(BaseModel):
    name: str = "rando-MBL"
    resource_group: str = "MBL"
    min: str = "10000"
    max: str = "99999"


class ServicePlan(BaseModel):
    name: str = "Plan-MBL"
    resource_group: str = "MBL"
    tier: str = "Free"
    size: str = "F1"

class MachineServicePlan(BaseModel):
    name: str = "VM-MBL"
    resource_group: str = "MBL"
    app_service_plan_id: str = "Plan-MBL"
    repo_url: str = "https://github.com/Azure-Samples/nodejs-docs-hello-world"
    branch: str = "master"  
    manual_integration: str = "true"
    mercurial: str = "false"

   
    
