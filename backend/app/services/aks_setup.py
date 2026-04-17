import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

class AKSStagingEnvironment:
    def __init__(self, subscription_id: str, resource_group_name: str, aks_cluster_name: str):
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.aks_cluster_name = aks_cluster_name
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        self.aks_client = ContainerServiceClient(self.credential, self.subscription_id)

    def create_resource_group(self) -> None:
        print(f"Creating resource group: {self.resource_group_name}")
        self.resource_client.resource_groups.create_or_update(
            self.resource_group_name,
            {
                'location': 'eastus'
            }
        )

    def create_aks_cluster(self) -> None:
        print(f"Creating AKS cluster: {self.aks_cluster_name}")
        self.aks_client.managed_clusters.begin_create_or_update(
            self.resource_group_name,
            self.aks_cluster_name,
            {
                'location': 'eastus',
                'kubernetes_version': '1.21.2',
                'agent_pool_profiles': [
                    {
                        'name': 'agentpool',
                        'count': 3,
                        'vm_size': 'Standard_DS2_v2',
                        'os_type': 'Linux'
                    }
                ],
                'dns_prefix': self.aks_cluster_name
            }
        )

    def setup_environment(self) -> None:
        self.create_resource_group()
        self.create_aks_cluster()

if __name__ == "__main__":
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    resource_group_name = os.getenv('AZURE_RESOURCE_GROUP')
    aks_cluster_name = os.getenv('AKS_CLUSTER_NAME')

    aks_env = AKSStagingEnvironment(subscription_id, resource_group_name, aks_cluster_name)
    aks_env.setup_environment()
