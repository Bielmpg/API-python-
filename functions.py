import classes
import textwrap

def resource_group_script(rg: classes.ResourceGroup):
    rg_script = textwrap.dedent(f'''

    # Creating Azure Resource Group 
    resource "azurerm_resource_group" "{rg.name}" {{
      name     = "{rg.name}"
      location = "{rg.location}"
    }}''')
    return rg_script

def virtual_network_script(vnet: classes.VirtualNetwork):
    vnet_script = textwrap.dedent(f'''

    # Creating Azure Virtual Network
    resource "azurerm_virtual_network" "{vnet.name}" {{
      name                = "{vnet.name}"
      location            = azurerm_resource_group.{vnet.rg}.location
      address_space       = ["{vnet.cidr_block}"]
      resource_group_name = azurerm_resource_group.{vnet.rg}.name
    }}
    ''')
    return vnet_script


def vnet_subnets_script(subnet: classes.Subnet):
    subnet_script = textwrap.dedent(f'''
    resource "azurerm_subnet" "{subnet.name}" {{
      name           = "{subnet.name}"
      resource_group_name  = azurerm_resource_group.{subnet.resource_group}.name
      virtual_network_name = azurerm_virtual_network.{subnet.vnet}.name
      address_prefixes = ["{subnet.cidrblock}"]
    }}
    ''')
    return subnet_script

def windows_virtual_machine_script(vm: classes.WindowsVirtualMachine):
    vm_script = textwrap.dedent(f'''

    # VM Public IP
    resource "azurerm_public_ip" "{vm.name}-public-ip" {{
      name                = "{vm.name}-public-ip"
      resource_group_name = azurerm_resource_group.{vm.rg}.name
      location            = azurerm_resource_group.{vm.rg}.location
      allocation_method   = "Dynamic"
    }}
    
    # Network Interface for VM
    resource "azurerm_network_interface" "{vm.name}-nic" {{
      name                = "{vm.name}-nic"
      location            = azurerm_resource_group.{vm.rg}.location
      resource_group_name = azurerm_resource_group.{vm.rg}.name
      ip_configuration {{
        name                          = "{vm.name}-ip-config"
        subnet_id                     = azurerm_subnet.{vm.subnet}.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id = azurerm_public_ip.{vm.name}-public-ip.id
      }}
    }}
    
    # Windows Virtual Machine
    resource "azurerm_windows_virtual_machine" "{vm.name}" {{
      name                = "{vm.name}"
      resource_group_name = azurerm_resource_group.{vm.rg}.name
      location            = azurerm_resource_group.{vm.rg}.location
      size                = "{vm.size}"
      admin_username      = "{vm.username}"
      admin_password      = "{vm.password}"
      network_interface_ids = [
        azurerm_network_interface.{vm.name}-nic.id,
      ]

      os_disk {{
        name                 = "osdisk-{vm.name}"
        caching              = "ReadWrite"
        storage_account_type = "Standard_LRS"
      }}

      source_image_reference {{
        publisher = "{vm.image[0]}"
        offer     = "{vm.image[1]}"
        sku       = "{vm.image[2]}"
        version   = "{vm.image[3]}"
      }}
    }}
    ''')
    
    return vm_script

def Random(rd: classes.Rando):
    rd_script = textwrap.dedent(f'''

# Serviço de aplicativo
resource "random_integer" "{rd.name}" {{
  min =  "{rd.min}"
  max = "{rd.max}"
}}
''')
    
    return rd_script

def ServiçoAP(sp: classes.ServicePlan):
    sp_script = textwrap.dedent(f'''

#Serviço de aplicativo
resource "azurerm_app_service_plan" "{sp.name}" {{
  name                = "{sp.name}"
  location            = azurerm_resource_group.{sp.resource_group}.location
  resource_group_name = azurerm_resource_group.{sp.resource_group}.name
  sku {{
  tier = "{sp.tier}"
  size = "{sp.size}"
}}
  }}
''')
    
    return sp_script

def MachinePlan(mp: classes.MachineServicePlan):
    mp_script = textwrap.dedent(f'''

resource "azurerm_app_service" "{mp.name}" {{
  name                = "{mp.name}"
  location            = azurerm_resource_group.{mp.resource_group}.location
  resource_group_name = azurerm_resource_group.{mp.resource_group}.name
  app_service_plan_id = azurerm_app_service_plan.{mp.app_service_plan_id}.id
  source_control {{
  repo_url           = "{mp.repo_url}"
  branch             = "{mp.branch}"
  manual_integration = "{mp.manual_integration}"
  use_mercurial      = "{mp.mercurial}"
}}
  }}
''')
    
    return mp_script

