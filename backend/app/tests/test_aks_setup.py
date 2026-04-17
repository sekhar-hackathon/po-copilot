import unittest
from unittest.mock import patch, MagicMock
from app.services.aks_setup import AKSStagingEnvironment

class TestAKSStagingEnvironment(unittest.TestCase):
    @patch('app.services.aks_setup.ResourceManagementClient')
    @patch('app.services.aks_setup.ContainerServiceClient')
    @patch('app.services.aks_setup.DefaultAzureCredential')
    def test_setup_environment(self, mock_credential, mock_container_client, mock_resource_client):
        mock_resource_client.return_value.resource_groups.create_or_update = MagicMock()
        mock_container_client.return_value.managed_clusters.begin_create_or_update = MagicMock()

        aks_env = AKSStagingEnvironment('test-subscription-id', 'test-resource-group', 'test-aks-cluster')
        aks_env.setup_environment()

        mock_resource_client.return_value.resource_groups.create_or_update.assert_called_once_with(
            'test-resource-group', {'location': 'eastus'}
        )
        mock_container_client.return_value.managed_clusters.begin_create_or_update.assert_called_once_with(
            'test-resource-group', 'test-aks-cluster', {
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
                'dns_prefix': 'test-aks-cluster'
            }
        )

if __name__ == '__main__':
    unittest.main()
