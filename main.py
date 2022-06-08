from fastapi import FastAPI
import os, subprocess, shutil
from classes import *
from functions import *
from provider import provider_block_script
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="LattineMBL")



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/create_project/')
def create_new_project(project: Project):
    project_path = f'/Deploy-Terraform/{project.username}/{project.project_name}'
    if project.project_name != "init_project":
        if not os.path.exists(f'/Deploy-Terraform/{project.username}/{project.project_name}/'):
            os.makedirs(f'{project_path}/init_project/')
            os.system(f'touch /Deploy-Terraform/{project.username}/{project.project_name}/init_project/init.txt')


@app.delete('/api/delete_project/')
def delete_existing_project(project: Project):
        shutil.rmtree(f'/Deploy-Terraform/{project.username}/{project.project_name}')
        
@app.post('/api/account_credentials/')
def set_account_credentials(useracc: UserAccount, project: Project):
    if(useracc):
        os.system(f'az login -u {useracc.user_email} -p {useracc.user_password}')
        account_settings = provider_block_script()
    else:
        account_settings = provider_block_script(useracc.subscription_id, useracc.client_id, useracc.client_secret, useracc.tenant_id)
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/provider.tf', 'a+')
    terraform_file.write(account_settings)
    return {"Status": "Account authenticated!"}         

@app.post('/api/resource_group/')
def create_resource_group(rg: ResourceGroup, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(resource_group_script(rg))
    return {"Status": "Resource Group created!"}


@app.post('/api/virtual_network/')
def create_virtual_network(vnet: VirtualNetwork, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(virtual_network_script(vnet))
    return {"Status": "Virtual Network created!"}


@app.post('/api/subnet/')
def create_subnet(subnet: Subnet, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(vnet_subnets_script(subnet))
    return {"Status": "Subnet created!"}


@app.post('/api/windows_virtual_machine/')
def create_virtual_machine(vm: WindowsVirtualMachine, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(windows_virtual_machine_script(vm))
    return {"Status": "Virtual Machine created!"}

@app.post('/api/random_integer/')
def create_random(rd: Rando, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(Random(rd))
    return {"Status": "Random Integer created!"}

@app.post('/api/azurerm_app_service_plan/')
def create_app_service(sp: ServicePlan, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(ServiçoAP(sp))
    return {"Status": "App service created!"}

@app.post('/api/azurerm_app_service_vm/')
def create_machine_app_Service(mp: MachineServicePlan, project: Project):
    terraform_file = open(f'/Deploy-Terraform/{project.username}/{project.project_name}/main.tf', 'a+')
    terraform_file.write(MachinePlan(mp))
    return {"Status": "MachineAP created!"}

@app.post('/api/apply/')
def apply_infrastructure(project: Project):
    os.chdir(f'/Deploy-Terraform/{project.username}/{project.project_name}')
    os.system('terraform init')
    os.system('terraform apply --auto-approve')
    return {"Status": "Success apply!"}

@app.delete('/api/destroy/')
def destroy_infrastructure(project: Project):
    os.chdir(f'/Deploy-Terraform/{project.username}/{project.project_name}/')
    os.system('terraform apply -destroy --auto-approve')
    return {"Status": "Infrasctructure and files destroyed"}
